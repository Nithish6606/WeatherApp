import requests
import logging
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

class ServiceUnavailable(Exception):
    """Raised when both primary and secondary weather services fail."""
    pass

def _fetch_openweather(lat, lon):
    """
    Fetch weather data from OpenWeatherMap (Primary).
    Timeout: 3 seconds.
    """
    api_key = settings.OPENWEATHER_API_KEY
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"

    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        data = response.json()

        return {
            "temp": float(data["main"]["temp"]),
            "humidity": int(data["main"]["humidity"]),
            "description": str(data["weather"][0]["description"]),
            "wind_speed": round(float(data["wind"]["speed"]) * 3.6, 1), # Convert m/s to km/h
            "location_name": data.get("name", "Farm Location"),
            "source": "OpenWeatherMap"
        }
    except (requests.exceptions.RequestException, KeyError, ValueError) as e:
        logger.warning(f"OpenWeatherMap failed: {e}")
        raise

def _fetch_openmeteo(lat, lon):
    """
    Fetch weather data from Open-Meteo (Secondary).
    Timeout: 3 seconds.
    """
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"

    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        data = response.json()
        current = data["current_weather"]

        return {
            "temp": float(current["temperature"]),
            "humidity": 0, # Open-Meteo current_weather doesn't provide humidity directly in this endpoint
            "description": "Clear sky" if current["weathercode"] == 0 else "Cloudy/Rainy", # Simplified mapping
            "wind_speed": float(current["windspeed"]), # Open-Meteo defaults to km/h
            "location_name": "Custom GPS Location",
            "source": "Open-Meteo"
        }
    except (requests.exceptions.RequestException, KeyError, ValueError) as e:
        logger.warning(f"Open-Meteo failed: {e}")
        raise

def get_weather_data(lat, lon):
    """
    Orchestrator to fetch weather data.
    Tries OpenWeatherMap first (if key exists), then falls back to Open-Meteo.
    Raises ServiceUnavailable if both fail.
    Cached for 10 minutes.
    """
    cache_key = f"weather_{lat}_{lon}"
    
    def fetch_data():
        # Try OpenWeatherMap if key is present
        if settings.OPENWEATHER_API_KEY:
            try:
                data = _fetch_openweather(lat, lon)
                logger.info("Served via OpenWeatherMap")
                return data
            except Exception as e:
                logger.warning(f"OpenWeatherMap failed: {e}")
                # Fall through to Open-Meteo
        else:
            logger.info("No OpenWeatherMap API key found, skipping.")

        # Try Open-Meteo
        try:
            data = _fetch_openmeteo(lat, lon)
            logger.info("Served via Open-Meteo")
            return data
        except Exception as e:
            logger.error(f"Open-Meteo failed: {e}")
            raise ServiceUnavailable(f"Weather services unavailable. Last error: {str(e)}")

    return cache.get_or_set(cache_key, fetch_data, timeout=600)

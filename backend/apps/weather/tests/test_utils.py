import pytest
from unittest.mock import patch, MagicMock
from apps.weather.utils import get_weather_data, ServiceUnavailable


class TestGetWeatherData:
    """Unit tests for the get_weather_data function."""

    @pytest.fixture(autouse=True)
    def clear_cache(self, settings):
        """Clear cache before each test to ensure fresh data fetching."""
        from django.core.cache import cache
        cache.clear()

    @patch('apps.weather.utils._fetch_openweather')
    def test_success_from_openweather(self, mock_fetch_openweather):
        """Test successful fetch from OpenWeatherMap (primary service)."""
        expected_data = {
            "temp": 25.5,
            "humidity": 60,
            "description": "clear sky",
            "wind_speed": 5.2,
            "source": "OpenWeatherMap"
        }
        mock_fetch_openweather.return_value = expected_data

        result = get_weather_data(40.7128, -74.0060)

        assert result == expected_data
        mock_fetch_openweather.assert_called_once_with(40.7128, -74.0060)

    @patch('apps.weather.utils._fetch_openmeteo')
    @patch('apps.weather.utils._fetch_openweather')
    def test_fallback_to_openmeteo_when_openweather_fails(
        self, mock_fetch_openweather, mock_fetch_openmeteo
    ):
        """Test fallback to Open-Meteo when OpenWeatherMap fails."""
        mock_fetch_openweather.side_effect = Exception("OpenWeatherMap unavailable")
        expected_data = {
            "temp": 24.0,
            "humidity": 0,
            "description": "Clear sky",
            "wind_speed": 4.5,
            "source": "Open-Meteo"
        }
        mock_fetch_openmeteo.return_value = expected_data

        result = get_weather_data(40.7128, -74.0060)

        assert result == expected_data
        mock_fetch_openweather.assert_called_once()
        mock_fetch_openmeteo.assert_called_once_with(40.7128, -74.0060)

    @patch('apps.weather.utils._fetch_openmeteo')
    @patch('apps.weather.utils._fetch_openweather')
    def test_service_unavailable_when_both_fail(
        self, mock_fetch_openweather, mock_fetch_openmeteo
    ):
        """Test ServiceUnavailable is raised when both services fail."""
        mock_fetch_openweather.side_effect = Exception("OpenWeatherMap unavailable")
        mock_fetch_openmeteo.side_effect = Exception("Open-Meteo unavailable")

        with pytest.raises(ServiceUnavailable):
            get_weather_data(40.7128, -74.0060)

        mock_fetch_openweather.assert_called_once()
        mock_fetch_openmeteo.assert_called_once()

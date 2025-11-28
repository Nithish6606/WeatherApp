import pytest
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status


@pytest.fixture
def api_client():
    """Return an API client for testing."""
    return APIClient()


@pytest.fixture(autouse=True)
def clear_cache(settings):
    """Clear cache before each test to ensure fresh data fetching."""
    from django.core.cache import cache
    cache.clear()


class TestWeatherView:
    """API integration tests for the /api/weather/ endpoint."""

    @patch('apps.weather.views.get_weather_data')
    def test_weather_api_returns_200_with_valid_data(
        self, mock_get_weather_data, api_client
    ):
        """Test successful weather data response (200 OK)."""
        expected_data = {
            "temp": 25.5,
            "humidity": 60,
            "description": "clear sky",
            "wind_speed": 5.2,
            "source": "OpenWeatherMap"
        }
        mock_get_weather_data.return_value = expected_data

        response = api_client.get('/api/weather/current/', {'lat': '40.7128', 'lon': '-74.0060'})

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'temp' in data
        assert 'humidity' in data
        assert 'description' in data
        assert 'wind_speed' in data
        assert 'source' in data

    def test_weather_api_returns_400_without_parameters(self, api_client):
        """Test missing parameters response (400 Bad Request)."""
        response = api_client.get('/api/weather/current/')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert 'error' in data

    def test_weather_api_returns_400_with_invalid_coordinates(self, api_client):
        """Test invalid coordinates response (400 Bad Request)."""
        response = api_client.get('/api/weather/current/', {'lat': 'invalid', 'lon': 'invalid'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert 'error' in data

    @patch('apps.weather.views.get_weather_data')
    def test_weather_api_returns_503_when_service_unavailable(
        self, mock_get_weather_data, api_client
    ):
        """Test service unavailable response (503)."""
        from apps.weather.utils import ServiceUnavailable
        mock_get_weather_data.side_effect = ServiceUnavailable("Services unavailable")

        response = api_client.get('/api/weather/current/', {'lat': '40.7128', 'lon': '-74.0060'})

        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        data = response.json()
        assert 'error' in data

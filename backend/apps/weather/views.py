from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import get_weather_data, ServiceUnavailable

class WeatherView(APIView):
    def get(self, request):
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')

        if not lat or not lon:
            return Response(
                {"error": "Latitude and longitude are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            return Response(
                {"error": "Latitude and longitude must be valid numbers."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            weather_data = get_weather_data(lat, lon)
            return Response(weather_data, status=status.HTTP_200_OK)
        except ServiceUnavailable:
            return Response(
                {"error": "Weather services are currently unavailable."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

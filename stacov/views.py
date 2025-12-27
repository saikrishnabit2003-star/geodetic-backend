import os
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import parse_stacov_file
from django.http import JsonResponse

# def ping(request):
#     return JsonResponse({"message": "STACOV API working"})

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STACOV_DIR = os.path.join(BASE_DIR, "stacov", "stacov_files")


class StacovByDateAPIView(APIView):
    def get(self, request):
        date_str = request.query_params.get("date")
        if not date_str:
            return Response({"error": "date required (YYYY-MM-DD)"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # ⚡ Parse frontend date YYYY-MM-DD
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            # ⚡ Convert to filename format: YYMMMDD
            file_date = f"{str(date_obj.year % 100).zfill(2)}{date_obj.strftime('%b').lower()}{str(date_obj.day).zfill(2)}"
        except ValueError:
            return Response({"error": "Invalid date format"}, status=400)

        matched_file = None
        for file in os.listdir(STACOV_DIR):
            if file.startswith(file_date):
                matched_file = file
                break

        if not matched_file:
            return Response({"error": "STACOV file not found"}, status=404)

        file_path = os.path.join(STACOV_DIR, matched_file)
        stations = parse_stacov_file(file_path)

        # ⚡ Convert stations to GeoJSON
        geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [s["longitude"], s["latitude"]],
                    },
                    "properties": {
                        "station": s["station"],
                        "height": s["height"]
                    },
                }
                for s in stations
            ]
        }

        return Response(geojson)

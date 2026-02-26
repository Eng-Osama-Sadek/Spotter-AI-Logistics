from rest_framework.decorators import api_view
from rest_framework.response import Response
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

@api_view(['POST', 'OPTIONS'])
def calculate_trip(request):
    if request.method == 'OPTIONS': return Response()
    
    # قراءة المدن من الطلب
    curr_n = request.data.get('current_location')
    pick_n = request.data.get('pickup_location')
    drop_n = request.data.get('dropoff_location')

    geolocator = Nominatim(user_agent="spotter_ai_v1")

    try:
        # البحث عن الإحداثيات
        c = geolocator.geocode(curr_n)
        p = geolocator.geocode(pick_n)
        d = geolocator.geocode(drop_n)

        # حساب المسافات
        deadhead = geodesic((c.latitude, c.longitude), (p.latitude, p.longitude)).miles
        loaded = geodesic((p.latitude, p.longitude), (d.latitude, d.longitude)).miles

        return Response({
            "distance_to_pickup_miles": round(deadhead, 2),
            "trip_distance_miles": round(loaded, 2),
            "coordinates": {
                "current": {"lat": c.latitude, "lng": c.longitude},
                "pickup": {"lat": p.latitude, "lng": p.longitude},
                "dropoff": {"lat": d.latitude, "lng": d.longitude}
            }
        })
    except:
        return Response({"error": "Location not found"}, status=400)
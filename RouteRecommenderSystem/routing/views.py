from django.shortcuts import render
import googlemaps, haversine
from datetime import datetime
from .models import District, Locality, State
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def test(request):
    a = [1, 2, 3]
    return render(request, 'result.html', {'a': a})

#find closest locality using haversine
def findNearestLocality(lat, lng):
    min_dist = float("inf")
    min_locality = ''
    states = State.objects.all()
    for state in states:
        districts = District.objects.filter(state = state)
        for district in districts:
            localities = Locality.objects.filter(district = district)
            for locality in localities:
                dist = haversine.haversine(locality.lat, locality.lng, lat, lng)
                if min_dist > dist:
                    min_dist = dist
                    min_locality = locality

    return min_locality

def home(request):
    return render(request, 'map.html', )

@csrf_exempt
def result(request):
    start = request.POST.get('start')
    destination = request.POST.get('destination')
    poi_coeff = request.POST.get('poi_coeff')
    crime_coeff = request.POST.get('crime_coeff')
    traffic_coeff = request.POST.get('traffic_coeff')
    gmaps = googlemaps.Client(key='AIzaSyAtc-2ZwV_PGZaT-TxNR1YUnicbdeCNEg0')
    now = datetime.now()
    response = gmaps.directions(start,destination,mode="transit",departure_time=now,alternatives = True)

    max_weight = -float('inf')
    max_polyline = ''
    #max_path = []
    for directions_result in response:
        path = []
        weight = 0.0
        # start = nested_lookup.nested_lookup('start_location', directions_result)
        # end = nested_lookup.nested_lookup('end_location', directions_result)
        # for s in start:
        #     path.append([s['lat'], s['lng']])
        # for e in end:
        #     path.append([e['lat'], e['lng']])
        for l in directions_result['legs']:
            print "l is ", l
            for loc in l['steps']:
                print "loc is ", loc
                if 'steps' in loc:
                    for s in loc['steps']:
                        print "s is", s
                        path.append([s['start_location']['lat'], s['start_location']['lng']])
                        path.append([s['end_location']['lat'], s['end_location']['lng']])
                else:
                    path.append([loc['start_location']['lat'], loc['start_location']['lng']])
                    path.append([loc['end_location']['lat'], loc['end_location']['lng']])
        for p in path:
            l = findNearestLocality(p[0], p[1])
            weight += (float(crime_coeff)*float(l.crime_wt) + float(poi_coeff)*float(l.poi_wt) + float(traffic_coeff)*float(l.traffic_wt))

        if weight > max_weight:
            max_weight = weight
            max_polyline = directions_result['overview_polyline']['points']
            #max_path = path
    return render(request, 'result.html', {'polyline': max_polyline})
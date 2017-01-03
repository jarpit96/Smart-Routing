from django.db.migrations.topological_sort import stable_topological_sort
from django.shortcuts import render
import googlemaps, haversine
from datetime import datetime
from .models import District, Locality, State
from django.views.decorators.csrf import csrf_exempt
import pprint
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
    poi_list = request.POST.get('poiData')
    poi_list = poi_list.split(',')
    print poi_list, "--->>poi's selected"
    gmaps = googlemaps.Client(key='AIzaSyAtc-2ZwV_PGZaT-TxNR1YUnicbdeCNEg0')
    now = datetime.now()
    response = gmaps.directions(start,destination,mode="transit",departure_time=now,alternatives = True)

    max_weight = -float('inf')
    max_polyline = ''
    #max_path = []
    index = -1
    for directions_result in response:
        path = []
        weight = 0.0
        index+=1
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
            poi_weight = 0.0
            total_poi_list = []
            poi_obj = l.poi
            total_poi_list.append(poi_obj.amusement_park_wt)
            total_poi_list.append(poi_obj.art_gallery_wt)
            total_poi_list.append(poi_obj.cafe_wt)
            total_poi_list.append(poi_obj.casino_wt)
            total_poi_list.append(poi_obj.hindu_temple_wt)
            total_poi_list.append(poi_obj.zoo_wt)
            total_poi_list.append(poi_obj.spa_wt)
            total_poi_list.append(poi_obj.restaurant_wt)
            total_poi_list.append(poi_obj.museum_wt)
            total_poi_list.append(poi_obj.lodging_wt)
            for p_index in poi_list:
                poi_weight += total_poi_list[int(p_index)]
            poi_weight /= len(poi_list)
            weight += (float(crime_coeff)*float(l.crime_wt) + float(poi_coeff)*float(poi_weight) + float(traffic_coeff)*float(l.traffic_wt))

        if weight > max_weight:
            max_weight = weight
            max_index = index
            #max_path = path
    return render(request, 'plotTest_working.html', {'index': max_index, 'start': start, 'destination' : destination})


def plotTest(request):
    gmaps = googlemaps.Client(key='AIzaSyAtc-2ZwV_PGZaT-TxNR1YUnicbdeCNEg0')

    # Request directions via public transit
    now = datetime.now()

    directions_result = gmaps.directions("Rohini, Delhi, India",
                                         "CP, Delhi, India",
                                         mode="transit",
                                         departure_time=now,
                                         alternatives=True)
                                         # region="in")
    pp = pprint.PrettyPrinter(indent=4)
    #
    pp.pprint(directions_result)

    # print directions_result
    # points = []
#    for leg in directions_result[0]['legs']:
#     leg = directions_result[0]['legs'][0]
#     for ostep in leg['steps']:
#         ostep = ostep.split("',{u'distance'")
#
#         for step in ostep:
#             if 'steps' in step:
#                 for istep in step['steps']:
#                     points += googlemaps.convert.decode_polyline(istep['polyline']['points'])
#             else:
#                 points += googlemaps.convert.decode_polyline(ostep['polyline']['points'])
#     print len(points)
    # polylines = nested_lookup.nested_lookup('polyline', directions_result[0])
    # polylines2 = nested_lookup.nested_lookup('points', polylines)
    # for polyline in polylines2:
    #      points += googlemaps.convert.decode_polyline(polyline)
    #     # pass
    #print len(points)
    # encoded_polyline = googlemaps.convert.encode_polyline(points)
    # end = nested_lookup.nested_lookup('end_location', directions_result)
    # for s in start:
    #     path.append([s['lat'], s['lng']])
    # for e in end:
    #     path.append([e['lat'], e['lng']])
    # print encoded_polyline
    return render(request, 'plotTest_working.html', {'index': 1})

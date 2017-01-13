from django.db.migrations.topological_sort import stable_topological_sort
from django.shortcuts import render
import googlemaps, haversine
from datetime import datetime
from .models import District, Locality, State
from django.views.decorators.csrf import csrf_exempt
import pprint
from sets import Set
import requests
# Create your views here.

def test(request):
    a = [1, 2, 3]
    return render(request, 'result.html', {'a': a})


def get_weather(lat, lon):
    key = '26b7b7d50fc03f7adfffab8179df757b'
    r = requests.get(
        'http://api.openweathermap.org/data/2.5/weather?lat=' + str(lat) + '&lon=' + str(lon) + '&APPID=' + key)
    return r.json()

def get_weather_weight(temperature,weather_condition):
    if temperature > 25:
        temperature = 50 - temperature
    temperature /= 5
    weather_description = {"clear sky":5,"few clouds" :3 ,"scattered clouds":4, "broken clouds":0,
                           "shower rain":3, "rain":2, "thunderstorm":0, "snow":0, "mist":2}
    if weather_condition in weather_description:
        temperature = (weather_description[weather_condition]+temperature)/2

    return temperature

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

    poi_types = {'Amusement Park': 0, 'Art Gallery': 1, 'Cafe': 2, 'Casino': 3, 'Hindu Temple':4, 'Zoo':5, 'Spa':6, 'Restaurant':7,
                 'Museum':8, 'Lodging':9}
    return render(request, 'home.html', {'poiList': poi_types})


def start(request):
    return render(request, 'startPage.html',)

@csrf_exempt
def result(request):
    poi_types = ['amusement_park', 'art_gallery', 'cafe', 'casino', 'hindu_temple', 'zoo', 'spa', 'restaurant',
                 'museum', 'lodging']

    start = request.POST.get('start')
    destination = request.POST.get('destination')
    poi_coeff = request.POST.get('poi_coeff')
    crime_coeff = request.POST.get('crime_coeff')
    traffic_coeff = request.POST.get('traffic_coeff')
    weather_coeff = request.POST.get('weather_coeff')
    poi_list = request.POST.get('poiPriority')
    poi_list = poi_list.split(',')
    print poi_list, "--->>poi's selected"
    gmaps = googlemaps.Client(key='AIzaSyDmT6F29WJ9M-viNlrMzRpRPtdseHTCfoA')
    now = datetime.now()
    response = gmaps.directions(start,destination,mode="driving",departure_time=now,alternatives = True)

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
            # print "l is ", l
            for loc in l['steps']:
                # print "loc is ", loc
                if 'steps' in loc:
                    for s in loc['steps']:
                        # print "s is", s
                        path.append([s['start_location']['lat'], s['start_location']['lng']])
                        path.append([s['end_location']['lat'], s['end_location']['lng']])
                else:
                    path.append([loc['start_location']['lat'], loc['start_location']['lng']])
                    path.append([loc['end_location']['lat'], loc['end_location']['lng']])
        pois = []
        locs = Set([])
        for p in path:
            l = findNearestLocality(p[0], p[1])
            print l.name
            locs.add(l)
        for l in locs:
            print "Reached 1"
            for poi_index in poi_list:
                print "Reached 2"
                results = gmaps.places_nearby(location=[l.lat, l.lng], radius=2000, type=poi_types[int(poi_index)])['results']
                print "Len: ", len(results)
                if len(results) != 0:
                    print "Reached 3"
                    max_rating = 0
                    max_poi = {}
                    for pid in results:
                        print "Reached 4"
                        if 'rating' in pid:
                            print "Reached 5"
                            if int(pid['rating']) > max_rating:
                                print "Reached 6"
                                max_rating = pid['rating']
                                max_poi = pid['geometry']['location']
                            pois.append(max_poi)
                            print "Updated POIS", pois
                            break
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

            weather = get_weather(l.lat, l.lng)
            temp = weather['main']['temp']-273.15
            description = str(weather['weather'][0]['description'])
            weather_weight = get_weather_weight(temp, description)
            weight += (float(crime_coeff)*float(l.crime_wt) + float(poi_coeff)*float(poi_weight) + float(traffic_coeff)*float(l.traffic_wt)) + float(weather_coeff)*float(weather_weight)

        if weight > max_weight:
            max_weight = weight
            max_index = index
            max_pois = pois
            #max_path = path
    print "Max_POI", max_pois
    return render(request, 'result.html', {'index': max_index, 'start': start, 'destination' : destination, 'wayPoints': list(max_pois)})


def plotTest(request):
    gmaps = googlemaps.Client(key='AIzaSyAtc-2ZwV_PGZaT-TxNR1YUnicbdeCNEg0')

    # Request directions via public transit
    now = datetime.now()

    directions_result = gmaps.directions("Rohini, Delhi, India",
                                         "CP, Delhi, India",
                                         mode="driving",
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
    return render(request, 'result.html', {'index': 1})

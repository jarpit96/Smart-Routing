import googlemaps
from datetime import datetime
import json
import pprint

gmaps = googlemaps.Client(key='AIzaSyAtc-2ZwV_PGZaT-TxNR1YUnicbdeCNEg0')

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("Delhi, India",
                                     "Chennai, India",
                                     mode="transit",
                                     departure_time=now)

# print directions_result

pp = pprint.PrettyPrinter(indent=4)

pp.pprint(directions_result[0])

for l in directions_result[0]['legs']:
    for loc in l['steps']:
        print gmaps.reverse_geocode((loc['start_location']['lat'], loc['start_location']['lng']))[0]['formatted_address']
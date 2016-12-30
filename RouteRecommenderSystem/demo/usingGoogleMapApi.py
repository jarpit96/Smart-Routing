import googlemaps
from datetime import datetime
import json
import pprint

gmaps = googlemaps.Client(key='AIzaSyAtc-2ZwV_PGZaT-TxNR1YUnicbdeCNEg0')

# Request directions via public transit
now = datetime.now()

print gmaps.geocode('AIIMS')

# directions_result = gmaps.directions("Rohini, Delhi, India",
#                                      "CP, Delhi, India",
#                                      mode="transit",
#                                      departure_time=now,
#                                      alternatives = True,
#                                      region="in")
#
# # print directions_result
#
# pp = pprint.PrettyPrinter(indent=4)
#
# pp.pprint(directions_result)

# for l in directions_result[0]['legs']:
#     for loc in l['steps']:
#         if 'steps' in loc:
#             for s in loc['steps']:
#                 print s['start_location']
#         else:
#             print loc['start_location']
#         print gmaps.reverse_geocode((loc['start_location']['lat'], loc['start_location']['lng']))[0]['formatted_address']
#
#         print loc['start_location']
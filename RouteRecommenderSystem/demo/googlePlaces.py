import googlemaps
import pprint

pp = pprint.PrettyPrinter(indent=4)

gmaps = googlemaps.Client(key='AIzaSyAtc-2ZwV_PGZaT-TxNR1YUnicbdeCNEg0')

loc = {u'lat': 28.7039053, u'lng': 77.10255529999999}

result = gmaps.places_nearby(location=loc, radius = 2000, type='cafe')

pp.pprint (result)
from pprint import pprint
import requests

lat = '19.01'
lon = '72.85'
loc = 'NorthDelhi,Delhi,India'
key = '26b7b7d50fc03f7adfffab8179df757b'

def getWeather(lat, lon):
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?lat=' + lat + '&lon=' + lon + '&APPID=' + key)
    pprint(r.json())

def getWeather(loc):
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q=' + loc + '&APPID=' + key)
    pprint(r.json())

getWeather(loc)
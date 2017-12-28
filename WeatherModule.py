# -*- coding: utf-8 -*-

from urllib.request import urlopen
import json
key = '7047852fabf9ea82'

def getCurWeatInfo():
    url = 'http://api.wunderground.com/api/' + key + '/geolookup/conditions/q/UK/London.json'
    currentWeat = parseJsonFromURL(url)
    weatStat = currentWeat['current_observation']['weather']
    temperature = str(currentWeat['current_observation']['temp_c']) + '°C'
    # feelLikeTemp = 'Feels Like %sÂ°C' %(parsed_json['current_observation']['feelslike_c'])
    return weatStat, temperature

def getForecast():
    url = 'http://api.wunderground.com/api/' + key + '/geolookup/forecast10day/q/UK/London.json'
    forecast = parseJsonFromURL(url)['forecast']['simpleforecast']['forecastday']
    return forecast

def getIcon(weatStat):
    iconPath = 'WeatherIcons/unknown.pgm'
    possibleStat= {
        'drizzle':'drizzle.pgm',
        'rain':'rain.pgm',
        'snow':'snow.pgm',
        'ice':'snow.pgm',
        'hail':'hail.pgm',
        'mist':'mistFog.pgm',
        'fog':'mistFog.pgm',
        'thunderstorm':'thunder.pgm',
        'overcast':'overcast.pgm',
        'clear':'clear.pgm',
        'cloudy':'cloudy.pgm'
    }
    for status in possibleStat:
        if status in weatStat.lower():
            iconPath = 'WeatherIcons/' + possibleStat[status]
    return iconPath

def parseJsonFromURL(url):
    with urlopen(url) as f:
        json_string = f.read()
        return json.loads(json_string.decode())

if __name__ == '__main__':
    print(getIcon('Thunderstorm and Rain'))
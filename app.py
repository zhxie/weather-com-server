from flask import Flask, request
import json
import requests

app = Flask(__name__)

WEATHER_COM_COD_URL = 'https://api.weather.com/v3/wx/observations/current'
API_KEY = ''

SUCCESS = 0
ERR_INTERNAL_ERROR = -1
ERR_INVALID_PARAM = -2

CLEAR = 0
PARTLY_CLOUDY = 1
MOSTLY_CLOUDY = 2
CLOUDY = 3
RAINY = 4
SNOWY = 5

CLOUD_COVER_PHRASES = {
    'Clear': CLEAR,
    'Partly Cloudy': PARTLY_CLOUDY,
    'Mostly Cloudy': MOSTLY_CLOUDY,
    'Cloudy': CLOUDY
}


def create_app():
    with open('config.json') as f:
        data = json.load(f)
        API_KEY = data['api_key']

    @app.route('/')
    def weather():
        lat = request.args.get('lat', -1, type=float)
        lon = request.args.get('lon', -1, type=float)
        if lat < -90 or lat > 90 or lon < -180 or lon > 180:
            return {
                'status': ERR_INVALID_PARAM
            }
        else:
            try:
                content = requests.get(WEATHER_COM_COD_URL, params={
                    'geocode': '{},{}'.format(lat, lon),
                    'units': 's',
                    'language': 'en-US',
                    'format': 'json',
                    'apiKey': API_KEY
                }).json()

                rain = content['precip1Hour']
                snow = content['snow1Hour']

                if snow > rain:
                    return {
                        'status': SUCCESS,
                        'result': SNOWY
                    }
                elif rain >= snow and rain > 0:
                    return {
                        'status': SUCCESS,
                        'result': RAINY
                    }
                else:
                    return {
                        'status': SUCCESS,
                        'result': CLOUD_COVER_PHRASES[content['cloudCoverPhrase']]
                    }

            except:
                return {
                    'status': ERR_INTERNAL_ERROR
                }


create_app()

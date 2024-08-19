import os
import requests
import logging
from flask import Flask, jsonify, request
from dotenv import load_dotenv


# load env
load_dotenv()

# init Flask app
app = Flask(__name__)

# set up logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@app.route('/weather', methods=['GET'])
def get_weather():
    api_key = os.getenv('OPEN_WEATHER_MAP_API_KEY')
    if not api_key:
        return jsonify({'status': 'error', 'message': 'API key is missing'}), 500
    
    # get params
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    units = request.args.get('units')

    # validate params
    if not lat or not validate_latitude(lat):
        return jsonify({'status': 'error', 'message': 'Invalid latitude. Must be a number between -90 and 90'}), 400
    
    if not lon or not validate_longtitude(lon):
        return jsonify({'status': 'error', 'message': 'Invalid longitude. Must be a number between -180 and 180'}), 400

    if not units or not validate_units(units):
        return jsonify({'status': 'error', 'message': 'Invalid units. Must be one of: standard, metrics, or imperial'}), 400


    try: 
        # get weather data
        weather_data = get_weather_data(lat, lon, units, api_key)

        filtered_data = {
            'temperature': weather_data['main']['temp'],
            'humidity': weather_data['main']['humidity'],
            'wind speed': weather_data['wind']['speed']
        }

        return jsonify({'status': 'success', 'data': filtered_data})
    except Exception as e:
        logger.error(f'Error fetching weather data: {e}')

        return jsonify({'status': 'error', 'message': 'Failed to retrieve weather data'}), 500


def get_weather_data(lat, lon, units, api_key):
    url = os.getenv('OPEN_WEATHER_MAP_URL')
    if not url:
        url = 'https://api.openweathermap.org/data/2.5/weather'

    params = {
        'lat': lat,
        'lon': lon,
        'units': units,
        'appid': api_key
    }

    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as http_err:
        logging.error(f'HTTP error occured: {http_err}')
        raise
    except requests.exceptions.RequestException as req_err:
        logging.error(f'Request error occured: {req_err}')
        raise


def validate_latitude(lat):
    try:
        lat = float(lat)
        return -90 <= lat <= 90
    except ValueError:
        return False

def validate_longtitude(lon):
    try:
        lon = float(lon)
        return -180 <= lon <= 180
    except ValueError:
        return False
    

def validate_units(units):
    valid_units = ['standard', 'metrics', 'imperial']
    return units in valid_units
    

if __name__ == '__main__':
    app.run(debug=True)

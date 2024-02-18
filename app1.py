from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_hospitals', methods=['POST'])
def get_hospitals():
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    
    URL = "https://discover.search.hereapi.com/v1/discover"
    api_key = 'gyOHH09M0UHJcE-3cIZEoRyyKWlyvJNr6J_kd7gdIkk' # Acquire from developer.here.com
    query = 'hospital'
    limit = 5

    PARAMS = {
        'apikey': api_key,
        'q': query,
        'limit': limit,
        'at': f'{latitude},{longitude}'
    }

    r = requests.get(url=URL, params=PARAMS)
    data = r.json()

    hospitals = []
    for item in data.get('items', []):
        hospital = {
            'name': item.get('title', 'N/A'),
            'address': item['address'].get('label', 'N/A'),
            'latitude': item['position'].get('lat', 'N/A'),
            'longitude': item['position'].get('lng', 'N/A'),
            'contact': item.get('contacts', [{}])[0].get('phone', 'N/A')
        }
        hospitals.append(hospital)

    return render_template('hospitals.html', hospitals=hospitals)

if __name__ == '__main__':
    app.run(debug=True)

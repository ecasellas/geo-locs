from flask import Flask, render_template, request
from flask_cors import CORS
from pyproj import Proj, Transformer
import json
import random
from math import exp


app = Flask(__name__)
CORS(app)


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/navigation')
def navigation():
    return render_template('navigation.html')

@app.route('/instructions')
def instructions():
    return render_template('instructions.html')

@app.route('/catalan-peaks')
def catalan_peaks():
    return render_template('catalan_peaks.html')

@app.route('/check-distance/<lon>/<lat>/<peak>', methods=['GET', 'POST'])
def check_distance(lon, lat, peak):

    xy = Transformer.from_crs(4326, 25831).transform(float(lat), float(lon))

    if peak[0:2] == 'catPeaks':
        loc_file = './data/catalan_peaks_100.json'
    else:
        loc_file = './data/catalan_peaks_100.json'
    
    with open(loc_file, 'r') as f:
        locs = json.load(f)
        f.close()

    x_loc = locs[peak]['utm_x']
    y_loc = locs[peak]['utm_y']

    lonlat_loc = Transformer.from_crs(25831, 4326).transform(x_loc, y_loc)

    d_x = xy[0] - x_loc
    d_y = xy[1] - y_loc

    dist = round((d_x**2 + d_y**2)**(1/2)/1000, 1)

    points = round((exp(-3*dist/100)) * 1000, 0)

    return {'distance': dist, 'points': points,
            'x_loc': lonlat_loc[1], 'y_loc': lonlat_loc[0],
            'x': float(lon), 'y': float(lat)}

@app.route('/load-locs/<option>/<num>', methods=['GET', 'POST'])
def load_locs(option, num):
    if option == 'cat':
        loc_file = './data/catalan_peaks_100.json'
    else:
        loc_file = './data/catalan_peaks_100.json'

    with open(loc_file, 'r') as f:
        locs = json.load(f)
        f.close()
    
    keys = list(locs.keys())
    r_keys = random.sample(range(0, len(keys)), int(num))

    r_locs = []
    for key in r_keys:
        locs[keys[key]]['id'] = keys[key]
        r_locs.append(locs[keys[key]])

    return {'locs': r_locs}


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Origin, X-Requested-With, Content-Type, Accept')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET, PUT, POST, DELETE, OPTIONS')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
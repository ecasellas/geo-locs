import json


with open('./data/46465_100 Cims/100 Cims.geojson', 'r') as f:
    data = json.load(f)
    f.close()

out = {}
for i in range(len(data['features'])):
    peak = data['features'][i]
    peak_id = 'cat' + str(i)
    
    out[peak_id] = {'name': peak['properties']['nom'],
                    'altitude': peak['properties']['cota'],
                    'utm_x': peak['geometry']['coordinates'][0],
                    'utm_y': peak['geometry']['coordinates'][1]}

with open('./data/catalan_peaks_100.json', 'w') as f:
    json.dump(out, f)
    f.close()
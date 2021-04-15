import json
import pandas as pd
from pyproj import Proj, Transformer

# Catalan peaks
'''
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
'''
#

# Badalona peaks
turons = pd.read_csv('/home/ecm/Downloads/turons_bdn.csv')
colls = pd.read_csv('/home/ecm/Downloads/colls_bdn.csv')

data = turons.append(colls)

out = {}
for i in range(len(data['NOM'])):
    peak = data.iloc[i]
    peak_id = 'bdn' + str(i)

    lonlat_loc = Transformer.from_crs(4326, 25831).transform(float(peak['LATITUD']), float(peak['LONGITUD']))

    out[peak_id] = {'name': peak['NOM'],
                    'altitude': int(peak['COTA']),
                    'utm_x': float(lonlat_loc[0]),
                    'utm_y': float(lonlat_loc[1])}

with open('./data/bdn_peaks_40.json', 'w') as f:
    json.dump(out, f)
    f.close()


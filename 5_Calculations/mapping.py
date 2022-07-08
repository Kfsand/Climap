#Functions useful for coordinate conversion and geojson structuring
from bng_latlon import OSGB36toWGS84
import numpy as np
import pandas as pd
import json


def ReuCoord (xcoord,ycoord):
    print(type(xcoord))
    print(type(ycoord))
    coordarray=np.stack(xcoord, ycoord)
    return coordarray


def bulkOSGB36toWGS84(xBNG, yBNG):

    latlonarray=[]

    for i in xBNG:
        for j in yBNG:
            latlonarray.append(OSGB36toWGS84(i, j))

    return latlonarray


def CoordtoGeojson(latlonarray,fname='dataset.json'):
    'Note: convert data to geojson and write in file'

    df = pd.DataFrame(latlonarray, columns=['latitude','longitude'])


    def df_to_geojson(df, properties, lat='latitude', lon='longitude'):
        geojson = {'type':'FeatureCollection', 'features':[]}
        for _, row in df.iterrows():
            feature = {'type':'Feature',
                    'properties':{},
                    'geometry':{'type':'Point',
                                'coordinates':[]}}
            feature['geometry']['coordinates'] = [row[lon],row[lat]]
            for prop in properties:
                feature['properties'][prop] = row[prop]
            geojson['features'].append(feature)
        return geojson


    cols = ['latitude','longitude']
    geojson = df_to_geojson(df, cols)


    output_filename = '../6_Results/data/' +fname
    with open(output_filename, 'w') as output_file:
        json.dump(geojson, output_file, indent=2)
    
    pass


#Functions useful for coordinate conversion and geojson structuring
from bng_latlon import OSGB36toWGS84
import numpy as np
import pandas as pd
import json

def bulkOSGB36toWGS84(xBNG, yBNG):

    latlonarray=[]

    for i in xBNG:
        for j in yBNG:
            latlonarray.append(OSGB36toWGS84(i, j))

    return latlonarray

def df_to_geojson(df, properties, lat='latitude', lon='longitude'):
    #initialising geojson object
    geojson = {'type':'FeatureCollection', 'features':[]}

    #Iterating through dataframe, 
    # _ stores index, row stores data of the row as a Series
    for _, row in df.iterrows():
        #initialising feature in geojson's colelction
        feature = {'type':'Feature',
                    'properties':{},
                    'geometry':{'type':'Point',
                                'coordinates':[]}}

        #editing feature's coordinates using dataframe's columns titled
        # with lat and lon
        feature['geometry']['coordinates'] = [row[lon],row[lat]]

        #loop over properties string list
        for prop in properties:
            #editing feature's property, "prop" is the title, row[prop] the value assigned
            #assumed df has a column titled with prop
            feature['properties'][prop] = row[prop]
        geojson['features'].append(feature)

    return geojson

def PointstoGeojson(latlonarray,foldername="new",fname='dataset.geojson'):
    'Note: convert data to geojson and write in file'

    df = pd.DataFrame(latlonarray, columns=['latitude','longitude'])
    cols = ['latitude','longitude']
    geojson = df_to_geojson(df, cols)


    output_filename = '../6_Results/data/'+foldername+"/" +fname
    with open(output_filename, 'w') as output_file:
        json.dump(geojson, output_file, indent=2)

def buildsqrBNG(xcoord,ycoord):
    #returns array of coordinates (lat long) defining grid squares

    #coordinate arrays to be passed in BNG coordinates
    x=xcoord
    y=ycoord

    squares_array=[]
    
    #n x m cordinates give (n-1) x (m-1) squares
    for i in range(len(xcoord)-1):
        for j in range(len(ycoord)-1):
        
            x1=x[i]
            x2=x[(i+1)%len(xcoord)]
            y1=y[j]
            y2=y[(j+1)%len(ycoord)]

            a=OSGB36toWGS84(x1, y1)
            b=OSGB36toWGS84(x2, y1)
            c=OSGB36toWGS84(x2, y2)
            d=OSGB36toWGS84(x1,y2)

            squares_array.append([a,b,c,d])
    return squares_array


def PolystoGeojson(squares_array,over_array,bloc=0,foldername="new"):

    geojson = {'type':'FeatureCollection', 'features':[]}
    
    #slice data array to select correct time period (usually one of the 5 x 20y time periods)
    slice_over=over_array[bloc,:,:]
    flat_over=slice_over.flatten('F')
    df = pd.DataFrame(flat_over, columns=['excess days'])
    prop='excess days'
    
    for i in range(len(squares_array)):
    
        a=squares_array[i][0]
        b=squares_array[i][1]
        c=squares_array[i][2]
        d=squares_array[i][3]

        feature = {'type':'Feature',
                        "id":{},
                        'properties':{},
                        'geometry':{'type':'Polygon',
                                    'coordinates':[]}}


        feature["id"]=str(i+1)
        feature['properties'][prop] = df.loc[i,prop]                         
        feature['geometry']['coordinates'] = [[[a[1],a[0]],
                                              [b[1],b[0]],
                                              [c[1],c[0]],
                                              [d[1],d[0]],
                                              [a[1],a[0]]]]
           

        geojson['features'].append(feature)

    output_filename = '../6_Results/data/'+foldername+"/"+str(bloc)+'_squares.geojson'
    with open(output_filename, 'w') as output_file:
        json.dump(geojson, output_file, indent=2)
    
    return flat_over
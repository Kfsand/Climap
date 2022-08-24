#Functions useful for coordinate conversion and geojson structuring
from bng_latlon import OSGB36toWGS84
import numpy as np
import pandas as pd
import json
from Classes import DataO
from Classes import GC
import os

class MapObject:

    ##### CLASS ATTRIBUTES ####
    # MAPID : (string)
    # DLIST : (list of DataObjects)
    # DNAMES : (list of strings) DataObject names contained in dlist
    # RESPATH : (string) path for result saving
    # SQRCOORDS : (?) lat lon coordinates for squares mapping
    # GEOJSON : (dict) data in geojson format

    ######### INIT #########
    # 1. initialising attributes
    # 2. creating coordinates array for map squares
    # 3. creating gepjson dictionnary object with coordinates

    def __init__(self,MapID,dataobject,respath):

        ######### 1 ########## - initialising attributes
        self.MapID=MapID
        self.dlist=[dataobject]
        self.dnames= [dataobject.title]
        self.respath=respath

        ######### 2 ########## - creating coordinates array for map squares
        self.sqrcoords=self.buildsqrBNG(dataobject.xcoord,dataobject.ycoord)

        ######### 3 ########## - creating gepjson dictionnary object and intialising features with square coordinates
        self.sqrcoords=self.geojson_coords()
        
    
    def addDataObject(self,dataobject):
            self.dlist.append(dataobject)
            self.dnames.append(dataobject.varname)
    
    def bulkOSGB36toWGS84(xBNG, yBNG):

        latlonarray=[]

        for i in xBNG:
            for j in yBNG:
                latlonarray.append(OSGB36toWGS84(i, j))

        return latlonarray
    
    def buildsqrBNG(self,xcoord,ycoord):

        #returns array of coordinates (lat long) defining grid squares

        #coordinate arrays to be passed in BNG coordinates
        assert (xcoord.size,ycoord.size)==(153,244), "coordinate arrays passed from object are not correct size"
        x=xcoord
        y=ycoord

        squares_array=[]
        
        #n x m cordinates give (n-1) x (m-1) squares
        for i in range(len(x)-1):
            for j in range(len(y)-1):
            
                x1=x[i]
                x2=x[(i+1)%len(x)]
                y1=y[j]
                y2=y[(j+1)%len(y)]

                a=OSGB36toWGS84(x1, y1)
                b=OSGB36toWGS84(x2, y1)
                c=OSGB36toWGS84(x2, y2)
                d=OSGB36toWGS84(x1,y2)

                squares_array.append([a,b,c,d])
        return squares_array

    def geojson_coords(self):
        #creates geojson dictionnary defining map squares as polygons with coordinates

        self.geojson = {'type':'FeatureCollection', 'features':[]}

        for i in range(len(self.sqrcoords)):
    
            a=self.sqrcoords[i][0]
            b=self.sqrcoords[i][1]
            c=self.sqrcoords[i][2]
            d=self.sqrcoords[i][3]

            feature = {'type':'Feature',
                            "id":{},
                            'properties':{},
                            'geometry':{'type':'Polygon',
                                        'coordinates':[]}}


            feature["id"]=str(i+1)                       
            feature['geometry']['coordinates'] = [[[a[1],a[0]],
                                                [b[1],b[0]],
                                                [c[1],c[0]],
                                                [d[1],d[0]],
                                                [a[1],a[0]]]]
            
            self.geojson["features"].append(feature)
    
    def build_props(self):
        for variable in self.dlist:
            self.geojson_props(variable.title,variable.fcounter_array)

    def geojson_props(self,vartitle,flat_prop_array):
        ##add property to geojson features, expect title of property 
        # and flat property array aligned with features

        i=0
        for feature in self.geojson['features']:
            feature["properties"][vartitle]=int(flat_prop_array[i])
            #feature["properties"][vartitle+" - excess days"]=i
            i+=1

    def geojson_write(self,index):
        output_filename = self.respath+"/"+str(index)+'_squares.geojson'
        #creating result directory
        if not os.path.exists(self.respath):
            os.mkdir(self.respath)
        with open(output_filename, 'w') as output_file:
            json.dump(self.geojson, output_file, indent=2)



class MapObject_daily:

    ##### CLASS ATTRIBUTES ####
    # MAPID : (string)
    # RESPATH : (string) path for result saving
    # SQRCOORDS : (?) lat lon coordinates for squares mapping
    # GEOJSON : (dict) data in geojson format

    ######### INIT #########
    # 1. initialising attributes
    # 2. creating coordinates array for map squares
    # 3. creating gepjson dictionnary object with coordinates

    def __init__(self,MapID,respath,coord_dict,geojsontitle='test'):

        ######### 1 ########## - initialising attributes
        self.MapID=MapID
        self.respath=respath

        ######### 2 ########## - creating coordinates array for map squares
        self.sqrcoords=self.buildsqrBNG(coord_dict)

        ######### 3 ########## - creating gepjson dictionnary object and intialising features with square coordinates
        self.geojson_coords()

        self.geojson_write(geojsontitle)
        
    
    def buildsqrBNG(self,coord_dict):

        #returns array of coordinates (lat long) defining grid squares

        #coordinate arrays to be passed in BNG coordinates
        assert (len(coord_dict))==(75), "coordinate arrays passed from object are not correct size"
        squares_array=[]
        
        for key in coord_dict:


            x=coord_dict[key][0]
            y=coord_dict[key][1]

            x1=x-30000
            x2=x+30000
            y1=y-30000
            y2=y+30000

            a=OSGB36toWGS84(x1, y1)
            b=OSGB36toWGS84(x2, y1)
            c=OSGB36toWGS84(x2, y2)
            d=OSGB36toWGS84(x1,y2)

            squares_array.append([a,b,c,d])
        return squares_array

    def geojson_coords(self):
        #creates geojson dictionnary defining map squares as polygons with coordinates

        self.geojson = {'type':'FeatureCollection', 'features':[]}

        for i in range(len(self.sqrcoords)):
    
            a=self.sqrcoords[i][0]
            b=self.sqrcoords[i][1]
            c=self.sqrcoords[i][2]
            d=self.sqrcoords[i][3]

            feature = {'type':'Feature',
                            "id":{},
                            'properties':{},
                            'geometry':{'type':'Polygon',
                                        'coordinates':[]}}


            feature["id"]=str(i+1)                       
            feature['geometry']['coordinates'] = [[[a[1],a[0]],
                                                [b[1],b[0]],
                                                [c[1],c[0]],
                                                [d[1],d[0]],
                                                [a[1],a[0]]]]
            
            self.geojson["features"].append(feature)

    def geojson_props(self,vartitle,flat_prop_array):
        ##add property to geojson features, expect title of property 
        # and flat property array aligned with features

        i=0
        for feature in self.geojson['features']:
            feature["properties"][vartitle]=int(flat_prop_array[i])
            i+=1
        

    def geojson_write(self,index):
        output_filename = self.respath+"/"+str(index)+'_squares.geojson'
        #creating result directory
        if not os.path.exists(self.respath):
            os.mkdir(self.respath)
        with open(output_filename, 'w') as output_file:
            json.dump(self.geojson, output_file, indent=2)



    
    

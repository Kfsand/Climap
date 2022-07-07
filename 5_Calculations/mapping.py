#Functions useful for coordinate conversion and geojson structuring
from bng_latlon import OSGB36toWGS84
import numpy as np


def ReuCoord (xcoord,ycoord):
    print(type(xcoord))
    print(type(ycoord))
    coordarray=np.stack(xcoord, ycoord)
    return coordarray


def bulkOSGB36toWGS84(xBNG, yBNG):

    latlonarray=[]

    for i in xBNG:
        for j in yBNG:
            #print(OSGB36toWGS84(i, j))
            latlonarray.append(OSGB36toWGS84(i, j))

    return latlonarray

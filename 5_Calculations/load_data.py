#import necessary libraries
import numpy as np
import pandas as pd

import csv
import os

def loadnp(path="../3_Raw_Data/V2",rows_block=25,rows_data=23):
    # create list of files names to open, every .csv file in directory
    list_file=[f for f in os.listdir(path) if ".csv" in f]
    #initialising 4D array storing all values
    array4D=[]

    #list of column names, needed to force correct shape of df
    'NOTE: change range to nm of x columns'
    col_names=["x"+str(i) for i in range(15)]

    #opening and reading each consecutive file
    for f in list_file:
        df = pd.read_csv(os.path.join(path,f),skiprows=14, names=col_names)
        #initialising 3D array storing values of each file
        array3D=[]

        'NOTE: change range to nb blocks=nbrowstotal/bn rows block'
        rows_block=rows_block
        rows_data=rows_data

        for i in range(935):
            idx_1 = rows_data*i+i*2+2
            idx_2 = rows_data*(i+1)+2*(i)+2
            array3D.append(df.iloc[idx_1:idx_2, 1:].to_numpy())
        
        array3D=np.stack(array3D)
        array4D.append(array3D)
    array4D=np.stack(array4D)
    #si tu veux pas un array 3d
    #(exemple pour exporter en csv) alors np.vstack pour tout mettre à la suite


    #intitialising common coordinate vectors from last df read
    [xcoord, ycoord]=[df.iloc[1,1:].map(lambda x : int(float(x)) ).to_numpy(),df.iloc[2:24,0].map(lambda x : int(float(x)) ).to_numpy()]
    return [xcoord, ycoord, array4D]

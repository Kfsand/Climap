#import necessary libraries
import numpy as np
import pandas as pd

import csv
import os

def load(path="../3_Raw_Data/V2"):
    # create list of files names to open, every .csv file in directory
    list_file=[f for f in os.listdir(path) if ".csv" in f]
    #initialising 4D array storing all values
    array4D=[]

    #list of column names, needed to force correct shape of df
    col_names=["x"+str(i) for i in range(14)]

    #opening and reading each consecutive file
    for f in list_file:
        df = pd.read_csv(os.path.join(path,f),skiprows=14, names=col_names)
        #initialising 3D array storing values of each file
        array3D=[]


        for i in range(1199):
            idx_1 = 22*i+i*2+2
            idx_2 = 22*(i+1)+2*(i)+2
            array3D.append(df.iloc[idx_1:idx_2, 1:].to_numpy())
        
        array3D=np.stack(array3D)
        array4D.append(array3D)
    array4D=np.stack(array4D)
    #si tu veux pas un array 3d
    #(exemple pour exporter en csv) alors np.vstack pour tout mettre à la suite


    #intitialising common coordinate vectors from last df read
    [xcoord, ycoord]=[df.iloc[1,1:].to_numpy(),df.iloc[2:24,0].to_numpy()]
    'NOTE:non functional coordinate conversion to int: remained floats'
    #[xcoord, ycoord]=[df.iloc[1,1:].to_numpy(dtype=np.int32),df.iloc[2:24,0].to_numpy(dtype=np.int32)]
    return [xcoord, ycoord, array4D]

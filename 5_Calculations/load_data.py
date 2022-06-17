# %% codecell
import numpy as np
import pandas as pd

import csv
import os
# %% codecell
print(os.listdir(os.getcwd()))
# %% codecell
#iterating over entire raw data directory
list_file=[f for f in os.listdir("./3_Raw_Data/V1") if ".csv" in f]
print(list_file)

for f in list_file:
    print(os.path.join("./3_Raw_Data/V1/",f))
    df = pd.read_csv(os.path.join("./3_Raw_Data/V1/",f),skiprows=14)
# reading the CSV file
#df = pd.read_csv('./3_Raw_Data/V1/subset_2022-06-07T09-05-05_ACCESS1-3-r1i1p1.csv',skiprows=14)

#slicing to keep only values without xy coordinates (1st column and row)
#cleaning intermediary rows

[xcoord, ycoord]=[df.iloc[2:24,0].to_numpy(dtype=np.int32),df.iloc[1,1:].to_numpy(dtype=np.int32)]
#print(xcoord)
#print(ycoord)
df=df.iloc[:,1:]
array3D = []

for i in range(len(df)/24):
    idx_1 = 22*i+i*2+2
    idx_2 = 22*(i+1)+2*(i)+2
    array3D.append(df.iloc[idx_1:idx_2, :].to_numpy())

array3D=np.stack(array3D)
print(array3D)

#si tu veux pas un array 3d de merde
#(exemple pour exporter en csv) alors np.vstack pour tout mettre à la suite

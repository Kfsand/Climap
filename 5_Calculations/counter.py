import numpy as np

#function meant to count number of occurances of variable exceeding given threshold in a specific timerange


def var_counter(array3D,threshold=6,periodiser=20):

    exc_array=islarger(array3D,threshold)
    counter=np.empty((20,22,13))

    for i in range(3):
        idx_1 = periodiser*i
        idx_2 = periodiser*(i+1)
        np.add(counter,exc_array[idx_1:idx_2,:,:].astype(int))

    return counter


    

def islarger (array3D, threshold):

    #returns boolean matrix of indexes meeting condition

    threshold=threshold
    islarger=array3D>=threshold
  
    return islarger


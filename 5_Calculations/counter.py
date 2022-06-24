import numpy as np
import math


def var_counter(array3D,threshold=9,periodiser=20):

    #function takes in an array, a theshold and a year period -
    # returns aryay of ints = nb of months the values 
    # in the argument array exceeded the threshold during the specified time period.

    d1=np.size(array3D,0)
    d2=np.size(array3D,1)
    d3=np.size(array3D,2)

    nyears=periodiser
    nmonths=12*nyears

    #computing bool array of values exceeding threshold (=>)
    exc_array=islarger(array3D,threshold)
   
   #initialising return array
    sum_array=np.empty((math.ceil(d1/nmonths),d2,d3))

    for i in range(math.ceil(d1/nmonths)):
        
        #slicing appropriate time period from bool array
        idx_1 = nmonths*i
        idx_2 = nmonths*(i+1)
        slice=exc_array[idx_1:idx_2,:,:].astype(int)

        #sum of bool as ints within selected time period
        sum_slice=np.sum(slice,axis=0, dtype=np.int32)
        
        sum_array[i,:,:]=sum_slice
       
    return sum_array



def islarger (array3D, threshold):

    #returns boolean matrix of indexes meeting condition

    threshold=threshold
    islarger=array3D>=threshold
  
    return islarger


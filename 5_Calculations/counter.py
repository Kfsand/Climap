import numpy as np

#function meant to count number of occurances of variable exceeding given threshold in a specific timerange


def var_counter(array3D,threshold=6,periodiser=20):

    exc_array=islarger(array3D,threshold)
    counter=np.empty((12*periodiser,np.size(array3D,1),np.size(array3D,2)))
    print(counter.shape)

    for i in range(5):
        #1199//(periodiser*12)
        print(i)
        zeros=np.zeros(counter.shape)
        idx_1 = periodiser*12*i
        idx_2 = periodiser*12*(i+1)
        slice=exc_array[idx_1:idx_2,:,:]

        if counter.shape== slice.shape:
            print(slice.shape)
            np.add(counter,slice.astype(int))
            
        else:
            'TODO: fix last iteration'
            continue
            resized=exc_array[idx_1:idx_2,:,:].resize(counter.shape)
            print(resized.shape)
            np.add(counter,resized.astype(int))
        

    return counter


    

def islarger (array3D, threshold):

    #returns boolean matrix of indexes meeting condition

    threshold=threshold
    islarger=array3D>=threshold
  
    return islarger


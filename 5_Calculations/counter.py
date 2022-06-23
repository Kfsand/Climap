import numpy as np

#function meant to count number of occurances of variable exceeding given threshold in a specific timerange


def var_counter(array3D,threshold=6,periodiser=20):

    exc_array=islarger(array3D,threshold)
    counter=np.zeros((12*periodiser,np.size(array3D,1),np.size(array3D,2)))

    for i in range(5):
        'TODO: set range according to shape and chosen periosider'
        #1199//(periodiser*12)
        zeros=np.zeros(counter.shape)
        idx_1 = periodiser*12*i
        idx_2 = periodiser*12*(i+1)
        slice=exc_array[idx_1:idx_2,:,:].astype(int)
       

        if counter.shape== slice.shape:
            np.add(counter,slice,out=counter)
            
        else:
            'TODO: fix last iteration'
            'compter la diff sur le bon axe, créer un array de 0, ajouter avec .stack'
            print(resized.shape)
            np.add(counter,resized,out=counter)
        

        counter=counter.astype(int)

    return counter

    

def islarger (array3D, threshold):

    #returns boolean matrix of indexes meeting condition

    threshold=threshold
    islarger=array3D>=threshold
  
    return islarger


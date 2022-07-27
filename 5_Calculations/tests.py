import random
import numpy as np
from plot import histoplot

from Classes import DataO
from Classes import MapO

'to run test generate testing DataObject'
'TODO: create run_tests function'

'Note: visualising distribution'
#plotting values across 28 mmbers (1 location, 1 month)
def print_histo(array4D):
    month=random.randint(0,len(array4D[0,:,0,0])-1)
    xloc=random.randint(0,len(array4D[0,0,:,0])-1)
    yloc=random.randint(0,len(array4D[0,0,0,:])-1)

    vars=array4D[:,month,xloc,yloc]

    ysort=np.sort(vars)
    histoplot(ysort)


def counter_test(p90,dataObject_test):
    ### TESTING MODULE -Counter ###
    zero_array=np.zeros(np.shape(p90))
    dataObject_test.set_threshold(20)
    dataObject_test.p90_array=zero_array
    dataObject_test.counter(periodiser=20)
    counter_array_test=dataObject_test.counter_array
    flat_counter_array_test=dataObject_test.flat_array(counter_array_test)

    for array in flat_counter_array_test:
        for element in array:
            assert element.all()==0, "element is non 0"


    ones_array=np.ones(np.shape(p90))
    for array in ones_array:
        for element in array:
            assert element.all()==1, "element is non 1"
            
    dataObject_test.p90_array=ones_array
    dataObject_test.set_threshold(1)

    dataObject_test.counter(periodiser=20)
    counter_array_test=dataObject_test.counter_array
    flat_counter_array_test=counter_array_test.flatten('F')
    #flat_counter_array_test=dataObject_test.flat_array(counter_array_test)

    for element in flat_counter_array_test:
            assert element==240, "element is non 240, is " +str(element)

def flat_test(dataObject_test):
    ### TESTING MODULE - flattening ###

    array=np.array([[1,2,3],[4,5,6],[7,8,9]])
    flatarray_method=dataObject_test.flat_array(array)


    flatarray_lib=array.flatten('F')
    assert flatarray_method.all()==flatarray_lib.all(), 'Flattening method does not have stable results'


def passedKS_test(WV_list):
    'Testing : run only if KS test calculated'
    for object in WV_list:
        object.display_results()
        object.KS_passed(setting=0.99)
        print("This variable has passed the KS test: " + str(object.KS))
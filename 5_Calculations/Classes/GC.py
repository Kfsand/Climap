import numpy as np
import pandas as pd
import json
from Classes import DataO
import os
from numpy import NaN


class GComponent:

    ##### CLASS ATTRIBUTES ####
    # GCID : (string) name if grid component, used to extract correct thresholds and correlations
    # THRESHOLDS : (dataframe) relevant slive of general threshold table, 
                # counter threshold, value above which event is judge extreme (or below which if Mintemp)
    # CORREL Table : (dataframe) relevant slive of general correlations table
    # DATAOBJECTS : (object dataobject)list of used DataObjects
    # COUNTER : (list of arrayd ) 
                # np.array shape= blocks,ydim.xdim 2D array with number of time points where weather variable exceeds threshold, 
                # in multiple blocks if more than one 20y period evaluated
    # FCOUNTER : (np.array len=ydim*xdim ) flat counter array 1D
    # IMPACTS: (array) table of impact arrays for each evaluated DataObject and threshold
    # FIMPACTS: (array) flat imapct array

    ######### INIT #########
    # 1. initialising attributes
#
    def __init__(self,GCID):

        self.GCID=GCID
        self.data_objects=[]
        self.correls={}
        self.impact_arrays={}


    def init_thresh(self,threshold_df):
        
        # print('Init '+ str(self.GCID) + ' thresholds at: ' ) #as expected
        # print(threshold_df.loc[self.GCID,:])
        self.thresholds=threshold_df.loc[self.GCID,:]
    
    def init_correl(self,correls_df,wv_list):
        
        for wv in wv_list:

            correlation=correls_df.loc[self.GCID,wv.varID]
            
            # adds correlation to dictionnary, adds NaN if no function was initialised
            self.correls[wv.varID]=correlation            

    def add_DataO(self,data_object):
        self.data_objects.append(data_object)

    def calc_impacts(self,threshold,do): 
        '#passed on threshold for now,to replace with self.threshold list in correct way'
        # print('\n'+'in calc_impacts, printing for: ' + do.varID)

        #1. call counter function of do with chosen threshold (using varname)
        diff_array=do.counter(threshold,option='rel')
        # print('\n in calc_impacts, diff type is:')
        # print(type(diff_array))
        # print(np.shape(diff_array))

        # #2. recover result and calculate impact array

        if pd.isna(self.correls[do.varID]):
            
            #print('no correlations provided, impact calculation unsuccesful')
            return

        else:

            impact_array=self.correls[do.varID](diff_array); 'TODO: also iterate over correlations, for the moment just one,'
            self.impact_arrays["avg impact"]=np.mean(impact_array,axis=0)
            self.impact_arrays["max impact"]=np.max(impact_array,axis=0)
            # print('\n in calc_impacts, impact_array type is:')
            # print(type(self.impact_array))
            # print(np.size(self.impact_array))





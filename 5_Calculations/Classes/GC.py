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

        #1. call counter function of DO with chosen threshold (using varname)
        data_array=do.counter(threshold,option='rel')

        # #2. recover result and calculate impact array
        if pd.isna(self.correls[do.varID]):
            
            print('no correlation provided for: ' + self.GCID + '- variable '+ do.varID + ' impact calculation unsuccesful')
            return

        else:
            #saves min, max and avg impact values across time for each spatial location

            impact_array=self.correls[do.varID](data_array); 'TODO: also iterate over correlations, for the moment just one,'
            self.impact_arrays["avg impact"]=np.mean(impact_array,axis=0)
            self.impact_arrays["max impact"]=np.max(impact_array,axis=0)
            self.impact_arrays["min impact"]=np.min(impact_array,axis=0)


    def calc_impacts_abs(self):
        #used to recover absolute maximum min, max and avg impact values over entire space

        minimpact=round(np.min(self.impact_arrays["max impact"]),2)
        maximpact=round(np.max(self.impact_arrays["max impact"]),2)
        avgimpact=round(np.mean(self.impact_arrays["max impact"]),2)

        return [minimpact, maximpact, avgimpact]



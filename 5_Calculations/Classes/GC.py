import numpy as np
import pandas as pd
import json
from Classes import DataO
import os



class GComponent:

    ##### CLASS ATTRIBUTES ####
    # NAME : (string) 
    # THRESHOLDS : (dataframe) relevant slive of general threshold table, 
                # counter threshold, value above which event is judge extreme (or below which if Mintemp)
    # CORREL Table : (dataframe) relevant slive of general correlations table
    # DATAOBJECTS : (list - strings) name list of used DataObjects
    # COUNTER : (list of arrayd ) 
                # np.array shape= blocks,ydim.xdim 2D array with number of time points where weather variable exceeds threshold, 
                # in multiple blocks if more than one 20y period evaluated
    # FCOUNTER : (np.array len=ydim*xdim ) flat counter array 1D
    # IMPACTS: (array) table of impact arrays for each evaluated DataObject and threshold
    # FIMPACTS: (array) flat imapct array

    ######### INIT #########
    # 1. initialising attributes

    def __init__(self,name):

        self.name=name
        self.data_objects=[]
        self.counters={}
        self.fcounters={}

    def init_thesh(self,threshold_df):

        self.thesholds=threshold_df.loc[self.name,:]
    
    def init_correl(self,correls_df):

        self.correls=correls_df[self.name,:]

    def add_DataO(self,data_object):
        self.data_objectst.append(data_object.name)

    def add_counter(self,datao):
        'Save in dictionary for retreaval with name '
        [array, farray]=datao.counter(self.thresholds[datao.varname])
        self.counters.append(array)
        self.fcounters.append(farray)

    def calc_impacts(self,varname,counterID):
        'need : varname to get correct correlation from corrl table'
        f = self.correls[self.name,varname]

        array=f(counterID.all())




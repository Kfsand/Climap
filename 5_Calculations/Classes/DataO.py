#import necessary libraries
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import norm
import os
import math

class DataObject:

    ##### CLASS ATTRIBUTES ####
    # title : (string)
    # varname : (string)
    # sres : (int)
    # tres : (int)
    # fdname : (path)
    # fdpath : (path)
    # respath : (path)
    # xcoord : (np.array)
    # ycoord : (np.array)
    # untreated_array : (np.array)
    # KS_results : (list)
    # KS : (bool)
    # stats : (list)
    # p90_array : (np.array)
    # threshold: (int)
    # counter_array: (np.array shape= blocks,ydim.xdim)

    'TODO: create flat_prop_arrays, create counter at this level'


    def __init__(self,title,varname,sres,tres,fdname,fdpath,respath,rows_block=25,rows_data=23,columns_data=14,):

        #title: name of variable ex: MaxTemp
        self.title=title
        self.varname=varname
        self.sref=sres
        self.tres=tres
        self.fdname=fdname
        self.respath=respath+'/'+title

        #creating result directory
        if not os.path.exists(self.respath):
            os.mkdir(self.respath)
    
        #loading data
        [self.xcoord, self.ycoord, self.untreated_array]=self.loadnp(fdpath,rows_block=rows_block,rows_data=rows_data,columns_data=columns_data)   

    def loadnp(self,path,rows_block=25,rows_data=23,columns_data=14):


        # create list of files names to open, every .csv file in directory
        list_file=[f for f in os.listdir(path) if ".csv" in f]
        #initialising 4D array storing all values
        array4D=[]

        #list of column names, needed to force correct shape of df
        col_names=["x"+str(i) for i in range(columns_data+1)]

        #opening and reading each consecutive file
        for f in list_file:
            df = pd.read_csv(os.path.join(path,f),skiprows=14, names=col_names)
            #initialising 3D array storing values of each file
            array3D=[]

            'NOTE: change range to nb blocks=nbrowstotal/bn rows block'
            rows_block=rows_block
            rows_data=rows_data
            for i in range(935):
                idx_1 = rows_data*i+i*2+2
                idx_2 = rows_data*(i+1)+2*(i)+2
                array3D.append(df.iloc[idx_1:idx_2, 1:].to_numpy())
            
            array3D=np.stack(array3D)
            array4D.append(array3D)
        array4D=np.stack(array4D)
        #si tu veux pas un array 3d
        #(exemple pour exporter en csv) alors np.vstack pour tout mettre à la suite


        #intitialising common coordinate vectors from last df read
        [xcoord, ycoord]=[df.iloc[1,1:].map(lambda x : int(float(x)) ).to_numpy(),df.iloc[2:24,0].map(lambda x : int(float(x)) ).to_numpy()]
        return [xcoord, ycoord, array4D]

    def run_stats(self,KStest=True,stats=True,tp_90=True):
        if KStest==True:
            self.KS_results=self.norm_test()

            self.success_rate=self.KS_results[1]/self.KS_results[0]
            if self.success_rate > 0.99:
                self.KS=True
            else:
                self.KS=False

        if stats==True:
            self.stats=self.av_min_max()
        
        if tp_90==True:
            self.p90_array=self.p_90()

    def norm_test(self, Dcrit=0.25, timeaxis=1,xaxis=2,yaxis=3,Save=True,Display=False):

        array4D=self.untreated_array

        '''H0:  the data are normally distributed
        Ha:  the data are not normally distributed
        Significance level:  α = 0.05
        Critical value:  Dcrit=0.25    
        Critical region:  Reject H0 if D > Dcrit'''

        total=0
        fitted=0
        fails=0
        stat_array=np.empty([np.shape(array4D)[timeaxis],np.shape(array4D)[xaxis],np.shape(array4D)[yaxis]],dtype=object)
        mstats=np.empty([4,1])

        
        'TODO: create stat_array with shape 2xarray4D.shape(2),3,4'

        dist = getattr(stats, 'norm')

        for i in range(935):
            for j in range(23):
                for k in range(14):
                    slice=array4D[:,i,j,k]
                    #outputs are mean and std dev
                    parameters = dist.fit(slice)
                    #ouputs are statistic and pvalue
                    result=stats.kstest(slice, "norm", parameters)
                    test_statistic=result[0]

                    if test_statistic>Dcrit:
                        fails+=1
                    else:
                        fitted+=1
                    mstats=[parameters[0],parameters[1],result[0],result[1]]
                    stat_array[i,j,k]=mstats
                    total+=1
        
        test_results=[total,fitted,fails,Dcrit,stat_array]
        #Diplaying results
        if Display==True:
            print(str(fitted)+" fit a normal distribution out of : "+str(total)+" with critical value of: "+str(Dcrit))
            print("success rate: " +str(fitted/total))
        
        #Saving results
        if Save==True:
            np.savez(self.respath+'/norm_results',test_results)

        return test_results

    def av_min_max(self):
        return [np.mean(self.untreated_array,axis=0), np.amax(self.untreated_array,axis=0), np.amin(self.untreated_array,axis=0)]

    def p_90(self,Save=True):
        p90_array=np.percentile(self.untreated_array,90,axis=0)

        if Save==True:
            np.savez(self.respath+'/p90',p90_array)
        return p90_array

    def flat_array(self,array):
        #flattens an array one column after another
        # to follow features which are squares buit colmn-wise (iteration through y then y)

        flatarray=array.flatten('F')
        return flatarray

    def set_threshold(self,threshold):
        self.threshold=threshold

    def counter(self,periodiser=20):
         #function takes in an array, a theshold and a year period -
        # returns array of ints = nb of months the values 
        # in the argument array exceeded the threshold during the specified time period.
        
        d1=np.size(self.p90_array,0)
        self.counter_array=np.empty(self.p90_array.shape)

        if self.tres=='monthly':
            nmonths=12*periodiser

        #computing bool array of values exceeding threshold (=>)
        exc_array=self.islarger(self.p90_array,self.threshold)

        stacker=[]

        for i in range(math.ceil(d1/nmonths)):
        
            #slicing appropriate time period from bool array
            idx_1 = nmonths*i
            idx_2 = nmonths*(i+1)
            slice=exc_array[idx_1:idx_2,:,:].astype(int)

            #sum of bool as ints within selected time period
            stacker.append(np.sum(slice,axis=0, dtype=np.int32))
            
        self.counter_array=np.stack(stacker,axis=0)

    def islarger (self,array3D, threshold):
        #returns boolean matrix of indexes meeting condition

        threshold=threshold
        islarger=array3D>=threshold
    
        return islarger    



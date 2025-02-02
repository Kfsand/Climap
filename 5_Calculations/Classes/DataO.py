 #import necessary libraries
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import norm
import os
import math
import csv

class DataObject:

    ##### CLASS ATTRIBUTES ####
    # TITLE : (string) title of dataobject - used for component calculatations USE SAME AS NAME OR VARIABLE IN CODE
    # VARID : (string) name of variable ex: MaxTemp - used in map object USE SAME AS THRESHOLDS AND CORREL DATAFRAMES
    # SRES : (int) spatial resolution (in km_sqr)
    # TRES : (int) time resolution (dayly, monthly, seasonal, yearly)
    # SYEAR: (int) start year of data series
    # FYEAR: (int) end year of data series (included)
    # FDPATH : (path) path of data folder
    # RESPATH : (path) path of result folder
    # MEMBERS: (int) number of evaluated climate scenario members
    # TOTAL_ROWS : (int) number of rows in data excel
    # BLOCK_ROWS : (int) total number of rows in one data block, including coordinate and blanck rows (one time unit: ex one month)
    # DATA_ROWS : (int) number of data rows in one data block (one time unit: ex one month)
    # DATA_COLUMNS : (int) number of data columns (excluding coordinate column)
    # XCOORD : (np.array) xcoordinate 1D array (length data_rows)
    # YCOORD : (np.array) ycoordinate 1D array (length data_columns)
    # UNTREATED_ARRAY : (np.array) raw data array [members,time,ydim,xdim]
    # KS_RESULTS : (list) [total,fitted,fails,Dcrit,stat_array]
    # KS : (bool) set to True if KS success_rate > 0.99, False otherwise
    # STATS : (list) [mean_array_across_time max_array_across_time min_array_across_time]
    # P90_ARRAY : (np.array) array of p90 values accross members (90% of values fall below p90)
    # P10_ARRAY : (np.array) array of p10 values accross members (10% of values fall below p10), used for MINTEMP



    ######### INIT #########
    # 1. initialising attributes
    # 2. creating result directory
    # 3. loading data

    def __init__(self,title,varID,sres,tres,syear,fyear,fdpath,respath,
                members=12,total_rows=58794,block_rows=246,data_rows=243,data_columns=153):
        
        ######### 1 ########## - initialising attributes
        self.title=title
        self.varID=varID
        self.sref=sres
        self.tres=tres
        self.syear=syear 
        self.fyear=fyear
        self.respath=respath+'/'+title
        self.members=members
        self.total_rows=total_rows
        self.block_rows=block_rows
        self.data_rows=data_rows
        self.data_columns=data_columns

    
        ######### 2 ########## - creating result directory
        if not os.path.exists(self.respath):
            os.mkdir(self.respath)
        
        ######### 3 ########## - loading data
        if sres==5 and tres=='monthly':
            [self.xcoord, self.ycoord, self.untreated_array]=self.load_subsets(fdpath)
        
        if sres==60 and tres=='daily':
            [self.coord_dict, self.untreated_array]=self.load_sqrs(fdpath)




    def load_subsets(self,path):

        # create list of files names to open, every .csv file in directory
        list_file=[f for f in os.listdir(path) if ".csv" in f]
        #initialising 4D array storing all values
        array4D=[]

        #list of column names, needed to force correct shape of df
        col_names=["x"+str(i) for i in range(self.data_columns+1)]

        #opening and reading each consecutive file
        for f in list_file:
            df = pd.read_csv(os.path.join(path,f),skiprows=14, names=col_names)
            #initialising 3D array storing values of each file
            array3D=[]

            for i in range(math.ceil(self.total_rows/self.block_rows)):

                
                #slicing data from dataframe and storing it into 3D array for stacking
                #each time block is stored separately
                # data is saved skipping date row and excluding coordinate column and row
                # this section should adapt to varying block and data_row sizes

                idx_1 = self.block_rows*i+2
                idx_2 = idx_1+self.data_rows-1
                array3D.append(df.iloc[idx_1:idx_2+1, 1:].to_numpy())
            array3D=np.stack(array3D)
            array4D.append(array3D)
        array4D=np.stack(array4D)

        #si tu veux pas un array 3d
        #(exemple pour exporter en csv) alors np.vstack pour tout mettre à la suite

        #intitialising common coordinate vectors from last df read
        [xcoord, ycoord]=[df.iloc[1,1:].map(lambda x : int(float(x)) ).to_numpy(),df.iloc[2:self.block_rows,0].map(lambda x : int(float(x)) ).to_numpy()]
        return [xcoord, ycoord, array4D]

    def load_sqrs(self,path):

        'How to go in each directory'
        # create list of files names to open, every .csv file in directory
        list_file=sorted([f for f in os.listdir(path) if ".csv" in f])

        #coordinate dict
        coord_dict={}
        #initialising 3D array storing all values
        array3D=[]

        #list of column names, needed to force correct shape of df
        col_names=["member_"+str(i) for i in range(self.data_columns+1)]

        #locaiton/file/square ID
        squareID=1

        #opening and reading each consecutive file
        for f in list_file:

            #collecting coordinates
            with open(os.path.join(path,f),newline='') as csvfile:
                reader=csv.DictReader(csvfile)
                for i, row in enumerate(reader): 
                    if i==0:

                        values = row['13'].split(" ")  #first value is xcoord, second value is ycoord
                        xcoord = int(float(values[0]))
                        ycoord = int(float(values[1]))
                        coord_dict[squareID]=(xcoord, ycoord)
            squareID+=1
            
            #reading and saving values
            df = pd.read_csv(os.path.join(path,f),skiprows=13, names=col_names)
            #initialising 3D array storing values of each file
            array2D=[]
        
            #saving all values in file
            array2D.append(df.iloc[:,1:13].to_numpy())

            array3D.append(array2D)
        
        array3D=np.stack(array3D)
        array3D=np.transpose(array3D,(3,2,1,0))
        return [coord_dict, array3D]

    def run_stats(self,KStest=False,stat_source='p90',tp_90=True,tp_10=False):

        #    stat_source can either be 'members' for a calculation of avg,max and min over member data purely
        #    or (PREFERRED OPTION) can be 'p90' for a calculation of avg,max and min over p90 of member data : 

        if KStest==True:
            self.KS_results=self.norm_test()

            self.success_rate=self.KS_results[1]/self.KS_results[0]
            if self.success_rate > 0.99:
                self.KS=True
            else:
                self.KS=False
        
        if tp_90==True:
            self.p90_array=self.p90()
        
        if tp_10==True:
            self.p10_array=self.p10()

        if stat_source=='members':
            [self.member_avg, self.member_max, self.member_min]=self.av_min_max(self.untreated_array)
        elif stat_source=='p90':
            [self.member_avg, self.member_max, self.member_min]=self.av_min_max(self.p90_array)

    def norm_test(self,timeaxis=1,xaxis=2,yaxis=3,Save=True,Display=True):

        array4D=self.untreated_array

        '''H0:  the data are normally distributed
        Ha:  the data are not normally distributed
        Significance level:  α = 0.05
        Critical value:  Dcrit=0.25 for 28 members
                         Dcrit=0.37543 for 12 members

        Critical region:  Reject H0 if D > Dcrit'''

        if self.members==12:
            Dcrit=0.37542
        if self.members==28:
            Dcrit=0.25

        total=0
        fitted=0
        fails=0
        stat_array=np.empty([np.shape(array4D)[timeaxis],np.shape(array4D)[xaxis],np.shape(array4D)[yaxis]],dtype=object)
        mstats=np.empty([4,1])

        dist = getattr(stats, 'norm')

        for i in range(math.ceil(self.total_rows/self.block_rows)):
            for j in range(self.data_rows):
                for k in range(self.data_columns):
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
        #setting boolean to reflect KS results
        self.KS_check()

        #Diplaying results
        if Display==True:
            print(str(fitted)+" fit a normal distribution out of : "+str(total)+" with critical value of: "+str(Dcrit))
            print("success rate: " +str(fitted/total))
        
        #Saving results
        if Save==True:
            np.savez(self.respath+'/norm_results',test_results)

        return test_results

    def av_min_max(self, array):
        return [np.mean(array,axis=0), np.amax(array,axis=0), np.amin(array,axis=0)]

    def p90(self,Save=True):
        p90_array=np.percentile(self.untreated_array,90,axis=0)

        if Save==True:
            np.savez(self.respath+'/p90',p90_array)
        return p90_array

    def p10(self,Save=True):
        p10_array=np.percentile(self.untreated_array,10,axis=0)

        if Save==True:
            np.savez(self.respath+'/p10',p10_array)
        return p10_array

    def flat_array(self,array):
        #flattens an array one column after another
        # to follow features which are squares buit colmn-wise (iteration through y then x)

        flatarray=array.flatten('F')
        return flatarray

    def counter(self,thresh,periodiser=20, option='rel'):
        'TODO: solve issue of missing months in year blocks'
        #function takes in an array, a theshold and a year period -
        # returns array of ints = nb of months the values 
        # in the argument array exceeded the threshold during the specified time period.
        # option can be either 'abs': counting occurrances above threshold,
        # or 'rel': counting occurrances above threhold and scale of excess (weighted mean)

        'NOTE: monthly option is not up to date, rel calculations are not correct, needs to use same approach as daily'
        if self.tres=='monthly':

            assert self.p90_array.shape==(239,self.data_rows,self.data_columns), "p90_array passed on doesn't have correct shape"
            
            #setting first dimension as total number of months in array
            d1=np.size(self.p90_array,0)
            counter_array=np.empty(self.p90_array.shape)
            
            #number of months in block of periodiser years
            nmonths=12*periodiser
            
            if option=='abs':
                #computing bool array of values exceeding threshold (=>)
                bool_array=self.islarger(self.p90_array,thresh)

                stacker=[]

                for i in range(math.ceil(d1/nmonths)):
                
                    #slicing appropriate time period from bool array
                    idx_1 = nmonths*i
                    idx_2 = nmonths*(i+1)
                    slice=bool_array[idx_1:idx_2,:,:].astype(int)

                    #sum of bool as ints within selected time period
                    stacker.append(np.sum(slice,axis=0, dtype=np.int32))    
                counter_array=np.stack(stacker,axis=0)

                fcounter_array=self.flat_array(counter_array)

                assert counter_array.shape==(math.ceil(d1/nmonths),self.data_rows,self.data_columns), "produced counter array doesn not have correct shape"
                
            if option=='rel':
                
                #1.checking if value is above thresh for each time-space point
                bool_array=self.islarger(self.p90_array,thresh)
                #2.created DT=T-T_thresh array for all time-space points
                diff_array=self.p90_array-thresh

                stacker=[]

                for i in range(math.ceil(d1/nmonths)):
                
                    #slicing appropriate time period from arrays
                    idx_1 = nmonths*i
                    idx_2 = nmonths*(i+1)
                    #product of DT array with bool array generates array with DT as value if T>=Thresh or 0 as value if T>thres
                    slice=diff_array[idx_1:idx_2,:,:]*bool_array[idx_1:idx_2,:,:].astype(int)

                    #sum of bool as ints within selected time period
                    stacker.append(np.sum(slice,axis=0, dtype=np.int32))

                #normalisation
                stacker=stacker/nmonths    
                counter_array=np.stack(stacker,axis=0)

                assert counter_array.shape==(math.ceil(d1/nmonths),self.data_rows,self.data_columns), "produced counter array doesn not have correct shape"

            return  counter_array

        if self.tres=='daily':
            #assert self.p90_array.shape==(7200,1,75), "p90_array passed on doesn't have correct shape"
            
            if option=='abs':

                #1. compute bool array of values exceeding threshold (checking Tamb >= Tthresh)
                bool_array=self.islarger(self.p90_array,thresh)
                #summing bools
                counter_array=np.sum(bool_array,axis=0, dtype=np.int32)

                return  counter_array

            if option=='rel':

                #1. compute bool array of values exceeding threshold (checking Tamb >= Tthresh)
                bool_array=self.islarger(self.p90_array,thresh)
                
                #2. multiplying data and bool arrays -> only values above threshold non null
                data_array=np.multiply(self.p90_array,bool_array)

                #3. passing on to impact calculations
                return  data_array

    def islarger(self,array3D, threshold):
        #returns boolean matrix of indexes meeting condition

        threshold=threshold
        islarger=array3D>=threshold
    
        return islarger    
    
    def display_results(self):

        [total,fitted,fails,Dcrit,stat_array]=self.KS_results
        print("\n KS test results for Weather Variable: "+self.varID)
        print(str(fitted)+" fit a normal distribution out of : "+str(total)+" with critical value of: "+str(Dcrit))
        print("success rate: " +str(fitted/total))

    def KS_check(self,setting=0.99):
        [total,fitted,fails,Dcrit,stat_array]=self.KS_results

        if fitted/total >= setting:

            self.KS=True
        else:
            self.KS=False


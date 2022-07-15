import numpy as np
from scipy import stats
from scipy.stats import norm

def run_stats(array4D,path,KStest=True,stats=True,tp_90=True,result='p_90'):
    if KStest==True:
        test_results=norm_test(array4D,resultpath=path)
        if result=='KS':
            return test_results

    if stats==True:
        stats=av_min_max(array4D)
        if result=='stats':
            return stats
    
    if tp_90==True:
        results_p_90=p_90(array4D,resultpath=path)
        if result=='p_90':
            return results_p_90

def norm_test(array4D, Dcrit=0.25, timeaxis=1,xaxis=2,yaxis=3,resultpath='../6_Results/data/',Save=True,Display=True):

    array4D=array4D

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
        np.savez(resultpath+'/norm_results',test_results)

    return test_results

def av_min_max(array4D,axis=0):
    return [np.mean(array4D,axis=0), np.amax(array4D,axis=0), np.amin(array4D,axis=0)]

def p_90(array4D,axis=0,resultpath='../6_Results/data/',Save=True):
    p90_array=np.percentile(array4D,90,axis=axis)

    if Save==True:
        np.savez(resultpath+'/p90',p90_array)
    return p90_array
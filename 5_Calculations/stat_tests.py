import numpy as np
from scipy import stats
from scipy.stats import norm


def norm_test(array4D, Dcrit=0.25, timeaxis=1,xaxis=2,yaxis=3):

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

    for i in range(1199):
        for j in range(22):
            for k in range(13):
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
    return [total,fitted,fails,Dcrit,stat_array]

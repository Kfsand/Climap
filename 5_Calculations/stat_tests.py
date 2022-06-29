from scipy import stats
from scipy.stats import norm


def norm_test(array4D, Dcrit=0.25):

    '''H0:  the data are normally distributed
      Ha:  the data are not normally distributed
      Significance level:  α = 0.05
      Critical value:  Dcrit=0.25    
      Critical region:  Reject H0 if D > Dcrit'''

    total=0
    fitted=0
    fails=0

    array4D=array4D
    'TODO: create stat_array with shape 2xarray4D.shape(2),3,4'
    stat_array=[]

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
                'TODO: append statistic and pvalue for each element +return statarray to write in file'
                #stat_array.append([])
                total+=1
    return [total,fitted,fails,Dcrit]

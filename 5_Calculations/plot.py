#plotting functions

from matplotlib.ticker import PercentFormatter
import matplotlib.pyplot as plt
import matplotlib.colors as colors

def histoplot (toplot,n_bins=25):
    fig, axs = plt.subplots(1, 2, tight_layout=True)

    n_bins = n_bins

    axs[0].hist(toplot, bins=n_bins)

    # N is the count in each bin, bins is the lower-limit of the bin
    N, bins, patches = axs[0].hist(toplot, bins=n_bins)

    # We'll color code by height, but you could use any scalar
    fracs = N / N.max()

    # we need to normalize the data to 0..1 for the full range of the colormap
    norm = colors.Normalize(fracs.min(), fracs.max())

    # Now, we'll loop through our objects and set the color of each accordingly
    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)

    # We can also normalize our inputs by the total number of counts
    axs[1].hist(toplot, bins=n_bins, density=True)

    # Now we format the y-axis to display percentage
    axs[1].yaxis.set_major_formatter(PercentFormatter(xmax=1))
import numpy as np
import matplotlib.pyplot as plt

# we use a random seed to change the random result that we get each time we run the code.
# we have to put this outside the function 
np.random.seed()
rseed = np.random.randint(100)
print(rseed)

def plot_interactive_line(numdata=20, a=2., b=2., noiselevel=2.):

    # User-defined model:
    xmax=10
    x = np.linspace(-xmax, xmax, int(100*xmax))
    y = a + b*x
 
    # create random noisy data
    # get a random a between (0,5) and b between (0,5)
    np.random.seed(rseed)
    a_true = 5 * np.random.rand()
    b_true = 5 * np.random.rand()
    
    # create some synthetic GPS locations
    xdata = np.linspace(-0.9*xmax,0.9*xmax,numdata) + np.random.normal(loc=0,scale=1,size=numdata)
    
    # create the synthetic model
    ymodel = a_true + b_true * xdata
    
    #add gaussian noise: mean of 0, standard deviation of 'noiselevel'
    ynoise = np.random.normal(loc=0,scale=noiselevel,size=numdata)
    
    #get the final 'observed' data
    ydata = ymodel + ynoise
    
    # compute the model from the input parameters
    ydata_predicted = a + b*xdata
    
    # compute the total misfit ('chi-squared' statistic): 
    # this is the sum of the misfits, divided by number of data and the data noise
    chi_squared = np.sum( (ydata - ydata_predicted)**2 )/(numdata*noiselevel**2)
    
    # prepare the plot
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    
    # prepare the axes limits
    ax.set_xlim((-xmax,xmax))
    ax.set_ylim((-50,50))
    
    #ax.plot(x, y, 'bx')
    points = ax.errorbar(xdata, ydata, fmt='kx', yerr=noiselevel, label='Data')
    lineref = ax.plot(x, y, 'b-',label = "Model: a=%.1f, b=%.1f"%(a,b))
    ax.text(-0.9*xmax,-45,'misfit = %.2f'%chi_squared)
    
    plt.setp(lineref, linewidth=2)
    plt.legend()
    plt.show()

    return a_true, b_true, xdata, ydata

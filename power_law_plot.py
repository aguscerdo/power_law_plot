import numpy as np
import matplotlib.pyplot as plt
from os import path, mkdir


def get_c(x, a):
    e = np.reciprocal(np.power(x, a))
    c = np.sum(e)
    return [c, e]


def plot_distribution(a, l, cumulative=False, log=False, save=False):
    if l <= 1:
        print("L needs to be greater than 1, got {}".format(l))
        return

    if not isinstance(a, list):
        a = [a]

    if cumulative:
        x = np.arange(1, l + 1)
    else:
        spacing = 10*(l+1)
        x = np.linspace(1, l+1, spacing)
        
    if log:
        xplot = np.log10(x)
    else:
        xplot = x
    

    ymax = 0
    ymin = 0

    cmap = plt.get_cmap('jet')
    colors = cmap(np.linspace(0, 1, len(a)))

    for j in range(len(a)):
        if not np.sign(a[j]) == 1:
            print("Alphas must be >0, got {}".format(a[j]))
            return

        results = get_c(x, a[j])
        c = results[0]
        y = np.divide(results[1], c)

        if cumulative:
            for i in range(1, len(y)):
                y[i] += y[i-1]

        if log:
            yplot = np.log10(y)
        else:
            yplot = y

        if cumulative:
            plt.plot(xplot, yplot, c=colors[j], label='Alpha = {}'.format(a[j]))
            plt.legend(bbox_to_anchor=(0.99, 0.01), loc=4, borderaxespad=0.)
        else:
            plt.plot(xplot, yplot, c=colors[j], label='Alpha = {}'.format(a[j]))
            plt.legend(bbox_to_anchor=(0.99, 0.99), loc=1, borderaxespad=0.)

        nymax = np.max(yplot)
        nymin = np.min(yplot)
        if(ymax < nymax): ymax = nymax
        if(ymin > nymin): ymin = nymin

    if cumulative:
        plt.title("Cumulative Plot\nL = {}".format(l))
        if log:
            plt.ylabel("-log[cumulative(c * k^-a)]")
            plt.xlabel("log(k)")
        else:
            plt.ylabel("cumulative[(c * k^-a)^-1]")
            plt.xlabel("k")
    else:
        plt.title("Distribution Plot\nL = {}".format(l))
        if log:
            plt.ylabel("-log(c * k^-a)")
            plt.xlabel("log(k)")
        else:
            plt.ylabel("(c * k^-a)^-1")
            plt.xlabel("k")

    axes = plt.gca()
    axes.set_xlim([np.min(xplot), np.max(xplot)])
    axes.set_ylim([ymin, ymax])

    if save:
        if cumulative:

            if log: plt.savefig("images/cumulative_L{}_log.png".format(l))
            else: plt.savefig("images/cumulative_L{}.png".format(l))
        else:
            if log: plt.savefig("images/distribution_L{}_log.png".format(l))
            else: plt.savefig("images/distribution_L{}.png".format(l))
        plt.clf()
    else:
        plt.show()
        plt.clf()


def save_batch(alphas, Ls, log=True, normal=False):
    if not path.exists("images"):
        mkdir("images")

    if not isinstance(Ls, list):
        Ls = [Ls]

    for l in Ls:
        # Save Distributions
        if normal:
            plot_distribution(alphas, l, cumulative=False, log=False, save=True)
            plot_distribution(alphas, l, cumulative=True, log=False, save=True)
        if log:
            plot_distribution(alphas, l, cumulative=False, log=True, save=True)
            plot_distribution(alphas, l, cumulative=True, log=True, save=True)

        print("L = {} saved".format(l))

    print("All files saved")

##-----------------------------------------------------------##

alpha = [1.2, 1.5, 2.0, 2.2]
L = [100, 500, 1500]

# Save
#                        log scale; normal scale
# save_batch(alphas, Ls, log=True, normal=False)
save_batch(alpha, L, log=True, normal=False)

# Only display
# plot_distribution(alphas, L, cumulative=False,log=False, save=False):
# plot_distribution(alpha, 100, save=False)
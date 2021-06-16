from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import cm
import os
#if using a Jupyter notebook, include:
#%matplotlib inline

#E2E =5" T10
#No corruption
#NonLinkBased
#B0

T10_B0_NonDB_mean_entropy = '/home/gaia/Documents/SecondPaper/LogsDummies/NonLinkBased/B_0_mean_entropy_RateDummies.csv'
T10_B0_NonDB_eps = '/home/gaia/Documents/SecondPaper/LogsDummies/NonLinkBased/B_0_eps_RateDummies.csv'
T10_B0_NonDB_delta = '/home/gaia/Documents/SecondPaper/LogsDummies/NonLinkBased/B_0_delta_RateDummies.csv'
#B=30%
T10_B30_NonDB_mean_entropy = '/home/gaia/Documents/SecondPaper/LogsDummies/NonLinkBased/B_30_RateDummies_mean_entropy.csv'
T10_B30_NonDB_eps = '/home/gaia/Documents/SecondPaper/LogsDummies/NonLinkBased/B_30_RateDummies_eps.csv'
T10_B30_NonDB_delta = '/home/gaia/Documents/SecondPaper/LogsDummies/NonLinkBased/B_30_RateDummies_delta.csv'



#LinkBased
#E2E =5" T10
#B0

T10_B0_LB_mean_entropy = '/home/gaia/Documents/SecondPaper/LogsDummies/LinkBased/B_0_LB_mean_entropy.csv'
T10_B0_LB_eps = '/home/gaia/Documents/SecondPaper/LogsDummies/LinkBased/B_0_LB_eps.csv'
T10_B0_LB_delta = '/home/gaia/Documents/SecondPaper/LogsDummies/LinkBased/B_0_LB_delta.csv'
#B=30%


T10_B30_LB_mean_entropy = '/home/gaia/Documents/SecondPaper/LogsDummies/LinkBased/B_30_LB_mean_entropy.csv'
T10_B30_LB_eps = '/home/gaia/Documents/SecondPaper/LogsDummies/LinkBased/B_30_LB_eps.csv'
T10_B30_LB_delta = '/home/gaia/Documents/SecondPaper/LogsDummies/LinkBased/B_30_LB_delta.csv'


file = T10_B30_LB_delta
data = pd.read_csv(file)


F = data.to_numpy()
y = np.arange(10,110,10)
x = np.arange(1,11,1)
X,Y = np.meshgrid(x,y)
fig = plt.figure(figsize=(20,20))
ax = fig.add_subplot(111, projection='3d')

# Plot a 3D surface
ax.plot_surface(X, Y, F, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=1, antialiased=True)
ax.set_zlim(0,1)
ax.zaxis.set_tick_params(labelsize=20)
#ax.set_zticks([0, 2,4,6,8,10,12,14], fontsize = 16)
ax.set_ylabel('$Width$', fontsize = 20, labelpad=15)
ax.set_xlabel('$Layers$', fontsize = 20, labelpad=10)
#ax.set_zlabel('$\epsilon$', fontsize = 20, labelpad=15)
ax.set_zlabel('$\delta$', fontsize = 20, labelpad=15)
#ax.set_zlabel('Entropy', fontsize = 20, labelpad=15)
plt.yticks(fontsize=20)
plt.xticks(fontsize=20)
string_to_plot = os.path.basename(file)
#ax.set_title("30% corruption, traffic load = 1000, E2E=5")

plt.show()
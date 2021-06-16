from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import cm
import os
T10_E5_B0_D_F1000_Sim_1000_mean_entropy = '/home/gaia/Documents/SecondPaper/Dummies/T10_E5_B0_D_F1000_Sim_1000_mean_entropy.csv'
T10_E5_B0_D_F1000_Sim_1000_eps = '/home/gaia/Documents/SecondPaper/Dummies/T10_E5_B0_D_F1000_Sim_1000_eps.csv'


file = T10_E5_B0_D_F1000_Sim_1000_mean_entropy
data = pd.read_csv(file)

F = data.to_numpy()
y = np.arange(10,70,10)
x = np.arange(1,7,1)
X,Y = np.meshgrid(x,y)

fig = plt.figure(figsize=(20,20))
ax = fig.add_subplot(111, projection='3d')

ax.set_xticks([1,2,3,4,5,6])
ax.set_yticks([10,20,30,40,50,60])

# Plot a 3D surface
ax.plot_surface(X, Y, F, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=1, antialiased=True)
ax.set_zlim(0,2)
ax.zaxis.set_tick_params(labelsize=20)
#ax.set_zticks([0, 2,4,6,8,10,12,14], fontsize = 16)
ax.set_ylabel('$Width$', fontsize = 20, labelpad=15)
ax.set_xlabel('$Layers$', fontsize = 20, labelpad=10)
ax.set_zlabel('$\epsilon$', fontsize = 20, labelpad=15)
plt.yticks(fontsize=20)
plt.xticks(fontsize=20)
string_to_plot = os.path.basename(file)
#ax.set_title("30% corruption, traffic load = 1000, E2E=5")

plt.show()
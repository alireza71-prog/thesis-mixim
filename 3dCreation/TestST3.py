from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import cm
import os
#if using a Jupyter notebook, include:
#%matplotlib inline
#Traffic 1000
#E2E =5" T1000_B0_E5_eps
#No corruption
B_0_T1000_E5_mean = '/home/gaia/Documents/SecondPaper/CorrectLogs(entropy_eps)/T1000_B0_E5_mean_entropy.csv'
B_0_T1000_E5_eps = '/home/gaia/Documents/SecondPaper/CorrectLogs(entropy_eps)/T1000_B0_E5_eps.csv'
#30 percent corruption
T1000_B30_E5_mean_entropy = '/home/gaia/Documents/SecondPaper/CorrectLogs(entropy_eps)/T1000_B30_E5_mean_entropy.csv'
B_30_T1000_E5_eps = '/home/gaia/Documents/SecondPaper/CorrectLogs(entropy_eps)/T1000_B30_E5_eps.csv'
T1000_B30_E5_median_entropy = '/home/gaia/Documents/SecondPaper/CorrectLogs(entropy_eps)/T1000_B30_E5_median_entropy.csv'
#test = '/home/gaia/Documents/SecondPaper/CorrectLogs(entropy_eps)/test.csv'
#B_fixed 3 per layer

#3 per layer
B_Fixed_3pl_mean_entropy = '/home/gaia/Documents/SecondPaper/CorrectLogs(entropy_eps)/B_Fixed_3pl_mean_entropy.csv'
B_Fixed_3pl_median_entropy = '/home/gaia/Documents/SecondPaper/CorrectLogs(entropy_eps)/B_Fixed_3pl_median_entropy.csv'
B_Fixed_3pl_q25_entropy = '/home/gaia/Documents/SecondPaper/CorrectLogs(entropy_eps)/B_Fixed_3pl_q25_entropy.csv'
B_Fixed_3pl_eps = '/home/gaia/Documents/SecondPaper/CorrectLogs(entropy_eps)/B_Fixed_3pl_eps.csv'

#Dummies Link: False, Real traffic 10, E2E = 5, Budget 1000 Sim duration 1000

T10_E5_B0_D_F1000_Sim_1000_mean_entropy = '/home/gaia/Documents/SecondPaper/Dummies/T10_E5_B0_D_F1000_Sim_1000_mean_entropy.csv'
T10_E5_B0_D_F1000_Sim_1000_eps = '/home/gaia/Documents/SecondPaper/Dummies/T10_E5_B0_D_F1000_Sim_1000_eps.csv'
    #Dummies for B=30%
T10_E5_B30_D_F1000_Sim_1000_entropy = '/home/gaia/Documents/SecondPaper/Dummies/T10_E5_B30_D_F1000_Sim_1000_entropy.csv'
T10_E5_B3_D_F1000_Sim_1000_eps = '/home/gaia/Documents/SecondPaper/Dummies/T10_E5_B3_D_F1000_Sim_1000_eps.csv'
#Dummies Non LInk Based , Real traffic 10, E2E = 5, Budget 2000 Sim duration 2000
#Dummies: NonLinkBased B=0
T10_S2000_B0_Non_LB_Budget_mean_entropy = '/home/gaia/Documents/SecondPaper/LogsDummies/NonLinkBased/T10_S2000_B0_Non_LB_Budget_mean_entropy.csv'
T10_S2000_B0_Non_LB_Budget_eps = '/home/gaia/Documents/SecondPaper/LogsDummies/NonLinkBased/T10_S2000_B0_Non_LB_Budget_eps.csv'
T10_S2000_B0_Non_LB_Budget_delta = '/home/gaia/Documents/SecondPaper/LogsDummies/NonLinkBased/T10_S2000_B0_Non_LB_Budget_delta.csv'
#Dummies: NonLinkBased B=30%
T10_S2000_B30_Non_LB_Budget_mean_entropy = '/home/gaia/Documents/SecondPaper/LogsDummies/NonLinkBased/T10_S2000_B30_Non_LB_Budget_mean_entropy.csv'
T10_S2000_B30_Non_LB_Budget_eps = '/home/gaia/Documents/SecondPaper/LogsDummies/NonLinkBased/T10_S2000_B30_Non_LB_Budget_eps.csv'
T10_S2000_B30_Non_LB_Budget_delta = '/home/gaia/Documents/SecondPaper/LogsDummies/NonLinkBased/T10_S2000_B30_Non_LB_Budget_delta.csv'

#Dummies: Link-based B=0
T10_B0_S2000_DB_2000_mean_entropy = '/home/gaia/Documents/SecondPaper/LogsDummies/LinkBased/T10_B0_S2000_DB_2000_mean_entropy.csv'
T10_B0_S2000_DB_2000_eps = '/home/gaia/Documents/SecondPaper/LogsDummies/LinkBased/T10_B0_S2000_DB_2000_eps.csv'
T10_B0_S2000_DB_2000_delta = '/home/gaia/Documents/SecondPaper/LogsDummies/LinkBased/T10_B0_S2000_DB_2000_delta.csv'

#Dummies: Link-based B=30%
T10_B30_S2000_DB_2000_mean_entropy = '/home/gaia/Documents/SecondPaper/LogsDummies/LinkBased/T10_B30_S2000_DB_2000_mean_entropy.csv'
T10_B30_S2000_DB_2000_eps = '/home/gaia/Documents/SecondPaper/LogsDummies/LinkBased/T10_B30_S2000_DB_2000_eps.csv'
T10_B30_S2000_DB_2000_delta = '/home/gaia/Documents/SecondPaper/LogsDummies/LinkBased/T10_B30_S2000_DB_2000_delta.csv'



file = B_0_T1000_E5_mean
data = pd.read_csv(file)


F = data.to_numpy()
y = np.arange(10,110,10)
x = np.arange(1,11,1)
X,Y = np.meshgrid(x,y)
fig = plt.figure(figsize=(20,20))
ax = fig.add_subplot(111, projection='3d')

# Plot a 3D surface
ax.plot_surface(X, Y, F, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=1, antialiased=True)
ax.set_zlim(0,14)
ax.zaxis.set_tick_params(labelsize=20)
#ax.set_zticks([0, 2,4,6,8,10,12,14], fontsize = 16)
ax.set_ylabel('$Width$', fontsize = 20, labelpad=15)
ax.set_xlabel('$Layers$', fontsize = 20, labelpad=10)
ax.set_zlabel('Entropy', fontsize = 20, labelpad=15)
plt.yticks(fontsize=20)
plt.xticks(fontsize=20)
string_to_plot = os.path.basename(file)
#ax.set_title("30% corruption, traffic load = 1000, E2E=5")

plt.show()
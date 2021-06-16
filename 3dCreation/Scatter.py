from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


fig = plt.figure()

# syntax for 3-D projection
ax = plt.axes(projection='3d')

# defining axes
NoCorruption = '/home/gaia/Documents/DARPA/Internal/Logs/Optimization/textcsv.csv'
Q_25_B0_1_e2e1 = '/home/gaia/Documents/SecondPaper/Logs/Q0_25_b_01(E2E1).csv'
Median_B0_1e2e1 = '/home/gaia/Documents/SecondPaper/Logs/Q0_5_b_01(E2E1).csv'
data = pd.read_csv(Median_B0_1e2e1)

F = data.to_numpy()
y = np.arange(10,110,10)
x = np.arange(1,11,1)
X,Y = np.meshgrid(x,y)


ax.scatter(X, Y, F )

# syntax for plotting
#ax.set_title('3d Scatter plot geeks for geeks')
plt.show()
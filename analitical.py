import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

#Given data.

L=100
h=1


x = np.linspace(0, L, 100)
y = x.copy().T
X = np.arange(0, L+h, h)
Y = np.arange(0, L+h, h)
Z = np.zeros(int(L/h)+1)
X, Y = np.meshgrid(X, Y)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

for i in range(1, 1000 + 1, 2):
    z_y = np.sin(np.pi * Y * i / L)
    if i>=220:
        #to avoid overflow
        z_x = 200 * np.exp(-np.pi * i * X/L) / ( np.pi * i )
    else:
        a = 200 / ( np.pi * i * (np.sinh(np.pi*i) ) )
        z_x = a * ( np.exp( np.pi*i*(1-X/L) ) - np.exp( np.pi*i* (-1+X/L) ) )
    
    Z=Z+z_y*z_x


# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, alpha = 0.5,
                       linewidth=0, antialiased=False)

# Add the contour. 

CS=ax.contour(X, Y, Z, zdir='z', offset=0, cmap=cm.coolwarm)
ax.clabel(CS,inline=True, fontsize=10)


# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()


"""The SIRS model for the epidemics spreading 
0 = Susceptible
1 = Infected
2 = Recovered
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import sys
matplotlib.use('qt5agg')

class SIRS_model():
    def __init__(self, n):
        self.n = n

    def create_arr(self):
        return np.random.randint(0, 3, size=(self.n, self.n))


    def one_sweep(self, arr, p1, p2, p3):
        #arr = self.create_arr()
        for k in range((self.n)**2):
            i, j =np.random.randint(0, self.n), np.random.randint(0, self.n)
            if arr[i,j] == 0: 
                if (arr[(i+1)%self.n, j] == 1) | (arr[(i-1)%self.n, j] == 1) | (arr[i, (j+1)%self.n] == 1) | (arr[i, (j-1)%self.n] == 1):
                    ran = np.random.uniform()
                    if ran <= p1:
                        arr[i, j] = 1
            elif arr[i,j] == 1:
                if np.random.uniform() < p2:
                    arr[i, j] = 2
            elif arr[i, j] == 2:
                if np.random.uniform() < p3:
                    arr[i, j] = 0
        return arr

    def metropolis_sweep(self, p1, p2, p3):
        arr = self.create_arr()

        fig, ax = plt.subplots()
        fig.canvas.mpl_connect("close_event", lambda x: sys.exit())

        for i in range(1000):
            arr = self.one_sweep(arr, p1, p2, p3)
            ax.cla()   #clears the figure plot to plot the next animation
            ax.imshow(arr, animated=True, clim=[0,2])  #animates the spin lattice
            fig.canvas.draw()
            plt.pause(0.01)



def main():
    a = SIRS_model(50)
    a.metropolis_sweep(0.5, 0.5, 0.5)
main()
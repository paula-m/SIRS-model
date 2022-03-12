"""The SIRS model for the epidemics spreading 
0 = Susceptible = susceptible
1 = Infected = yellow
2 = Recovered = red
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import sys
matplotlib.use('qt5agg')
import csv
import random

class SIRS_model():
    def __init__(self, n):
        self.n = n  #the number of sites N lattice

    def create_arr(self):
        return np.random.randint(0, 3, size=(self.n, self.n))   #creates random array for the initial consdition


    def one_sweep(self, arr, p1, p2, p3):
        #one sweep for iteration
        for k in range((self.n)**2):
            i, j =np.random.randint(0, self.n), np.random.randint(0, self.n)
            if arr[i,j] == 0: #checks if susceptible. If yes then uses the condition that if there is infected next then the cell becomes infected
                if (arr[(i+1)%self.n, j] == 1) | (arr[(i-1)%self.n, j] == 1) | (arr[i, (j+1)%self.n] == 1) | (arr[i, (j-1)%self.n] == 1):
                    ran = np.random.uniform()
                    if ran <= p1:
                        arr[i, j] = 1
            elif arr[i,j] == 1: #if infected becomes recovered with prob p2
                if np.random.uniform() < p2:
                    arr[i, j] = 2
                else:
                    arr[i,j] = 1
            elif arr[i, j] == 2:    #if recovered becomes susceptible with prob p3
                if np.random.uniform() < p3:
                    arr[i, j] = 0
        return arr  #returns array

    def metropolis_sweep(self, p1, p2, p3):
        arr = self.create_arr() #creates random array

        fig, ax = plt.subplots()
        fig.canvas.mpl_connect("close_event", lambda x: sys.exit())

        avr = []    #list for no of infected sites
        avr_pt2 = []    #list for squared no of infected sites
        for i in range(2500):
            arr = self.one_sweep(arr, p1, p2, p3)
        
            #code for plotting of animation
            ax.cla()   #clears the figure plot to plot the next animation
            ax.imshow(arr, animated=True, clim=[0,2], cmap='RdYlGn')  #animates the spin lattice
            fig.canvas.draw()
            plt.pause(0.01)
            """
            #code for calculation if not needed comment out
            if i > 200:
                arrlist = arr.flatten().tolist()    #the array is flattened to the list to use count function rather than iteration over array 
                no_infected_sites = arrlist.count(1)    #counts no of infected sites
                avr.append(no_infected_sites)   #appends normal no of infected sites to list
                avr_pt2.append((no_infected_sites)**2)  #appends the square of each infected site for var calc
        
        #code for saving calc if not needed comment out
        finding_avrgs = self.saving_and_cal_avrgs(avr, avr_pt2, p1, p3)
        """

    def saving_and_cal_avrgs(self, avr, avr_pt2, p1, p3):
        av = np.mean(np.array(avr))    #average of I i.e. <I> with no of times and not lattice pts.
        fraction_inf_sites = av/(self.n**2)   #fraction of infected sites
        av_sq = np.mean(np.array(avr_pt2))     #average of squared infections
        var = (av_sq - av**2)/(self.n**2)   #variance of the infected sites
        error = self.bootstrap(avr)     #error calculation
        
        #code for saving of the data to datafile, only change between plots has been different file name
        f = open("average4.csv", "a+")
        writer = csv.writer(f)
        writer.writerow((p1, p3, fraction_inf_sites, var, error))
        f.close()

    def immunity(self, arr, pi):
        #code for immunity
        #we iterate over array and then add immunity based on probability
        for i in range(self.n):
            for j in range(self.n):
                if np.random.uniform() < pi:
                    arr[i, j] = 3   #immunity fraction
        return arr
    
    def metropolis_immunity(self, p1, p2, p3, p_imm):
        arr = self.create_arr()

        fig, ax = plt.subplots()
        fig.canvas.mpl_connect("close_event", lambda x: sys.exit())

        arr = self.immunity(arr, p_imm)

        #list for immunity calculation
        #avr = []
        #imm = []
        for i in range(3100):
            arr = self.one_sweep(arr, p1, p2, p3)

            #code for saving the immunity fraction
            #if i > 100:
            #    arrlist = arr.flatten().tolist()
            #    no_infected_sites = arrlist.count(1)
            #    avr.append(no_infected_sites)
            #    no_immune = arrlist.count(3)
            #    imm.append(no_immune)
            

            ax.cla()   #clears the figure plot to plot the next animation
            ax.imshow(arr, animated=True, clim=[0,3], cmap='RdYlGn')  #animates the spin lattice
            fig.canvas.draw()
            plt.pause(0.01)
        
        #av = np.average(avr)    #average of I i.e. <I> with no of times and not lattice pts.
        
        """
        code for immunity saving
        av_im = np.average(imm)
        fraction_inf_sites = av/(self.n**2)   #fraction of infected sites
        immune_fract = av_im/(self.n**2)
        
        f = open("immunity.csv", "a+")
        writer = csv.writer(f)
        writer.writerow((fraction_inf_sites, immune_fract))
        f.close()
        """


    def bootstrap(self, arr):
        """Method for calculating errors using bootstrap"""
        tot_sample = []
        for j in range(1000):
            new_sample = []
            for i in range(len(arr)):
                ind = random.randrange(len(arr))
                new_sample.append(arr[ind])
            var = ((np.mean(np.array(new_sample)**2)) - (np.mean(np.array(new_sample)))**2)/self.n**2
            tot_sample.append(var)
        error = np.sqrt((np.mean(np.array(tot_sample)**2)) - (np.mean(np.array(tot_sample))**2))
        return error


def main():
    
    lat_size = input("Lattice size: ")
    a = SIRS_model(int(lat_size))

    variables = input("Please give type of system: waves, dyn eql, abs, immunity, other: ")
    if variables == "waves":
        #a.metropolis_sweep(0.8, 0.1, 0.01)  #waves for 100 by 100
        a.metropolis_sweep(0.7, 0.1, 0.015)
    elif variables == "dyn eql":
        a.metropolis_sweep(0.5, 0.5, 0.5)   #dynamical equilibrium
    elif variables == "abs":
        a.metropolis_sweep(0.5, 0.6, 0.1)  #absorbing state
    elif variables == "immunity":
        p1, p2, p3, pim = input("p1 "), input("p2 "), input("p3 "), input("p_im ")
        a.metropolis_immunity(float(p1), float(p2), float(p3), float(pim))
    elif variables == "other":
        p1, p2, p3 = input("p1 "), input("p2 "), input("p3 ")
        a.metropolis_sweep(float(p1), float(p2), float(p3))

main()
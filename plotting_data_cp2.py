import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import csv
from scipy.optimize import curve_fit

class reading_files():
    def plot_histogram(self):
        col_name = ["value", "time"]
        df = pd.read_csv("acttime.csv", names = col_name)
        time_dat = (df["time"])
        
        n_bins = 10
        plt.hist(time_dat, n_bins, rwidth = 0.7, color = 'purple')
        plt.xlabel("The time taken for equilibrium to be reached in metropolis sweeps")
        plt.ylabel("The number of instances")
        plt.title("The histogram showing the time taken for each equilibrium to be reached.")
        plt.show()

    def line(self, x, a, b):
        return a*x + b

    def plot_com_data(self):
        """Method for plotting of the data for the com for glider"""
        col_name = ["time", "x", "y"]
        df = pd.read_csv("com_glider.csv", names = col_name)
        x = (df["x"])
        y = (df["y"])
        time = (df["time"])

        popt, _ = curve_fit(self.line, time[0:182], x[0:182])   #fitting of line to find velocity
        a,b = popt
        plt.scatter(time[0:182], x[0:182], label="y = %.5f * x + %.5f" %(a,b), color="purple", s=10)
        plt.legend()
        plt.title("The x velocity vs the time")
        plt.xlabel("Time")
        plt.ylabel("X velocity")
        plt.show()

        popt, _ = curve_fit(self.line, time[0:182], y[0:182])
        a,b = popt
        plt.scatter(time[0:182], y[0:182], label="y = %.5f * x + %.5f" %(a,b), color="green", s=10)
        plt.legend()
        plt.title("The y velocity vs the time")
        plt.xlabel("Time")
        plt.ylabel("Y velocity")
        plt.show()

    def color_map(self):
        """Method which plots color map for the phase transition"""

        col_name = ["p1", "p3", "fraction", "variance"] #columns for pd file
        df = pd.read_csv("avrg.csv", names = col_name)  #reading file
        time_dat = df["fraction"].tolist()  #gets list of the data for the colorbar

        fract = np.array(time_dat).reshape((21,21))
        fract = np.transpose(fract) #reshapes and transposes the data to switch axis

        x = np.arange(0, 1.05, 0.05)
        X, Y = np.meshgrid(x, x)
    
        fig, ax = plt.subplots()
        clb = ax.pcolormesh(X, Y, fract)
        plt.title("The phase diagram for absorbing and active phases")
        cbar = fig.colorbar(clb)
        cbar.set_label("The fraction of infected ")
        plt.xlabel("p1")
        plt.ylabel("p3")
        plt.show()

    def color_map_var(self):
        """Method which plots color map for variance"""

        col_name = ["p1", "p3", "fraction", "variance"] #columns for pd file
        df = pd.read_csv("avrg.csv", names = col_name)  #reading file
        time_dat = df["variance"].tolist()  #gets list of the data for the colorbar

        fract = np.array(time_dat).reshape((21,21))
        fract = np.transpose(fract) #reshapes and transposes the data to switch axis

        x = np.arange(0, 1.05, 0.05)
        X, Y = np.meshgrid(x, x)
    
        fig, ax = plt.subplots()
        clb = ax.pcolormesh(X, Y, fract)
        plt.title("The phase diagram for variance")
        cbar = fig.colorbar(clb)
        plt.xlabel("p1")
        plt.ylabel("p3")
        plt.show()


    def detailed_plot(self):
        col_name = ["p1", "p3", "fraction", "variance", "error"]
        df = pd.read_csv("average3.csv", names = col_name)
        p1 =  df["p1"].tolist()
        var = df["variance"].tolist()
        err = df["error"].tolist()
        var = np.array(var)

        plt.errorbar(p1, var, yerr=err, fmt='none')
        plt.scatter(p1, var, color = "purple", s = 15)
        plt.title("Graph showing variance vs p1")
        plt.xlabel("p1")
        plt.ylabel("variance")
        plt.show()

    def immunity_plot(self):
        col_name = ["infected", "immune"]
        df = pd.read_csv("immunity2.csv", names = col_name)
        inf_d1 = df["infected"].tolist()
        imm1 = df["immune"].tolist()

        d1 = pd.read_csv("immunity.csv", names = col_name)
        inf2 = d1["infected"].tolist()
        imm2 = d1["immune"].tolist()

        d2 = pd.read_csv("immunity1.csv", names = col_name)
        inf3 = d2["infected"].tolist()
        imm3 = d2["immune"].tolist()

        d3 = pd.read_csv("immunity3.csv", names = col_name)
        inf4 = d3["infected"].tolist()
        imm4 = d3["immune"].tolist()

        d4 = pd.read_csv("immunity4.csv", names = col_name)
        inf5 = d4["infected"].tolist()
        imm5 = d4["immune"].tolist()

        err2 = []
        for i in range(len(inf2)):
            avr_vals = []
            avr_vals.append(inf_d1[i])
            avr_vals.append(inf2[i])
            avr_vals.append(inf3[i])
            avr_vals.append(inf4[i])
            avr_vals.append(inf5[i])

            avr = np.mean(avr_vals)
            sqr = np.array(avr_vals)**2
            avrsq = np.mean(sqr)

            errs = np.sqrt((avrsq - avr**2)/(len(avr_vals)-1))
            err2.append(errs)
        #print(err2)
        plt.errorbar(imm1, inf_d1, yerr=err2, color = "purple", fmt = "none")
        plt.scatter(imm1, inf_d1, s = 5)
        plt.xlabel("Fraction of immunity")
        plt.ylabel("Fraction of infection")
        plt.title("Graph showing fraction of immunity vs fraction of infection")
        plt.show()

        

def main():
    a = reading_files()
    inp = input("plot: com, hist, cmap, var, immunity: ")
    if inp == "com":
        a.plot_com_data()
    elif inp == "hist":
        a.plot_histogram()
    elif inp == "cmap":
        a.color_map()
    elif inp == "var":
        a.color_map_var()
        a.detailed_plot()
    elif inp == "immunity":
        a.immunity_plot()
main()
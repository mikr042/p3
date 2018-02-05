#! /usr/bin/python2

#########################################################
#                                                       #
#   Vorlage fuer Plots                                  #
#   Anselm Baur                                         #
#   Oktober 2016                                        #
#                                                       #
#########################################################

#%% Initialisierung
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from scipy.optimize import curve_fit

# Daten aus Datei
raw_data_file = "../messwerte/messwerte_1_2.csv"
# Float Werte
s_200, s_500, s_1000, dicke = np.loadtxt(raw_data_file, delimiter=",", unpack = True, usecols = tuple(range(1,5))) # usecols = (2, 3))
# Strings
material = np.core.defchararray.decode(np.loadtxt(raw_data_file, dtype='|S13', delimiter=",", unpack = True, usecols = [0]))


y_raw = np.zeros([5,3])
x_raw = np.array([s_200, s_500, s_1000]).transpose()

for i in range(0,5):
    y_raw[i] = np.array([0.2, 0.5, 1])*9.81


label = material

print(label)
print(y_raw)
for i in range(0,3):
    print(x_raw[i])


#%% Fit Funktion
def func(x, a, b):
     return x*a+b

# Achsenausschnitt auf der x und y Achse
x_scal = np.array([0,22])
y_scal = np.array([0,11])



# FIT
pcov = np.zeros([5,2,2])
perr = np.zeros([5,2])
popt = np.zeros([5,2])
m = np.zeros(5) 
y_0 = np.zeros(5)
x_fit = np.arange(0,23)
y_fit = np.zeros([5,x_fit.size])

for i in range (0,5):
    popt[i], pcov[i] = curve_fit(func, x_raw[i], y_raw[i])
    y_fit[i] = func(x_fit, popt[i][0], popt[i][1])
    m[i] = np.round(popt[i][0], 3)
    y_0[i] = np.round(popt[i][1], 3)
    perr[i] = np.sqrt(np.diag(pcov[i]))

print("Fehler")
print(perr)

#%% Ergebnisse:

print("\n\n####### Ergebnisse: ########\n")
for i in range(0,5):
    print(label[i] + ": \t" + str(m[i]) + " +/- " + str(perr[i][0]) + ", E = " + str(3*0.42**2*m[i]*(6*0.42+4*1.92)/(4*(dicke[i]*10**(-3))**3*0.025)*10**2*10**(-9)))        

#%% Plots
# FIGURE
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(1,1,1)
ax.clear()



###################################### Hier nur Style #################################
xmajor_ticks = np.arange(x_scal[0],x_scal[1]+0.1,(x_scal[1]-x_scal[0])/11)
xminor_ticks = np.arange(x_scal[0],x_scal[1],(x_scal[1]-x_scal[0])/110)

ymajor_ticks = np.arange(y_scal[0],y_scal[1]+0.01,(y_scal[1]-y_scal[0])/11)
yminor_ticks = np.arange(y_scal[0],y_scal[1],(y_scal[1]-y_scal[0])/110)

ax.set_xlim(x_scal[0],x_scal[1])
ax.set_ylim(y_scal[0], y_scal[1])
ax.axhline(linewidth=0.5, color="k")
ax.axvline(linewidth=0.5, color="k")
# Schriftgroesse der Achsenwerte
plt.setp(ax.get_xticklabels(), fontsize=18)
plt.setp(ax.get_yticklabels(), fontsize=18)

ax.set_xticks(xmajor_ticks)
ax.set_xticks(xminor_ticks, minor=True)
ax.set_yticks(ymajor_ticks)                                                       
ax.set_yticks(yminor_ticks, minor=True)
ax.tick_params("both", length=10, which="major")
ax.tick_params("both", length=5, which="minor")

ax.grid(which="major", alpha=0.5)
######################################################################################

#ax.set_title("Diagrammtitel", fontsize=18)
ax.set_ylabel(r'Kraft $F$ in N', fontsize=18)
ax.set_xlabel(r'Auslenkung $s$ in cm', fontsize=18)

color = ['b','r','g','k','c']

# Plot der Messwerte und der Fits
for i in range(0,5):
    ax.plot(x_fit, y_fit[i], color[i], linestyle="solid", linewidth = 0.5, label="Fit " + label[i]) # Fit Plot
    ax.errorbar(x_raw[i], y_raw[i], xerr=0.2, yerr=0.00981, fmt='o', c=color[i], label=label[i]) # Messdatenus

# Legende
ax.legend(loc="lower right", prop={'size':16}).get_frame().set_linewidth(0.5)

# Text im Plot
#ax.text(19.7, 245, 'f' + ' = '+str(m_1)+r'$\cdot$s - '+str(np.abs(y_0_1)), fontsize=16)
plt.show()

# Save figure
fig.savefig('../fig/figure_1_2_laserspiegel.eps')


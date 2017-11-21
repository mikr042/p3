#! /usr/bin/python2

#########################################################
#                                                       #
#   Vorlage fuer Plots                                  #
#   Anselm Baur                                         #
#   Oktober 2016                                        #
#                                                       #
#########################################################

import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from scipy.optimize import curve_fit

# Daten aus Datei
raw_data_file = "../messwerte/messwerte_1_2_2.csv"
l_r, t_1, t_2 = np.loadtxt(raw_data_file, delimiter=",", unpack = True) # usecols = (2, 3))


x_raw = l_r
y_raw_1 = t_1+0.023
y_raw_2 = t_2+0.023

label = "Messwerte"

print(label + ":")
print(y_raw_1)
print(y_raw_2)
print(x_raw)

def func(x, a, b):
     return x*a+b

# Achsenausschnitt auf der x und y Achse
y_scal = np.array([15.6,16.6])
x_scal = np.array([59, 69])



# FIT
popt, pcov = curve_fit(func, x_raw, y_raw_1)
x_fit = np.arange(59,70,1)
y_fit_1 = func(x_fit, popt[0], popt[1])
m_1 = np.round(popt[0], 3)
y_0_1 = np.round(popt[1], 3)

mask = ((x_raw[:]>=63) & (x_raw[:]<= 64))
popt, pcov = curve_fit(func, x_raw[mask], y_raw_2[mask])
y_fit_2 = func(x_fit, popt[0], popt[1])
m_2 = np.round(popt[0], 3)
y_0_2 = np.round(popt[1], 3)


# FIGURE
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(1,1,1)
ax.clear()



###################################### Hier nur Style #################################
xmajor_ticks = np.arange(x_scal[0],x_scal[1]+0.1,(x_scal[1]-x_scal[0])/10)
xminor_ticks = np.arange(x_scal[0],x_scal[1],(x_scal[1]-x_scal[0])/100)

ymajor_ticks = np.arange(y_scal[0],y_scal[1]+0.01,(y_scal[1]-y_scal[0])/10)
yminor_ticks = np.arange(y_scal[0],y_scal[1],(y_scal[1]-y_scal[0])/100)

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
ax.set_xlabel("Abstand Schneiden "+ "[cm]", fontsize=18)
ax.set_ylabel("Zeit " + r'$t$' + "[s]", fontsize=18)

# Plot der Messwerte und der Fits
#ax.plot(x_raw, y_raw, linestyle="dotted")
ax.plot(x_fit, y_fit_1, "r", linestyle="dotted", label="Fit feste Schneide") # Fit Plot
ax.plot(x_fit, y_fit_2, "g", linestyle="dotted", label="Fit bewegliche Schneide") # Fit Plot
ax.scatter(x_raw,y_raw_1, s=60, c="r", label="feste Schneide") # Messdaten
ax.scatter(x_raw,y_raw_2, s=60, c="g", label="bewegliche Schneide") # Messdaten

# Legende
ax.legend(loc="upper right", prop={'size':16}).get_frame().set_linewidth(0.5)

# Text im Plot
ax.text(61.7, 16.22, 't'+r'$_2$' + ' = '+str(m_2)+'x + '+str(y_0_2), fontsize=16)
ax.text(66.5, 16.05, 't'+r'$_1$' + ' = '+str(m_1)+'x + '+str(y_0_1), fontsize=16)
plt.show()

# Save figure
fig.savefig('../fig/figure_1_2_reduziert.eps')


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
raw_data_file = "../messwerte/messwerte_2_2.csv"
n, p, F_80, F_56 = np.loadtxt(raw_data_file, delimiter=",", unpack = True) # usecols = (2, 3))


x_raw = p-5
y_raw_1 = F_80-0.02
y_raw_2 = F_56-0.02
label_1 = "A = 201.1 cm"+r'$^2$' +" gemessen"
label_2 = "A = 98.5 cm"+r'$^2$' +" gemessen"

print(label_1 + ":")
print(y_raw_1)
print(x_raw)
#y_raw = np.exp(x)/10.

def func(x, a, b):
     return x*a+b

# Achsenausschnitt auf der x und y Achse
x_scal = np.array([0,130])
y_scal = np.array([0, 0.55])



# FIT
popt_1, pcov_1 = curve_fit(func, x_raw, y_raw_1)
x_fit = np.arange(0,140,10)
y_fit_1 = func(x_fit, popt_1[0], popt_1[1])
a_1 = round(popt_1[0], 4)
b_1 = round(popt_1[1], 4)

popt_2, pcov_2 = curve_fit(func, x_raw, y_raw_2)
y_fit_2 = func(x_fit, popt_2[0], popt_2[1])
a_2 = round(popt_2[0], 4)
b_2 = round(popt_2[1], 4)


# FIGURE
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(1,1,1)
ax.clear()



###################################### Hier nur Style #################################
xmajor_ticks = np.arange(x_scal[0],x_scal[1]+0.1,(x_scal[1]-x_scal[0])/13)
xminor_ticks = np.arange(x_scal[0],x_scal[1],(x_scal[1]-x_scal[0])/130)

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

#ax.set_title("Diagrammtitel", fontsize=16)
ax.set_xlabel("Staudruck "+r'$p_{dyn}$'+" [Pa]", fontsize=18)
ax.set_ylabel("Luftwiderstandskraft " + r'$F_W$' + " [N]", fontsize=18)

# Plot der Messwerte und der Fits
ax.scatter(x_raw,y_raw_1, s=60, c="r", label=label_1) # Messdaten
ax.scatter(x_raw,y_raw_2, s=60, c="g", label=label_2) # Messdaten
ax.plot(x_fit, y_fit_1, "r", label="Fit") # Fit Plot
ax.plot(x_fit, y_fit_2, "g", label="Fit") # Fit Plot

# Legende
ax.legend(loc="upper left", prop={'size':16}).get_frame().set_linewidth(0.5)

# Text im Plot
ax.text(3, 0.23, r'$F_W$'+" = "+str(a_1)+r'$p_{dyn}$'+ " - " + str(abs(b_1)), fontsize=16)
ax.text(67, 0.12, r'$F_W$'+" = "+str(a_2)+r'$p_{dyn}$'+ " - " + str(abs(b_2)), fontsize=16)
#ax.text(2.3, 15.7, 'f = '+str(f_0)+'')
plt.show()

# Save figure
fig.savefig('../fig/figure_2_2_staudruck.eps')


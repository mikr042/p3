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
raw_data_file = "../messwerte/messwerte_1_1_abstand.csv"
l, r_0, r_1, r_2, r_3, r_4, r_5 = np.loadtxt(raw_data_file, delimiter=",", unpack = True) # usecols = (2, 3))


x_raw = l+1.5
y_raw = [r_0-5, r_1-5, r_2-5, r_3-5, r_4-5, r_5-5]
#y_raw_1 = r_1
#y_raw_2 = r_2
#y_raw_3 = r_3
#y_raw_4 = r_4
#y_raw_5 = r_5

label = [	"Abweichung Achse 0 cm", 
		"Abweichung Achse 1 cm",
		"Abweichung Achse 2 cm",  
		"Abweichung Achse 3 cm", 
		"Abweichung Achse 4 cm",
		"Abweichung Achse 5 cm" ]



#print(label + ":")
#print(y_raw)
#print(x_raw)
#y_raw = np.exp(x)/10.

def func(x, a, b):
     return x*a+b

# Achsenausschnitt auf der x und y Achse
x_scal = np.array([10,35])
y_scal = np.array([20, 120])



# FIT
#popt, pcov = curve_fit(func, x_raw, y_raw)
#x_fit = np.arange(-20,21,1)
#y_fit = func(x_fit, popt[0], popt[1])
#f_0 = round(popt[0], 4)
#h_0 = round(popt[1], 4)


# FIGURE
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(1,1,1)
ax.clear()



###################################### Hier nur Style #################################
xmajor_ticks = np.arange(x_scal[0],x_scal[1]+0.1,(x_scal[1]-x_scal[0])/5)
xminor_ticks = np.arange(x_scal[0],x_scal[1],(x_scal[1]-x_scal[0])/50)

ymajor_ticks = np.arange(y_scal[0],y_scal[1]+0.1,(y_scal[1]-y_scal[0])/5)
yminor_ticks = np.arange(y_scal[0],y_scal[1],(y_scal[1]-y_scal[0])/50)

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


line_style = [ "o", "v", "x", "s", "D", ">"]

#ax.set_title("Diagrammtitel", fontsize=16)
ax.set_xlabel("Abstand " + r'$l$' + " [cm]", fontsize=18)
ax.set_ylabel("Staudruck " + r'$p_{dyn}$' + " [Pa]", fontsize=18)

for i in range(0,6):
	# Plot der Messwerte und der Fits
	ax.plot(x_raw, y_raw[i], marker=line_style[i], label=label[i]) # Fit Plot
	#ax.scatter(x_raw,y_raw[i], s=60, label=label[i]) # Messdaten
#ax.plot(x_fit_180, y_fit_180, "k", label="Fit") # Fit Plot

# Legende
#ax.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0., prop={'size':16}).get_frame().set_linewidth(0.5)
ax.legend( loc="lower", ncol=2,  prop={'size':16}).get_frame().set_linewidth(0.5)

# Text im Plot
#ax.text(1.5, 0.55, r'$F_A$'+" = "+str(f_0)+r'$\alpha$' + r'$+$' + str(h_0), fontsize=16)
#ax.text(2.3, 15.7, 'f = '+str(f_0)+'')
plt.show()

# Save figure
fig.savefig('../fig/figure_1_1_abstand.eps')


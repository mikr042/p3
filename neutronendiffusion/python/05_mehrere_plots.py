#! /usr/bin/python3

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

def get_csv_data(file, delimiter):
    #Anzahl Zeilen
    with open(file) as f:
        line_num = sum(1 for _ in f)
    #Anzahl Spalten
    with open(file) as f:
        for line in f:
            col_num = len(line.split(delimiter))
            break
    
    data = np.empty((line_num-1,col_num))
    with open(file) as f:
        try:
            with open(file) as f:
                i = 0
                j = 0
                for line in f:
                    if not line.startswith('#'):
                        line = line.replace("\n","")
                        line = line.split(delimiter)
                        if not i:
                            header = line
                            i = 1
                            continue
                        k = 0
                        for item in line:
                            data[j][k] = float(item)
                            k+=1
                        j+=1
        except:
            print("Fehler beim Lesen der Datei " + file)
            
    if line_num-1 == j:
        return header, data
    else:   
        return header, data[:-(line_num-1-j)][:]
        
raw_data_file = "Offset.csv"
#t, temp_diff = np.loadtxt(raw_data_file, delimiter=";", unpack = True skiprows = 1) #usecols = (2, 3))
#header = np.core.defchararray.decode(np.loadtxt(raw_data_file, dtype='|S13', delimiter=";", unpack = True, usecols = [0]))
header, data = get_csv_data(raw_data_file, ";")

rows = len(data[:][:])
cols = len(data[0][:])

 
y_raw = np.zeros((rows,cols-1))
x_raw = np.zeros(rows)

#nur Werte
for i in range(0,rows):
    for j in range(0,cols-1):
        y_raw[i][j] = data[i][j+1]
    x_raw[i] = data[i][0]

label = header

print(label)
print(y_raw)
for i in range(0,1):
    print(x_raw[i])


#%% Fit Funktion
def func(x, a, b, c):
     return a*(1/(1+np.exp(-b*x)))+c

# Achsenausschnitt auf der x und y Achse
x_scal = np.array([-20,70])
y_scal = np.array([-2,1])



# FIT
pcov = np.zeros((cols-1,3,3))
perr = np.zeros([rows,cols-1,3])
popt = np.zeros((cols-1,3))
a = np.zeros(cols-1) 
b = np.zeros(cols-1)
c = np.zeros(cols-1)
x_fit = np.arange(-20,65)
y_fit = np.zeros([cols-1,x_fit.size])
p0 = [-1.75, -0.1, 0.25]


for i in range (0,cols-1):
    popt[i], pcov[i] = curve_fit(func, x_raw, np.transpose(y_raw)[i], p0)
    y_fit[i] = func(x_fit, popt[i][0], popt[i][1], popt[i][2])
    a[i] = np.round(popt[i][0], 3)
    b[i] = np.round(popt[i][1], 3)
    c[i] = np.round(popt[i][2], 3)
    perr[i] = np.sqrt(np.diag(pcov[i]))
#
#print("Fehler")
#print(perr)

#%% Ergebnisse:

#print("\n\n####### Ergebnisse: ########\n")
#for i in range(0,5):
#    print(label[i] + ": \t" + str(m[i]) + " +/- " + str(perr[i][0]) + ", E = " + str(0.42**3*m[i]/(4*(dicke[i]*10**(-3))**3*0.025)*10**3*10**(-9)))        

#%% Plots
# FIGURE
fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(1,1,1)
ax.clear()



###################################### Hier nur Style #################################
xmajor_ticks = np.arange(x_scal[0],x_scal[1]+0.1,(x_scal[1]-x_scal[0])/9)
xminor_ticks = np.arange(x_scal[0],x_scal[1],(x_scal[1]-x_scal[0])/90)

ymajor_ticks = np.arange(y_scal[0],y_scal[1]+0.01,(y_scal[1]-y_scal[0])/12)
yminor_ticks = np.arange(y_scal[0],y_scal[1],(y_scal[1]-y_scal[0])/120)

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
ax.set_ylabel(r'Temperaturoffset in $K$', fontsize=18)
ax.set_xlabel(r'Kalibriertemperatur', fontsize=18)

color = ['b','r','g','k','c']
color_marker = ['bs','rv','gX','kd','co']

# Plot der Messwerte und der Fits
for i in range(0,cols-1):
    ax.plot(x_fit, y_fit[i], color[i], linestyle="solid", linewidth = 0.5, label="Fit " + label[i+1]) # Fit Plot
    #ax.errorbar(x_raw[i], y_raw[i], xerr=0.02, yerr=0.00981, fmt='o', c=color[i], label=label[i]) # Messdatenus
    ax.plot(x_raw,np.transpose(y_raw)[i], ""+color_marker[i], label=label[i+1])


# Legende
ax.legend(loc="upper right", prop={'size':16}).get_frame().set_linewidth(0.5)

# Text im Plot
#ax.text(19.7, 245, 'f' + ' = '+str(m_1)+r'$\cdot$s - '+str(np.abs(y_0_1)), fontsize=16)
plt.show()

# Save figure
fig.savefig('offset.eps')


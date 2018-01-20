import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
from scipy.odr import *


import math as m
k_Wert=[0.579,1.157,1.736,2.314,2.893,3.471]
Lsg,Lsg_err=[],[]
filelist = ['akustisch1','akustisch2','akustisch3','akustisch4','akustisch5','akustisch6']
matplotlib.rc('text', usetex=True)
k=1
for file in filelist: # Alles, was jetzt kommt, wird fuer jedes Textdokument wiederholt, welches in der filelist drinsteht.
    # Einlesen der Daten aus der Textdatei
    with open('{}.txt'.format(file)) as f:
        print ("Akustisch " + str(k))
        
        corr=m.sin(k*m.pi*7/13)/(m.sin(k*m.pi*8/13))
        
        print ("Korrekturfaktor: "+str(corr))
        
        result,x_value, y_value = [],[],[] # Definiert leere arrays x_value, y_value, x_error und y_error
        for line in f: #liest 4 Zahlen pro Zeile, ersetzt Komma durch Punkt, sofern vorhanden.
            x_value.append( float(line.split()[0].replace(',','.')) )
            y_value.append( float(line.split()[1].replace(',','.')) )
        
        for j in range(0,len(x_value)):
            result.append(y_value[j]/x_value[j]/corr)
        Lsg.append(abs(np.mean(result)))
        Lsg_err.append(np.var(result))
        print ("Mittelwert :"+str(abs(np.mean(result))))
        print ("Standardabweichung :"+str(np.var(result)))
        print
        k=k+1
f.close()
Lsg2,Lsg_err2=[],[]
filelist2 = ['optisch1','optisch2','optisch3','optisch4','optisch5','optisch6']

matplotlib.rc('text', usetex=True)
k=1
for file in filelist2: # Alles, was jetzt kommt, wird fuer jedes Textdokument wiederholt, welches in der filelist drinsteht.

    # Einlesen der Daten aus der Textdatei

    with open('{}.txt'.format(file)) as f:
        print ("Optisch " + str(k))
        
        corr=m.sin(k*m.pi*7/13)/(m.sin(k*m.pi*8/13))
        
        print ("Korrekturfaktor: "+str(corr))
        
        result,x_value, y_value = [],[],[] # Definiert leere arrays x_value, y_value, x_error und y_error

        for line in f: #liest 4 Zahlen pro Zeile, ersetzt Komma durch Punkt, sofern vorhanden.

            x_value.append( float(line.split()[0].replace(',','.')) )

            y_value.append( float(line.split()[1].replace(',','.')) )

        
        for j in range(0,len(x_value)):
            result.append(y_value[j]/x_value[j]/corr)
        Lsg2.append(-abs(np.mean(result)))
        Lsg_err2.append(np.var(result))
        print ("Mittelwert :"+str(-abs(np.mean(result))))
        print ("Standardabweichung :"+str(np.var(result)))
        print
        k=k+1
f.close()
file1 = open('lsgvektoren','w')
for element in Lsg:
    file1.write(str(element)+'&')
file1.write(r'\\'+'\n')
for element in Lsg_err:
    file1.write(str(element)+'&')
file1.write(r'\\'+'\n')

for element in Lsg2:
    file1.write(str(element)+'&')
file1.write(r'\\'+'\n')
for element in Lsg_err2:
    file1.write(str(element)+'&')
file1.write(r'\\'+'\n')
file1.close()
plt.errorbar(k_Wert, Lsg,Lsg_err,linestyle='None', marker='o', color='black', markersize=5, label='akustischer Zweig')

plt.errorbar(k_Wert, Lsg2,Lsg_err2,linestyle='None', marker='o', color='red', markersize=5, label='optischer Zweig')

plt.legend(loc='best', numpoints = 1)
plt.axis([0.0, 4.0, -6, 2]) 

plt.xlabel("k in 1/m", size=15)

plt.ylabel("Verhaeltnis Schwingungsamplituden", size=15)

plt.grid(True)

plt.savefig('plot_{}.png'.format(file), dpi=800)

plt.savefig('plot_{}.pdf'.format(file), dpi=800)
plt.show()
plt.close()

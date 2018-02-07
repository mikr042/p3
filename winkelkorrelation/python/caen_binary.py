import struct
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import peakutils

import pdb

# read first waveform file
fileList = ['cobalt_90_1_', 'cobalt_90_2_', 'cobalt_90_3_', 'cobalt_135_1_', 'cobalt_135_2_', 'cobalt_135_3_', 'cobalt_180_1_', 'cobalt_180_2_', 'cobalt_180_3_']

n1b = 1646
n2b = 1778
ncb = 6

nDet1 = []
nDet2 = []
nC = []

s = ''
for f in fileList:

    nevent1 = 0
    xList1 = []
    tList1 = []
    tDAQ1  = []
    event1 = []

    fileName = f + 'channel0.dat'
    f1 = open(fileName, "rb")
    notEOF = True
    #pdb.set_trace()
    while notEOF and nevent1 < 1000000000:

        # read header: record, boardID, channel, pattern, event, time_ns
        #pdb.set_trace()
        s = f1.read(24)
        if len(s) != 24:
            notEOF = False
            break
        record,boardID,channel,pattern,evt,time_ns = struct.unpack("<LLLLLL", s)

        # read data: record = Byte length of the waveform event (16 bit per sample) + 24 (6*4Byte) header length 
        s = f1.read(record-24)
        if len(s) != (record-24):
            notEOF = False
            break
        data = struct.unpack("<"+str((record-24)/2)+"H", s)
        
        # determine the baseline signal (average of first 10 samples)
        x0=0
        for i in range(10):
            x0 = x0 + data[i]
        x0 = x0/10.
        
        # find the maximum peak in the waveform event (gliding average of 10 samples)
        imax = 0
        xmax = 0.
        xsum = 0.
        for i in range(10,(record-24)/2):
            xsum = xsum + data[i-10] - data[i]
           #xsum = data[i] - x0
            if xmax < xsum:
                xmax = xsum
                imax = i
        xList1.append(xmax)
        tList1.append(imax * 8)
        tDAQ1.append(time_ns * 8)
        event1.append(evt)
        nevent1 = nevent1 + 1

    f1.close()
        
    # read second waveform file
    
    nevent2 = 0
    xList2 = []
    tList2 = []
    tDAQ2  = []
    event2 = []
    
    f2 = open(f + "channel1.dat", "rb")
    notEOF = True
    
    while notEOF and nevent2 < 10000000:
        
        # read header: record, boardID, channel, pattern, event, time_ns
        s = f2.read(24)
        if len(s) != 24:
            notEOF = False
            break
        record,boardID,channel,pattern,evt,time_ns = struct.unpack("<LLLLLL", s)
        
        # read data: record = Byte length of the waveform event (16 bit per sample) + 24 (6*4Byte) header length 
        s = f2.read(record-24)
        if len(s) != (record-24):
            notEOF = False
            break
        data = struct.unpack("<"+str((record-24)/2)+"H", s)
        
        # determine the baseline signal (average of first 10 samples)
        x0=0
        for i in range(10):
            x0 = x0 + data[i]
        x0 = x0/10.
        
        # find the maximum peak in the waveform event (gliding average of 10 samples)
        imax = 0
        xmax = 0.
        xsum = 0.
        for i in range(10,(record-24)/2):
            xsum = xsum + data[i-10] - data[i]
            if xmax < xsum:
                xmax = xsum
                imax = i
        xList2.append(xmax)
        tList2.append(imax * 8)
        tDAQ2.append(time_ns * 8)
        event2.append(evt)
        nevent2 = nevent2 + 1

    f2.close()

    print "dataset: ", f
        
    natrium1 = [33482, 77266] #an peaks in messung anpassen
    natrium2 = [31372, 72805] #ebenso
    def ampl1(x):
        return 511 + (x - natrium1[0])*764/(natrium1[1] - natrium1[0])
    def ampl2(x):
        return 511 + (x - natrium2[0])*764/(natrium2[1] - natrium2[0])
    
    cutoff1 = 80418*0.6
    cutoff2 = 75788*0.6

    # plot results
    plt.subplot(121)
    n1, bins, patches1 = plt.hist(xList1, 1000, range=(0,100000))
    #plt.xlabel('energy (chn)')
    #plt.ylabel('events')
    #plt.title('Na-22')
    #plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
    #plt.axis([0, 100000, 0, 1.2*np.amax(n1[10:])])
    #plt.grid(True)
    plt.subplot(122)
    n2, bins2, patches2 = plt.hist(xList2, 1000, range=(0,100000))
    #plt.axis([0, 100000, 0, 1.2*np.amax(n2[10:])])
    #plt.grid(True)
    #plt.show()
    #######################
    
    x = np.array(range(1000))
    indices1 = peakutils.indexes(n1, thres=0.0015, min_dist=100)
    indices2 = peakutils.indexes(n2, thres=0.0015, min_dist=100)
    peaks_x1 = peakutils.interpolate(x, n1, ind=indices1, width=50)
    peaks_x2 = peakutils.interpolate(x, n2, ind=indices2, width=50)
    print "photopeaks: ", ampl1(peaks_x1[-1]*100), ampl2(peaks_x2[-1]*100)
    
    #ind1 =  peakutils.indexes(n1[400:], thres=0.7, min_dist=100)
    #p1 = peakutils.interpolate(x[400:], n1[400:], ind=ind1, width=50)
    #print p1
    
    # search for coincidences
    
    n1 = 0
    n2 = 0
    coinc1  = []
    eCoinc1 = []
    tCoinc1 = []
    coinc2  = []
    eCoinc2 = []
    tCoinc2 = []
    dtCoinc = []
    eSum    = []
    
    if len(xList1) != len(xList2):
        print "Warning: different event numbers"
    
    n1 = len([x for x in xList1 if x>cutoff1])
    n2 = len([x for x in xList2 if x>cutoff2])
    
    for i in xrange(len(xList1)):
        if tDAQ1[i] != tDAQ2[i]:
            print "different times in event ",i
        if abs(tList1[i] - tList2[i])< 200 and xList1[i]>cutoff1 and xList2[i]>cutoff2:
            coinc1.append(event1[i])
            eCoinc1.append(xList1[i])
            tCoinc1.append(tList1[i])
            coinc2.append(event2[i])
            eCoinc2.append(xList2[i])
            tCoinc2.append(tList2[i])
            dtCoinc.append(tList2[i]-tList1[i])
            eSum.append(xList1[i]+xList2[i])
    
    nCoinc = len(eCoinc1)
    
    print "Number of events: ", n1, n2, nCoinc
    #print tCoinc1[0:20], tCoinc2[0:20]
    
    #timing resolution for the coincidence
    nCoinc = len(eCoinc1)
    dt = [tCoinc1[i]-tCoinc2[i] for i in xrange(len(tCoinc1))]
    n, bins, patches1 = plt.hist(dt, bins=50, range=(-200,200), normed=True)
    std = np.std(dt)
    mean = np.mean(dt)
    #p = np.linspace(-200, 200, 40000)
    #indx = (np.abs(n1 - np.std(n1))).argmin()
    #print indx-200
    
    #plt.plot(bins, 1/(std * np.sqrt(2 * np.pi))*np.exp( - (bins - mean)**2 / (2 * std**2) ),linewidth=2, color='r')
    print "mean and standard deviation of coincidence timings: ", mean, std
    
    #plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
    #plt.axis([-200, 200, 0, 0.01])
    #plt.grid(True)
    
    #plt.show()
    nCoinc = 0
    for i in xrange(len(xList1)):
        if abs(tList1[i] - tList2[i])< std and xList1[i]>cutoff1 and xList2[i]>cutoff2:
            nCoinc += 1
    
    print "adjusted number of coincidences: ", nCoinc, "\n"
    nDet1.append(n1-n1b)
    nDet2.append(n2-n2b)
    nC.append(nCoinc-ncb)
    
n1 = np.array(nDet1)
n2 = np.array(nDet2)
nc = np.array(nC)
stack = np.column_stack((n1,n2,nc))
np.savetxt('numbers.dat', stack, delimiter='&')

#Reihenfolge: 90_{1-3), 135_{1-3}, 180_{1-3}
#r_theta = nc/(n1*n2)
#k_135 = np.zeros(3)
#k_180 = np.zeros(3)

#for i in range(3):
#    k_135[i] = r_theta[i+3]/r_theta[i]
#    k_180[i] = r_theta[i+6]/r_theta[i]

#a2 = 4*k_135 - k_180 - 3
#a4 = 2 + 2*k_180 - 4*k_135
#an = a2 + a4

#result = np.column_stack((np.array(range(3)), k_135, k_180, a2, a4, an))
#np.savetxt('coefficients.dat', result, fmt='%+1.4f', delimiter='&')

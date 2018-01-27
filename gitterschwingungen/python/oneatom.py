import numpy as np

filestub = 'einatomig_'
eigenfrequencies = np.zeros(12)

for i in range(1, 5):
	temp = np.loadtxt('../messwerte/einatomig_{}.lvm'.format(i), delimiter='	', usecols=(1,2), unpack=True)
	eigenfrequencies += temp[0]
	eigenfrequencies += temp[1]

eigenfrequencies /= 8
eigenfrequencies *= 2*np.pi
#print eigenfrequencies

lamb = 5.43*np.array([2., 1., 2./3., 0.5, 2./5., 1./3., 2./7., 1./4., 2./9., 1./5., 2./11., 1./6.])
k = 2*np.pi/lamb
#print k
Ds = (np.square(eigenfrequencies)*0.504)/(4*np.square(np.sin(k*0.409/2)))
D = np.sum(Ds)/12
print D

stacked = np.column_stack((k, eigenfrequencies))

#np.savetxt('einatomig.dat', stacked, delimiter='	')

import numpy as np

filestub = 'einatomig_'
eigenfrequencies = np.zeros(12)

for i in range(1, 5):
	temp = np.loadtxt('../messwerte/zweiatomig_{}.lvm'.format(i), delimiter='	', usecols=(1,2), unpack=True)
	eigenfrequencies += temp[0]
	eigenfrequencies += temp[1]

eigenfrequencies /= 8
eigenfrequencies *= 2*np.pi

lamb = 5.43*np.array([2., 1., 2./3., 0.5, 2./5., 1./3.])
k = 2*np.pi/lamb

eigenfrequencies = np.split(eigenfrequencies, 2)
acoustic = eigenfrequencies[0]
optic = np.flipud(eigenfrequencies[1])
stacked = np.column_stack((k, acoustic, optic))

np.savetxt('zweiatomig.dat', stacked, delimiter='	')

import numpy as np
from sympy import *
from math import sqrt

n1, n2, nc = np.loadtxt('numbers.dat', delimiter='&', unpack=True)

measurement = np.array([1,2,3]*3)
angle = np.array([90]*3 + [135]*3 + [180]*3)
stack = np.column_stack((measurement, angle, n1,n2,nc))

head = '\\begin{tabular}{ccccc}\n\\toprule\nmeasurement&angle&$N_1$&$N_2$&$N_c$\n\\midrule'
foot = '\\bottomrule\n\\end{tabular}'
np.savetxt('numbers.tex', stack, fmt='%1d', delimiter='&', newline='\\\ \n', header=head, footer=foot, comments='')

#einzelauswertung
r_theta = nc/(n1*n2)
k_135 = np.zeros(3)
k_180 = np.zeros(3)

for i in range(3):
    k_135[i] = r_theta[i+3]/r_theta[i]
    k_180[i] = r_theta[i+6]/r_theta[i]

a2 = 4*k_135 - k_180 -3
a4 = 2 + 2*k_180 -4*k_135
an = a2 + a4

k_135 = np.append(k_135, np.mean(k_135))
k_180 = np.append(k_180, np.mean(k_180))
a2 = np.append(a2, np.mean(a2))
a4 = np.append(a4, np.mean(a4))
an = np.append(an, np.mean(an))

#auswertung summe der ergebnisse
n1_sum = np.sum(np.split(n1, 3), axis=1)
n2_sum = np.sum(np.split(n2, 3), axis=1)
nc_sum = np.sum(np.split(nc, 3), axis=1)

r_sum = nc_sum/(n1_sum*n2_sum)
k_135_sum = r_sum[1]/r_sum[0]
k_180_sum = r_sum[2]/r_sum[0]
a2_sum = 4*k_135_sum - k_180_sum -3
a4_sum = 2 + 2*k_180_sum -4*k_135_sum
an_sum = a2_sum + a4_sum

k_135 = np.append(k_135, k_135_sum)
k_180 = np.append(k_180, k_180_sum)
a2 = np.append(a2, a2_sum)
a4 = np.append(a4, a4_sum)
an = np.append(an, an_sum)

#alles zusammen
result = np.column_stack((np.array(range(1,6)), k_135, k_180, a2, a4, an))

head = '\\begin{tabular}{cccccc}\n\\toprule\nmeasurement&K(135\si{\degree})&K(180\si{\degree})&$a_2$&$a_4$&$A_n$\n\\midrule'
foot = '\\bottomrule\n\\end{tabular}'
np.savetxt('coefficients.tex', result, fmt='%1.4f', delimiter='&', newline='\\\ \n', header=head, footer=foot, comments='')


#Fehlerrechnung
cov =  np.cov((n1_sum, n2_sum, nc_sum))

n_1 = Symbol('n_1')
n_2 = Symbol('n_2')
n_c = Symbol('n_c')
Ns = [n_1, n_2, n_c]
Ns_sum = [n1_sum, n2_sum, nc_sum]
N = [n1, n2, nc]
R = n_c/(n_1*n_2)

k135 = Symbol('k135')
k180 = Symbol('k180')
Ks = [k135, k180]
eq_a2 = 4*k135 - k180 - 3
eq_a4 = 2 + 2*k180 - 4*k135

#gesamt
r_sum_err_sum = np.zeros(3)
for i in range(3):
    for j in range(3):
        r_sum_err_sum[i] += (R.diff(Ns[j]).subs([(n_1, n1_sum[i]),(n_2, n2_sum[i]),(n_c, nc_sum[i])])*np.sqrt(Ns_sum[j][i]))**2
r_sum_err = np.sqrt(r_sum_err_sum)

#cov_sum = 0
#for i in range(2):
#    for j in range(1,3):
#        cov_sum += 2*(R.diff(Ns[i]).subs([(n_1, n1_sum[1]),(n_2, n2_sum[1]),(n_c, nc_sum[1])]))*(R.diff(Ns[j]).subs([(n_1, n1_sum[1]),(n_2, n2_sum[1]),(n_c, nc_sum[1])]))*cov[i][j]

k_sum_err = np.zeros(2)
k_sum_err[0] = k_135_sum*sqrt((r_sum_err[1]/r_sum[1])**2 + (r_sum_err[0]/r_sum[0])**2)
k_sum_err[1] = k_180_sum*sqrt((r_sum_err[2]/r_sum[2])**2 + (r_sum_err[0]/r_sum[0])**2)

a2_sum_err_sum = 0
for i in range(2):
    a2_sum_err_sum += (eq_a2.diff(Ks[i]).subs([(k135, k_135_sum),(k180, k_180_sum)])*k_sum_err[i])**2
a2_sum_err = sqrt(a2_sum_err_sum)

a4_sum_err_sum = 0
for i in range(2):
    a4_sum_err_sum += (eq_a4.diff(Ks[i]).subs([(k135, k_135_sum),(k180, k_180_sum)])*k_sum_err[i])**2
a4_sum_err = sqrt(a4_sum_err_sum)

#einzeln
r_err_sum = np.zeros(9)
for i in range(9):
    for j in range(3):
        r_err_sum[i] += (R.diff(Ns[j]).subs([(n_1, n1[i]),(n_2, n2[i]),(n_c, nc[i])])*np.sqrt(N[j][i]))**2
r_err = np.sqrt(r_err_sum)

k_135_err = np.zeros(3)
k_180_err = np.zeros(3)
for i in range(3):
    k_135_err[i] = k_135[i]*sqrt((r_err[i+3]/r_theta[i+3])**2 + (r_err[i]/r_theta[i])**2)
    k_180_err[i] = k_180[i]*sqrt((r_err[i+6]/r_theta[i+6])**2 + (r_err[i]/r_theta[i])**2)
k_err = [k_135_err, k_180_err]

a2_err_sum = np.zeros(3)
for i in range(3):
    for j in range(2):
        a2_err_sum[i] += (eq_a2.diff(Ks[j]).subs([(k135, k_135[i]),(k180, k_180[i])])*k_err[j][i])**2
a2_err = np.sqrt(a2_err_sum)

a4_err_sum = np.zeros(3)
for i in range(3):
    for j in range(2):
        a4_err_sum[i] += (eq_a4.diff(Ks[j]).subs([(k135, k_135[i]),(k180, k_180[i])])*k_err[j][i])**2
a4_err = np.sqrt(a4_err_sum)

#mittelwert
k_135_err_mean = np.std(k_135[:3])/sqrt(3)
k_180_err_mean = np.std(k_180[:3])/sqrt(3)
a2_err_mean = np.std(a2[:3])/sqrt(3)
a4_err_mean = np.std(a4[:3])/sqrt(3)

k_135_err = np.append(k_135_err, [k_135_err_mean, k_sum_err[0]])
k_180_err = np.append(k_180_err, [k_180_err_mean, k_sum_err[1]])
a2_err = np.append(a2_err, [a2_err_mean, a2_sum_err])
a4_err = np.append(a4_err, [a4_err_mean, a4_sum_err])

errors = np.column_stack((range(1,6), k_135_err, k_180_err, a2_err, a4_err, k_180_err))

head = '\\begin{tabular}{cccccc}\n\\toprule\nmeasurement&$\Delta K(135\si{\degree})$&$\Delta K(180\si{\degree})$&$\Delta a_2$&$\Delta a_4$&$\Delta A_n$\n\\midrule'
foot = '\\bottomrule\n\\end{tabular}'
np.savetxt('errors.tex', errors, fmt='%1.4f', delimiter='&', newline='\\\ \n', header=head, footer=foot, comments='')

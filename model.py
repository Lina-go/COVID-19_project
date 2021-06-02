##
import tkinter as tk
import sys
# import config
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
import scipy.integrate as inte

'''=====================================================================================================================
                                        CONDICIONES INICIALES
====================================================================================================================='''
'''

s-> Fracción de la población que es susceptible (individuos en peligro de infectarse/total)
e-> Fracción de la población que es expuesta (individuos expuestos sin síntomas /total)
i-> Fracción población infectada (individuos infectados con síntomas/total)
r-> Fracción población recuperada (individuos recuperados/total)
p-> (Número de individuos que muere por la enfermedad /total)

a_e-> Factor de contagio entre las poblaciones susceptibles y las expuestas
(mayor que a_i)
a_i-> Factor de contagio entre las poblaciones infectadas y susceptibles 
y-> Tasa de reinfección
k-> Tasa en la que aparecen los síntomas en los casos expuestos
phi-> Tasa de recuperación de los casos expuestos 
B-> Tasa de recuperación de los casos infectados 

'''
# ==============================
# DEFINIR PARÁMETROS
# ==============================
a_e = 0.65
a_i = 0.005
k = 0.05
gamma = 0.0
B = 0.1
phi = 0.08
u = 0.02

# se define h
h = 0.01

# se definen los valores iniciales
# suma de valores iniciales debe dar 1
ys0 = 0.9
ye0 = 0.025
yi0 = 0.025
yr0 = 0.025
yp0 = 0.025

# se define el tiempo inicial y el tiempo final
t0 = 0.0
tf = 150.0

# ==============================
# DEFINIR FUNCIONES
# ==============================


# Definimos la función ds
def ds(s, e, i, r, a_e, a_i, gamma):
    return ((-a_e)*s*e) - (a_i*s*i) + gamma*r


# Definimos la función de
def de(s, e, i, a_e, a_i, k, phi):
    return (a_e*s*e) + (a_i*s*i) - k*e - phi*e


# Definimos la función di
def di(e, i, k, B, u):
    return k*e - B*i - u*i


# Definimos la función dr
def dr(e, i, r, B, phi, gamma):
    return B*i + phi*e - gamma*r


# Definimos la función dp
def dp(i, u):
    return u*i

##

# ==============================
# FUNCIONES AUXILIARES
# ==============================
# vector yt5 = [s(t),e(t),i(t),r(t),p(t)]
"""
y1t1= Arreglo de soluciones en la solución anterior  -> ds
y2t1= Arreglo de soluciones en la solución anterior  -> de
y3t1= Arreglo de soluciones en la solución anterior  -> di
y4t1= Arreglo de soluciones en la solución anterior  -> dr
y5t1= Arreglo de soluciones en la solución anterior  -> dp
"""


# vector = [s(t),e(t),i(t),r(t),p(t)]
def FEulerBackRoot(var, y1t1, y2t1,y3t1, y4t1,y5t1, h, a_e, a_i, gamma, k, u, B, phi):
    return [y1t1 + h * ds(var[0], var[1], var[2], var[3], a_e, a_i, gamma) - var[0],     # ds
            y2t1 + h * de(var[0], var[1], var[2], a_e, a_i, k, phi) - var[1],            # de
            y3t1 + h * di(var[1], var[2], k, B, u) - var[2],                             # di
            y4t1 + h * dr(var[1], var[2], var[3], B, phi, gamma) - var[3],               # dr
            y5t1 + h * dp(var[2], u) - var[4]]                                           # dp


def FEulerModRoot(yt5, y1t1, y2t1, y3t1, y4t1, y5t1, h, a_e, a_i, gamma, k, u, B, phi):
    return [y1t1 + (h / 2.0) * (ds(y1t1, y2t1, y3t1, y4t1, a_e, a_i, gamma) + ds(yt5[0], yt5[1], yt5[2], yt5[3], a_e, a_i, gamma)) - yt5[0],   # ds
            y2t1 + (h / 2.0) * (de(y1t1, y2t1, y3t1, a_e, a_i, k, phi) + de(yt5[0], yt5[1], yt5[2], a_e, a_i, k, phi)) - yt5[1],               # de
            y3t1 + (h / 2.0) * (di(y2t1, y3t1, k, B, u) + di(yt5[1], yt5[2], k, B, u)) - yt5[2],                                               # di
            y4t1 + (h / 2.0) * (dr(y2t1, y3t1, y3t1, B, phi, gamma) + dr(yt5[1], yt5[2], yt5[3], B, phi, gamma)) - yt5[3],                     # dr
            y5t1 + (h / 2.0) * (dp(y3t1, u) + dp(yt5[2], u)) - yt5[4]]                                                                         #dp




# vector de tiempo
t = np.arange(t0, tf + h, h)

# arreglos para Euler forward
ys_EulerFor = np.zeros(len(t))
ys_EulerFor[0] = ys0
ye_EulerFor = np.zeros(len(t))
ye_EulerFor[0] = ye0
yi_EulerFor = np.zeros(len(t))
yi_EulerFor[0] = yi0
yr_EulerFor = np.zeros(len(t))
yr_EulerFor[0] = yr0
yp_EulerFor = np.zeros(len(t))
yp_EulerFor[0] = yp0


# arreglos para Euler hacía atrás
ys_EulerBack = np.zeros(len(t))
ys_EulerBack[0] = ys0
ye_EulerBack = np.zeros(len(t))
ye_EulerBack[0] = ye0
yi_EulerBack = np.zeros(len(t))
yi_EulerBack[0] = yi0
yr_EulerBack = np.zeros(len(t))
yr_EulerBack[0] = yr0
yp_EulerBack = np.zeros(len(t))
yp_EulerBack[0] = yp0


# arreglos para Euler Modificado
ys_EulerMod = np.zeros(len(t))
ys_EulerMod[0] = ys0
ye_EulerMod = np.zeros(len(t))
ye_EulerMod[0] = ye0
yi_EulerMod = np.zeros(len(t))
yi_EulerMod[0] = yi0
yr_EulerMod = np.zeros(len(t))
yr_EulerMod[0] = yr0
yp_EulerMod = np.zeros(len(t))
yp_EulerMod[0] = yp0


# arreglos para RK2
ys_RK2 = np.zeros(len(t))
ys_RK2[0] = ys0
ye_RK2 = np.zeros(len(t))
ye_RK2[0] = ye0
yi_RK2 = np.zeros(len(t))
yi_RK2[0] = yi0
yr_RK2 = np.zeros(len(t))
yr_RK2[0] = yr0
yp_RK2 = np.zeros(len(t))
yp_RK2[0] = yp0


# arreglos para RK4
ys_RK4 = np.zeros(len(t))
ys_RK4[0] = ys0
ye_RK4 = np.zeros(len(t))
ye_RK4[0] = ye0
yi_RK4 = np.zeros(len(t))
yi_RK4[0] = yi0
yr_RK4 = np.zeros(len(t))
yr_RK4[0] = yr0
yp_RK4 = np.zeros(len(t))
yp_RK4[0] = yp0

for iter in range(1, len(t)):

    # Euler hacia adelante
    ys_EulerFor[iter] = ys_EulerFor[iter - 1] + h * ds(ys_EulerFor[iter-1], ye_EulerFor[iter-1], yi_EulerFor[iter-1], yr_EulerFor[iter-1], a_e, a_i, gamma)
    ye_EulerFor[iter] = ye_EulerFor[iter - 1] + h * de(ys_EulerFor[iter-1], ye_EulerFor[iter-1], yi_EulerFor[iter-1], a_e, a_i, k, phi)
    yi_EulerFor[iter] = yi_EulerFor[iter - 1] + h * di(ye_EulerFor[iter-1], yi_EulerFor[iter-1], k, B, u)
    yr_EulerFor[iter] = yr_EulerFor[iter - 1] + h * dr(ye_EulerFor[iter-1], yi_EulerFor[iter-1], yr_EulerFor[iter-1], B, phi, gamma)
    yp_EulerFor[iter] = yp_EulerFor[iter - 1] + h * dp(yi_EulerFor[iter-1], u)

    # Euler hacia atrás
    SolBack = opt.fsolve(FEulerBackRoot,
                         np.array([ys_EulerBack[iter - 1],
                                   ye_EulerBack[iter - 1],
                                   yi_EulerBack[iter - 1],
                                   yr_EulerBack[iter - 1],
                                   yp_EulerBack[iter - 1]]),
                         (ys_EulerBack[iter - 1],
                          ye_EulerBack[iter - 1],
                          yi_EulerBack[iter - 1],
                          yr_EulerBack[iter - 1],
                          yp_EulerBack[iter - 1], h, a_e, a_i, gamma, k, u, B, phi), xtol=10 ** -15)
    ys_EulerBack[iter] = SolBack[0]
    ye_EulerBack[iter] = SolBack[1]
    yi_EulerBack[iter] = SolBack[2]
    yr_EulerBack[iter] = SolBack[3]
    yp_EulerBack[iter] = SolBack[4]

    # Método Euler modificado
    SolMod = opt.fsolve(FEulerModRoot,
                        np.array([ys_EulerMod[iter - 1],
                                  ye_EulerMod[iter - 1],
                                  yi_EulerMod[iter - 1],
                                  yr_EulerMod[iter - 1],
                                  yp_EulerMod[iter - 1]]),
                        (ys_EulerMod[iter - 1],
                         ye_EulerMod[iter - 1],
                         yi_EulerMod[iter - 1],
                         yr_EulerMod[iter - 1],
                         yp_EulerMod[iter - 1], h, a_e, a_i, gamma, k, u, B, phi), xtol=10 ** -15)
    ys_EulerMod[iter] = SolMod[0]
    ye_EulerMod[iter] = SolMod[1]
    yi_EulerMod[iter] = SolMod[2]
    yr_EulerMod[iter] = SolMod[3]
    yp_EulerMod[iter] = SolMod[4]

    # Runge-Kutta de segundo orden
    k11 = ds(ys_RK2[iter-1], ye_RK2[iter-1], yi_RK2[iter-1], yr_RK2[iter-1], a_e, a_i, gamma)
    k21 = de(ys_RK2[iter-1], ye_RK2[iter-1], yr_RK2[iter-1], a_e, a_i, k, phi)
    k31 = di(ye_RK2[iter-1], yi_RK2[iter-1], k, B, u)
    k41 = dr(ye_RK2[iter-1], yi_RK2[iter-1], yr_RK2[iter-1], B, phi, gamma)
    k51 = dp(yi_RK2[iter-1], u)

    k12 = ds(ys_RK2[iter-1] + k11 * h, ye_RK2[iter-1] + k21 * h, yi_RK2[iter-1] + k31 * h, yr_RK2[iter-1] + k41 * h, a_e, a_i, gamma)
    k22 = de(ys_RK2[iter-1] + k11 * h, ye_RK2[iter-1] + k21 * h, yr_RK2[iter-1] + k41 * h, a_e, a_i, k, phi)
    k32 = di(ye_RK2[iter-1] + k21 * h, yi_RK2[iter-1] + k31 * h, k, B, u)
    k42 = dr(ye_RK2[iter-1] + k21 * h, yi_RK2[iter-1] + k31 * h, yr_RK2[iter-1] + k41 * h, B, phi, gamma)
    k52 = dp(yi_RK2[iter-1] + k41 * h, u)

    ys_RK2[iter] = ys_RK2[iter-1] + (h/2.0) * (k11+k12)
    ye_RK2[iter] = ye_RK2[iter-1] + (h/2.0) * (k21+k22)
    yi_RK2[iter] = yi_RK2[iter-1] + (h/2.0) * (k31+k32)
    yr_RK2[iter] = yr_RK2[iter-1] + (h/2.0) * (k41+k42)
    yp_RK2[iter] = yp_RK2[iter-1] + (h/2.0) * (k51+k52)

    # Runge-kutta de cuarto orden
    k11 = ds(ys_RK4[iter-1], ye_RK4[iter-1], yi_RK4[iter-1], yr_RK4[iter-1], a_e, a_i, gamma)
    k21 = de(ys_RK4[iter-1], ye_RK4[iter-1], yr_RK4[iter-1], a_e, a_i, k, phi)
    k31 = di(ye_RK4[iter-1], yi_RK4[iter-1], k, B, u)
    k41 = dr(ye_RK4[iter-1], yi_RK4[iter-1], yr_RK4[iter-1], B, phi, gamma)
    k51 = dp(yi_RK4[iter-1], u)

    k12 = ds(ys_RK4[iter-1] + 0.5 * k11 * h,
             ye_RK2[iter-1] + 0.5 * k21 * h,
             yi_RK2[iter-1] + 0.5 * k31 * h,
             yr_RK2[iter-1] + 0.5 * k41 * h, a_e, a_i, gamma)
    k22 = de(ys_RK4[iter-1] + 0.5 * k11 * h,
             ye_RK2[iter-1] + 0.5 * k21 * h,
             yr_RK2[iter-1] + 0.5 * k41 * h, a_e, a_i, k, phi)
    k32 = di(ye_RK4[iter-1] + 0.5 * k21 * h,
             yi_RK2[iter-1] + 0.5 * k31 * h, k, B, u)
    k42 = dr(ye_RK4[iter-1] + 0.5 * k21 * h,
             yi_RK2[iter-1] + 0.5 * k31 * h,
             yr_RK2[iter-1] + 0.5 * k41 * h, B, phi, gamma)
    k52 = dp(yi_RK4[iter-1] + 0.5 * k41 * h, u)

    k13 = ds(ys_RK4[iter-1] + 0.5 * k12 * h,
             ye_RK2[iter-1] + 0.5 * k22 * h,
             yi_RK2[iter-1] + 0.5 * k32 * h,
             yr_RK2[iter-1] + 0.5 * k42 * h, a_e, a_i, gamma)
    k23 = de(ys_RK4[iter-1] + 0.5 * k12 * h,
             ye_RK2[iter-1] + 0.5 * k22 * h,
             yr_RK2[iter-1] + 0.5 * k42 * h, a_e, a_i, k, phi)
    k33 = di(ye_RK4[iter-1] + 0.5 * k22 * h,
             yi_RK2[iter-1] + 0.5 * k32 * h, k, B, u)
    k43 = dr(ye_RK4[iter-1] + 0.5 * k22 * h,
             yi_RK2[iter-1] + 0.5 * k32 * h,
             yr_RK2[iter-1] + 0.5 * k42 * h, B, phi, gamma)
    k53 = dp(yi_RK4[iter-1] + 0.5 * k42 * h, u)

    k14 = ds(ys_RK4[iter-1] + 0.5 * k13 * h,
             ye_RK2[iter-1] + 0.5 * k23 * h,
             yi_RK2[iter-1] + 0.5 * k33 * h,
             yr_RK2[iter-1] + 0.5 * k43 * h, a_e, a_i, gamma)
    k24 = de(ys_RK4[iter-1] + 0.5 * k13 * h,
             ye_RK2[iter-1] + 0.5 * k23 * h,
             yr_RK2[iter-1] + 0.5 * k43 * h, a_e, a_i, k, phi)
    k34 = di(ye_RK4[iter-1] + 0.5 * k23 * h,
             yi_RK2[iter-1] + 0.5 * k33 * h, k, B, u)
    k44 = dr(ye_RK4[iter-1] + 0.5 * k23 * h,
             yi_RK2[iter-1] + 0.5 * k33 * h,
             yr_RK2[iter-1] + 0.5 * k43 * h, B, phi, gamma)
    k54 = dp(yi_RK4[iter-1] + 0.5 * k43 * h, u)

    ys_RK4[iter] = ys_RK4[iter-1] + (h/6.0) * (k11 + 2*k12 + 2*k13 + k14)
    ye_RK4[iter] = ye_RK4[iter-1] + (h/6.0) * (k21 + 2*k22 + 2*k23 + k24)
    yi_RK4[iter] = yi_RK4[iter-1] + (h/6.0) * (k31 + 2*k32 + 2*k33 + k34)
    yr_RK4[iter] = yr_RK4[iter-1] + (h/6.0) * (k41 + 2*k42 + 2*k43 + k44)
    yp_RK4[iter] = yp_RK4[iter-1] + (h/6.0) * (k51 + 2*k52 + 2*k53 + k54)


# vector = [s(t),e(t),i(t),r(t),p(t)]
def FSystem(t, y, a_e, a_i, gamma, k,  u, B, phi):
    return [ds(y[0], y[1], y[2], y[3], a_e, a_i, gamma),
            de(y[0], y[1], y[2], a_e, a_i, k, phi),
            di(y[1], y[2], k, B, u),
            dr(y[1], y[2], y[3], B, phi, gamma),
            dp(y[2], u)]


SolRK45 = inte.solve_ivp(FSystem, [t0, tf], [ys0, ye0, yi0, yr0, yp0], args=(a_e, a_i, gamma, k, u, B, phi), t_eval=t, method='RK45')
"""
# Graficamos la estimación de ds obtenida para s
plt.figure()
plt.plot(t, ys_EulerFor, "r")
plt.plot(t, ys_EulerBack, "g")
plt.plot(t, ys_EulerMod, "m")
plt.plot(t, ys_RK2, "orange")
plt.plot(t, ys_RK4, "maroon")
plt.plot(t, SolRK45.y[0], "--", color="olive")
plt.xlabel("t", fontsize=15)
plt.title("Estimaciones de ys(t)=Y(t)")
plt.legend(["EulerFor", "EulerBack", "EulerMod", "SolRK2", "SolRK4", "SolRK45"], fontsize=12)
plt.grid(1)

# vector = [s(t),e(t),i(t),r(t),p(t)]
# Graficamos la estimación de ds obtenida para e
plt.figure()
plt.plot(t, ye_EulerFor, "r")
plt.plot(t, ye_EulerBack, "g")
plt.plot(t, ye_EulerMod, "m")
plt.plot(t, ye_RK2, "orange")
plt.plot(t, ye_RK4, "maroon")
plt.plot(t, SolRK45.y[1], "--", color="olive")
plt.xlabel("t", fontsize=15)
plt.title("Estimaciones de ye(t)=Y(t)")
plt.legend(["EulerFor", "EulerBack", "EulerMod", "SolRK2", "SolRK4", "SolRK45"], fontsize=12)
plt.grid(1)

# vector = [s(t),e(t),i(t),r(t),p(t)]
# Graficamos la estimación de ds obtenida para i
plt.figure()
plt.plot(t, yi_EulerFor, "r")
plt.plot(t, yi_EulerBack, "g")
plt.plot(t, yi_EulerMod, "m")
plt.plot(t, yi_RK2, "orange")
plt.plot(t, yi_RK4, "maroon")
plt.plot(t, SolRK45.y[2], "--", color="olive")
plt.xlabel("t", fontsize=15)
plt.title("Estimaciones de yi(t)=Y(t)")
plt.legend(["EulerFor", "EulerBack", "EulerMod", "SolRK2", "SolRK4", "SolRK45"], fontsize=12)
plt.grid(1)

# vector = [s(t),e(t),i(t),r(t),p(t)]
# Graficamos la estimación de ds obtenida para r
plt.figure()
plt.plot(t, yr_EulerFor, "r")
plt.plot(t, yr_EulerBack, "g")
plt.plot(t, yr_EulerMod, "m")
plt.plot(t, yr_RK2, "orange")
plt.plot(t, yr_RK4, "maroon")
plt.plot(t, SolRK45.y[3], "--", color="olive")
plt.xlabel("t", fontsize=15)
plt.title("Estimaciones de yr(t)=Y(t)")
plt.legend(["EulerFor", "EulerBack", "EulerMod", "SolRK2", "SolRK4", "SolRK45"], fontsize=12)
plt.grid(1)

# vector = [s(t),e(t),i(t),r(t),p(t)]
# Graficamos la estimación de ds obtenida para p
plt.figure()
plt.plot(t, yp_EulerFor, "r")
plt.plot(t, yp_EulerBack, "g")
plt.plot(t, yp_EulerMod, "m")
plt.plot(t, yp_RK2, "orange")
plt.plot(t, yp_RK4, "maroon")
plt.plot(t, SolRK45.y[4], "--", color="olive")
plt.xlabel("t", fontsize=15)
plt.title("Estimaciones de yp(t)=Y(t)")
plt.legend(["EulerFor", "EulerBack", "EulerMod", "SolRK2", "SolRK4", "SolRK45"], fontsize=12)
plt.grid(1)

#Graficar todas"""
# vector = [s(t),e(t),i(t),r(t),p(t)]
""""
plt.figure()
plt.plot(t, SolRK45.y[0], '-', color="purple", label="s(t)")
plt.plot(t, SolRK45.y[1], '-', color="crimson", label="e(t)")
plt.plot(t, SolRK45.y[2], '-', color="yellow", label="i(t)")
plt.plot(t, SolRK45.y[3], '-', color="olive", label="r(t)")
plt.plot(t, SolRK45.y[4], '-', color="greenyellow", label="p(t)")
plt.xlabel("t", fontsize=15)
plt.title("Estimaciones Totales")
plt.legend()
plt.grid(1)

"""

##
'''Función para Euler Forward'''


def eulerforward(t0, tf, a_e, a_i, k, gamma, B, phi, u,h = 0.01):

    # vector de tiempo
    t = np.arange(t0, tf + h, h)

    # arreglos para Euler forward
    ys_EulerFor = np.zeros(len(t))
    ys_EulerFor[0] = ys0
    ye_EulerFor = np.zeros(len(t))
    ye_EulerFor[0] = ye0
    yi_EulerFor = np.zeros(len(t))
    yi_EulerFor[0] = yi0
    yr_EulerFor = np.zeros(len(t))
    yr_EulerFor[0] = yr0
    yp_EulerFor = np.zeros(len(t))
    yp_EulerFor[0] = yp0

    for iter in range(1, len(t)):
        # Euler hacia adelante
        ys_EulerFor[iter] = ys_EulerFor[iter - 1] + h * ds(ys_EulerFor[iter - 1], ye_EulerFor[iter - 1],
                                                           yi_EulerFor[iter - 1], yr_EulerFor[iter - 1], a_e, a_i,
                                                           gamma)
        ye_EulerFor[iter] = ye_EulerFor[iter - 1] + h * de(ys_EulerFor[iter - 1], ye_EulerFor[iter - 1],
                                                           yi_EulerFor[iter - 1], a_e, a_i, k, phi)
        yi_EulerFor[iter] = yi_EulerFor[iter - 1] + h * di(ye_EulerFor[iter - 1], yi_EulerFor[iter - 1], k, B, u)
        yr_EulerFor[iter] = yr_EulerFor[iter - 1] + h * dr(ye_EulerFor[iter - 1], yi_EulerFor[iter - 1],
                                                           yr_EulerFor[iter - 1], B, phi, gamma)
        yp_EulerFor[iter] = yp_EulerFor[iter - 1] + h * dp(yi_EulerFor[iter - 1], u)

    return t, ys_EulerFor, ye_EulerFor, yi_EulerFor, yr_EulerFor, yp_EulerFor


'''
# vector = [s(t),e(t),i(t),r(t),p(t)]
plt.figure()
plt.plot(t, ys_EulerFor, '-', color="blue", label="s(t)")
plt.plot(t, ye_EulerFor, '-', color="cyan", label="e(t)")
plt.plot(t, yi_EulerFor, '-', color="red", label="i(t)")
plt.plot(t, yr_EulerFor, '-', color="lime", label="r(t)")
plt.plot(t, yp_EulerFor, '-', color="k", label="p(t)")
plt.xlabel("t", fontsize=15)
plt.ylabel("Population Ratio", fontsize=15)
plt.title("Euler Forward")
plt.legend()
plt.grid(1)
'''

##
'''Función para Euler Backward'''


def eulerbackward(t0, tf, a_e, a_i, k, gamma, B, phi, u,h = 0.01):

    # vector de tiempo
    t = np.arange(t0, tf + h, h)

    # arreglos para Euler hacía atrás
    ys_EulerBack = np.zeros(len(t))
    ys_EulerBack[0] = ys0
    ye_EulerBack = np.zeros(len(t))
    ye_EulerBack[0] = ye0
    yi_EulerBack = np.zeros(len(t))
    yi_EulerBack[0] = yi0
    yr_EulerBack = np.zeros(len(t))
    yr_EulerBack[0] = yr0
    yp_EulerBack = np.zeros(len(t))
    yp_EulerBack[0] = yp0

    for iter in range(1, len(t)):
        # Euler hacia atrás
        SolBack = opt.fsolve(FEulerBackRoot,
                             np.array([ys_EulerBack[iter - 1],
                                       ye_EulerBack[iter - 1],
                                       yi_EulerBack[iter - 1],
                                       yr_EulerBack[iter - 1],
                                       yp_EulerBack[iter - 1]]),
                             (ys_EulerBack[iter - 1],
                              ye_EulerBack[iter - 1],
                              yi_EulerBack[iter - 1],
                              yr_EulerBack[iter - 1],
                              yp_EulerBack[iter - 1], h, a_e, a_i, gamma, k, u, B, phi), xtol=10 ** -15)
        ys_EulerBack[iter] = SolBack[0]
        ye_EulerBack[iter] = SolBack[1]
        yi_EulerBack[iter] = SolBack[2]
        yr_EulerBack[iter] = SolBack[3]
        yp_EulerBack[iter] = SolBack[4]

    return t, ys_EulerBack, ye_EulerBack, yi_EulerBack, yr_EulerBack, yp_EulerBack


'''
# vector = [s(t),e(t),i(t),r(t),p(t)]
plt.figure()
plt.plot(t, ys_EulerBack, '-', color="blue", label="s(t)")
plt.plot(t, ye_EulerBack, '-', color="cyan", label="e(t)")
plt.plot(t, yi_EulerBack, '-', color="red", label="i(t)")
plt.plot(t, yr_EulerBack, '-', color="lime", label="r(t)")
plt.plot(t, yp_EulerBack, '-', color="k", label="p(t)")
plt.xlabel("t", fontsize=15)
plt.ylabel("Population Ratio", fontsize=15)
plt.title("Euler Backward")
plt.legend()
plt.grid(1)
'''
##
'''Función para Euler Modificado'''


def eulermodificado(t0, tf, a_e, a_i, k, gamma, B, phi, u,h = 0.01):

    # vector de tiempo
    t = np.arange(t0, tf + h, h)

    # arreglos para Euler Modificado
    ys_EulerMod = np.zeros(len(t))
    ys_EulerMod[0] = ys0
    ye_EulerMod = np.zeros(len(t))
    ye_EulerMod[0] = ye0
    yi_EulerMod = np.zeros(len(t))
    yi_EulerMod[0] = yi0
    yr_EulerMod = np.zeros(len(t))
    yr_EulerMod[0] = yr0
    yp_EulerMod = np.zeros(len(t))
    yp_EulerMod[0] = yp0

    for iter in range(1, len(t)):
        # Método Euler modificado
        SolMod = opt.fsolve(FEulerModRoot,
                            np.array([ys_EulerMod[iter - 1],
                                      ye_EulerMod[iter - 1],
                                      yi_EulerMod[iter - 1],
                                      yr_EulerMod[iter - 1],
                                      yp_EulerMod[iter - 1]]),
                            (ys_EulerMod[iter - 1],
                             ye_EulerMod[iter - 1],
                             yi_EulerMod[iter - 1],
                             yr_EulerMod[iter - 1],
                             yp_EulerMod[iter - 1], h, a_e, a_i, gamma, k, u, B, phi), xtol=10 ** -15)
        ys_EulerMod[iter] = SolMod[0]
        ye_EulerMod[iter] = SolMod[1]
        yi_EulerMod[iter] = SolMod[2]
        yr_EulerMod[iter] = SolMod[3]
        yp_EulerMod[iter] = SolMod[4]

    return t, ys_EulerMod, ye_EulerMod, yi_EulerMod, yr_EulerMod, yp_EulerMod


'''
# vector = [s(t),e(t),i(t),r(t),p(t)]
plt.figure()
plt.plot(t, ys_EulerMod, '-', color="blue", label="s(t)")
plt.plot(t, ye_EulerMod, '-', color="cyan", label="e(t)")
plt.plot(t, yi_EulerMod, '-', color="red", label="i(t)")
plt.plot(t, yr_EulerMod, '-', color="lime", label="r(t)")
plt.plot(t, yp_EulerMod, '-', color="k", label="p(t)")
plt.xlabel("t", fontsize=15)
plt.ylabel("Population Ratio", fontsize=15)
plt.title("Euler Modificado")
plt.legend()
plt.grid(1)
'''

##
'''Función para RK2'''


def rk2(t0, tf, a_e, a_i, k, gamma, B, phi, u,h = 0.01):

    # vector de tiempo
    t = np.arange(t0, tf + h, h)

    # arreglos para RK2
    ys_RK2 = np.zeros(len(t))
    ys_RK2[0] = ys0
    ye_RK2 = np.zeros(len(t))
    ye_RK2[0] = ye0
    yi_RK2 = np.zeros(len(t))
    yi_RK2[0] = yi0
    yr_RK2 = np.zeros(len(t))
    yr_RK2[0] = yr0
    yp_RK2 = np.zeros(len(t))
    yp_RK2[0] = yp0

    for iter in range(1, len(t)):
        # Runge-Kutta de segundo orden
        k11 = ds(ys_RK2[iter - 1], ye_RK2[iter - 1], yi_RK2[iter - 1], yr_RK2[iter - 1], a_e, a_i, gamma)
        k21 = de(ys_RK2[iter - 1], ye_RK2[iter - 1], yr_RK2[iter - 1], a_e, a_i, k, phi)
        k31 = di(ye_RK2[iter - 1], yi_RK2[iter - 1], k, B, u)
        k41 = dr(ye_RK2[iter - 1], yi_RK2[iter - 1], yr_RK2[iter - 1], B, phi, gamma)
        k51 = dp(yi_RK2[iter - 1], u)

        k12 = ds(ys_RK2[iter - 1] + k11 * h, ye_RK2[iter - 1] + k21 * h, yi_RK2[iter - 1] + k31 * h,
                 yr_RK2[iter - 1] + k41 * h, a_e, a_i, gamma)
        k22 = de(ys_RK2[iter - 1] + k11 * h, ye_RK2[iter - 1] + k21 * h, yr_RK2[iter - 1] + k41 * h, a_e, a_i, k, phi)
        k32 = di(ye_RK2[iter - 1] + k21 * h, yi_RK2[iter - 1] + k31 * h, k, B, u)
        k42 = dr(ye_RK2[iter - 1] + k21 * h, yi_RK2[iter - 1] + k31 * h, yr_RK2[iter - 1] + k41 * h, B, phi, gamma)
        k52 = dp(yi_RK2[iter - 1] + k41 * h, u)

        ys_RK2[iter] = ys_RK2[iter - 1] + (h / 2.0) * (k11 + k12)
        ye_RK2[iter] = ye_RK2[iter - 1] + (h / 2.0) * (k21 + k22)
        yi_RK2[iter] = yi_RK2[iter - 1] + (h / 2.0) * (k31 + k32)
        yr_RK2[iter] = yr_RK2[iter - 1] + (h / 2.0) * (k41 + k42)
        yp_RK2[iter] = yp_RK2[iter - 1] + (h / 2.0) * (k51 + k52)

    return t, ys_EulerMod, ye_EulerMod, yi_EulerMod, yr_EulerMod, yp_EulerMod



'''
# vector = [s(t),e(t),i(t),r(t),p(t)]
plt.figure()
plt.plot(t, ys_RK2, '-', color="blue", label="s(t)")
plt.plot(t, ye_RK2, '-', color="cyan", label="e(t)")
plt.plot(t, yi_RK2, '-', color="red", label="i(t)")
plt.plot(t, yr_RK2, '-', color="lime", label="r(t)")
plt.plot(t, yp_RK2, '-', color="k", label="p(t)")
plt.xlabel("t", fontsize=15)
plt.ylabel("Population Ratio", fontsize=15)
plt.title("Runge-Kutta 2")
plt.legend()
plt.grid(1)
'''

##
'''Función para RK4'''


def rk4(t0, tf, a_e, a_i, k, gamma, B, phi, u,h = 0.01):

    # vector de tiempo
    t = np.arange(t0, tf + h, h)

    # arreglos para RK4
    ys_RK4 = np.zeros(len(t))
    ys_RK4[0] = ys0
    ye_RK4 = np.zeros(len(t))
    ye_RK4[0] = ye0
    yi_RK4 = np.zeros(len(t))
    yi_RK4[0] = yi0
    yr_RK4 = np.zeros(len(t))
    yr_RK4[0] = yr0
    yp_RK4 = np.zeros(len(t))
    yp_RK4[0] = yp0

    for iter in range(1, len(t)):
        # Runge-kutta de cuarto orden
        k11 = ds(ys_RK4[iter - 1], ye_RK4[iter - 1], yi_RK4[iter - 1], yr_RK4[iter - 1], a_e, a_i, gamma)
        k21 = de(ys_RK4[iter - 1], ye_RK4[iter - 1], yr_RK4[iter - 1], a_e, a_i, k, phi)
        k31 = di(ye_RK4[iter - 1], yi_RK4[iter - 1], k, B, u)
        k41 = dr(ye_RK4[iter - 1], yi_RK4[iter - 1], yr_RK4[iter - 1], B, phi, gamma)
        k51 = dp(yi_RK4[iter - 1], u)

        k12 = ds(ys_RK4[iter - 1] + 0.5 * k11 * h,
                 ye_RK2[iter - 1] + 0.5 * k21 * h,
                 yi_RK2[iter - 1] + 0.5 * k31 * h,
                 yr_RK2[iter - 1] + 0.5 * k41 * h, a_e, a_i, gamma)
        k22 = de(ys_RK4[iter - 1] + 0.5 * k11 * h,
                 ye_RK2[iter - 1] + 0.5 * k21 * h,
                 yr_RK2[iter - 1] + 0.5 * k41 * h, a_e, a_i, k, phi)
        k32 = di(ye_RK4[iter - 1] + 0.5 * k21 * h,
                 yi_RK2[iter - 1] + 0.5 * k31 * h, k, B, u)
        k42 = dr(ye_RK4[iter - 1] + 0.5 * k21 * h,
                 yi_RK2[iter - 1] + 0.5 * k31 * h,
                 yr_RK2[iter - 1] + 0.5 * k41 * h, B, phi, gamma)
        k52 = dp(yi_RK4[iter - 1] + 0.5 * k41 * h, u)

        k13 = ds(ys_RK4[iter - 1] + 0.5 * k12 * h,
                 ye_RK2[iter - 1] + 0.5 * k22 * h,
                 yi_RK2[iter - 1] + 0.5 * k32 * h,
                 yr_RK2[iter - 1] + 0.5 * k42 * h, a_e, a_i, gamma)
        k23 = de(ys_RK4[iter - 1] + 0.5 * k12 * h,
                 ye_RK2[iter - 1] + 0.5 * k22 * h,
                 yr_RK2[iter - 1] + 0.5 * k42 * h, a_e, a_i, k, phi)
        k33 = di(ye_RK4[iter - 1] + 0.5 * k22 * h,
                 yi_RK2[iter - 1] + 0.5 * k32 * h, k, B, u)
        k43 = dr(ye_RK4[iter - 1] + 0.5 * k22 * h,
                 yi_RK2[iter - 1] + 0.5 * k32 * h,
                 yr_RK2[iter - 1] + 0.5 * k42 * h, B, phi, gamma)
        k53 = dp(yi_RK4[iter - 1] + 0.5 * k42 * h, u)

        k14 = ds(ys_RK4[iter - 1] + 0.5 * k13 * h,
                 ye_RK2[iter - 1] + 0.5 * k23 * h,
                 yi_RK2[iter - 1] + 0.5 * k33 * h,
                 yr_RK2[iter - 1] + 0.5 * k43 * h, a_e, a_i, gamma)
        k24 = de(ys_RK4[iter - 1] + 0.5 * k13 * h,
                 ye_RK2[iter - 1] + 0.5 * k23 * h,
                 yr_RK2[iter - 1] + 0.5 * k43 * h, a_e, a_i, k, phi)
        k34 = di(ye_RK4[iter - 1] + 0.5 * k23 * h,
                 yi_RK2[iter - 1] + 0.5 * k33 * h, k, B, u)
        k44 = dr(ye_RK4[iter - 1] + 0.5 * k23 * h,
                 yi_RK2[iter - 1] + 0.5 * k33 * h,
                 yr_RK2[iter - 1] + 0.5 * k43 * h, B, phi, gamma)
        k54 = dp(yi_RK4[iter - 1] + 0.5 * k43 * h, u)

        ys_RK4[iter] = ys_RK4[iter - 1] + (h / 6.0) * (k11 + 2 * k12 + 2 * k13 + k14)
        ye_RK4[iter] = ye_RK4[iter - 1] + (h / 6.0) * (k21 + 2 * k22 + 2 * k23 + k24)
        yi_RK4[iter] = yi_RK4[iter - 1] + (h / 6.0) * (k31 + 2 * k32 + 2 * k33 + k34)
        yr_RK4[iter] = yr_RK4[iter - 1] + (h / 6.0) * (k41 + 2 * k42 + 2 * k43 + k44)
        yp_RK4[iter] = yp_RK4[iter - 1] + (h / 6.0) * (k51 + 2 * k52 + 2 * k53 + k54)

    return t, ys_EulerMod, ye_EulerMod, yi_EulerMod, yr_EulerMod, yp_EulerMod

'''
# vector = [s(t),e(t),i(t),r(t),p(t)]
plt.figure()
plt.plot(t, ys_RK4, '-', color="blue", label="s(t)")
plt.plot(t, ye_RK4, '-', color="cyan", label="e(t)")
plt.plot(t, yi_RK4, '-', color="red", label="i(t)")
plt.plot(t, yr_RK4, '-', color="lime", label="r(t)")
plt.plot(t, yp_RK4, '-', color="k", label="p(t)")
plt.xlabel("t", fontsize=15)
plt.ylabel("Population Ratio", fontsize=15)
plt.title("Runge-Kutta 4")
plt.legend()
plt.grid(1)
'''
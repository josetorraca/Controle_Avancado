# Model parameters for the Van de Vusse CSTR
# Assumptions:

# Libraries
from casadi import *

# Sampling time
dt = 0.1/40

# Parameters
k10 = 1.287e12 #1st reaction frequency factor (h-1)
k20 = 1.287e12 #2nd reaction frequency factor (h-1)
k30 = 9.043e9 #3rd reaction frequency factor (L/mol L)
E1 = 9758.3  #1st reaction activation energy /R (K)
E2 = 9758.3 #2nd reaction activation energy /R (K)
E3 = 8560 #3rd reaction activation energy /R (K)
deltaH1 = 4.2  #1st reaction enthalpy (kJ/mol)
deltaH2 = -11 #2nd reaction enthalpy (kJ/mol)
deltaH3 = -41.85 #3rd reaction enthalpy (kJ/mol)
rho = 0.9342 #density (kg/L)
cp = 3.01 #heat capacit (kJ/kg K)
Ar = 0.215 #jacket area (m2)
Kw = 4032 #jacket heat transfer coefficient (kJ/h m2 K)
V = 10 #reactor volume (L)
Cp_k = 2.0 # Coolant heat capacity [kj/kg.k]
A_R = 0.215 # Area of reactor wall [m^2]
m_k = 5.0 # Coolant mass[kg]

# Auxiliary terms
K_1 = k10 * exp((-E1)/((T_R+273.15)))
K_2 =  k20 * exp((-E2)/((T_R+273.15)))
K_3 = k30 * exp((-E3)/((T_R+273.15)))

# States
Ca = MX.sym('C_A',1) #yield of A (mol/L)
Cb = MX.sym('C_B',1) #yield of B (mol/L)
T = MX.sym('T',1) #system temperature (C)
x = vertcat(Ca, Cb, T)
c = vertcat(Cb, T) #controlled variables

# Outputs
y = vertcat(Ca, Cb, T)

# Inputs
f = MX.sym('F/V',1) #spacial velocity (h-1)
Tk = MX. sym('T_k',1) #jacket temperature (C)
u = vertcat(f, Tk)

# Disturances
Cain = MX.sym('C_Ain',1) #inlet yield of A
Tin = MX.sym('T_in',1)  #inlet temperature
d = vertcat(Cain, Tin)

# ODE system
dx1 = f*(Cain - Ca) - Ca*k10*exp(-E1/(T + 273.15)) - Ca**2*k30*exp(-E3/(T + 273.15))
dx2 = -f*Cb + Ca*k10*exp(-E1/(T + 273.15)) - Cb*k20*exp(-E2/(T + 273.15))
dx3 = f*(Tin - T) + (Kw*Ar*(Tk - T)/V + (Ca*(-deltaH1)*k10*exp(-E1/(T + 273.15))) \
+ (Cb*(-deltaH2)*k20*exp(-E2/(T + 273.15))) + (Ca**2*(-deltaH3)*k30*exp(-E3/(T + 273.15))))/(rho*cp)
dx = vertcat(dx1, dx2, dx3)

# Cost function
J = - (Cb/(Cain-Ca) + Cb/Cain - 0.06*Tk/100)

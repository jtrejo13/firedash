# -*- coding: utf-8 -*-

#fuel_species = 'H2:1'#H2
#fuel_species = {'H2':1}                 #Hydrogen Fuel
#fuel_species = 'C3H8:1'#Propane
#fuel_species = 'CO:0.5, H2:0.5'#H2 CO Mix

#fuel_species = 'CH4:1'#CH4
#fuel_species = 'CO2:0.011502545, CO:0.001180986, H2:0.00984, CH4:0.00189584, C2H4:0.001874703, C2H6:0.000997333, C3H8:0.005483636'#50 Percent Charge 
fuel_species = 'CO2:0.033698864, CO:0.023411161, H2:0.0283925, CH4:0.00654975, C2H4:0.002303411, C2H6:0.001314667,  C3H8:0.009136364'#100 Percent Charge C
#fuel_species = 'CO2:0.0563445, CO:0.0601125, H2:0.073062, CH4:0.0201966, C2H4:0.027186557, C2H6:0.0035904,  C3H8:0.011972727'#150 Percent Charge 

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import matplotlib as mpl
import cantera as ct
from explosion_model import *
"""
Created on Wed Oct 24 12:31:30 2018

@author: erik
"""



# Gas Properties Inputs
gas = inp(
            air =  {'O2':1, 'N2':3.76},
            fuel = fuel_species,
            phi = 1.0,                             # Composition
            f = 1.0, 
            P = Patm,                         # Initial Pressure
            T = 298,                              # Initial unburned gas temperature K
            S = 0.45
        )


# Room Geometry Inputs
geom = inp(
                #R = 0.198,                              #Radius (m)
                R = 0.378,
                Cd = 0.50,                              #Coefficient for vent
                Av = 0.0929                             #Vent Area (m2)
            )
#Control Inputs
cntrl = inp(
            tmax = 0.35                            #Max Time for analysis
            )

gas.fuel = fuel_species
r = explosion(gas=gas, geom=geom, cntrl=cntrl)
r.run()
fuel_conc = 1-sum(r.gas_u['N2','O2'].X)
print(r.P_.max(), r.Pf_, r.Tb, fuel_conc)
plt.plot(r.t,r.P_)
P = psi(np.nanmax(r.P_))
plt.show()




\
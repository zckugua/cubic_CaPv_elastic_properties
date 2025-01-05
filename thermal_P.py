#!/usr/bin/env python
# coding: utf-8

# In[11]:


from scipy import constants
from scipy.integrate import quad
import numpy as np
import casio3

class Thermal:
    def __init__(self):
        self.V0 = 46.271  # Initial volume (A^3)
        self.T0 = 700     # Initial temperature (K)
        self.g0 = 1.605   # Initial gamma value
        self.d0 = 1000    # Initial Debye temperature
        self.natoms = 5   # Number of atoms per formula unit

        # para_th parameters
        self.para_th = [3.141999407109362323e+02,
                        7.184194765633802149e+01,
                        7.586260665946504590e-03,
                        1.193027453280096686e-04,
                        -1.477624426251083416e-07]

        # para_mgd parameters
        self.para_mgd = [3.179905585397977461e+02,
                         6.242490299331557679e+01,
                         1.645532798344669700e+00,
                         1.031634865338042717e+00]

    def P_th(self, V, T):
        """
        Calculate the thermodynamic pressure based on volume and temperature.
        V: Volume (A^3)
        T: Temperature (K)
        Returns: Thermodynamic pressure (GPa)
        """
        b1, b2, b3, b4, b5 = self.para_th
        f = self.V0 / V
        dT = T - self.T0
        return b1 * (f**(7/3) - f**(5/3)) + b2 * ((f**(7/3) - f**(5/3)) * (f**(2/3) - 1)) + \
               b3 * dT + b4 * dT * np.log(1 / f) + b5 * dT**2

    def V_to_rho(self, V):
        """
        Calculate the density (g/cm³) based on the volume.
        V: Volume (A^3)
        Returns: Density (g/cm³)
        """
        return (1 / constants.Avogadro) * casio3.mol_mass / V * 10**24

    def rho_to_V(self, rho):
        """
        Calculate the volume based on the density.
        rho: Density (g/cm³)
        Returns: Volume (A^3)
        """
        return (1 / constants.Avogadro) * casio3.mol_mass / rho * 10**24

    def alpha(self, V, T):
        """
        Calculate the thermal expansion coefficient alpha based on volume and temperature.
        V: Volume (A^3)
        T: Temperature (K)
        Returns: Thermal expansion coefficient
        """
        b1, b2, b3, b4, b5 = self.para_th
        dT = T - self.T0
        return (b3 + b4 * np.log(V / self.V0) + 2 * b5 * dT) / (2 * b1 / 3 - b4 * dT)

    def P_MGD(self, V, T):
        """
        Calculate the pressure under the MGD model based on volume and temperature.
        V: Volume (A^3)
        T: Temperature (K)
        Returns: Pressure under the MGD model (GPa)
        """
        b1, b2, g0, q = self.para_mgd
        f = self.V0 / V
        evA3_GPa = 160.2176634  # Conversion factor: eV/Å³ to GPa
        kb2ev = 8.6173432e-5  # Boltzmann constant in eV/K
        r = 9 * self.natoms * kb2ev * evA3_GPa  # Scaling factor
        theta = self.d0 * np.exp((g0 - g0 * (V / self.V0)**q) / q)  # Debye temperature

        # Calculate the integral part
        integral1, _ = quad(lambda x: x**3 / (np.exp(x) - 1), 0, theta / T)
        integral2, _ = quad(lambda x: x**3 / (np.exp(x) - 1), 0, theta / self.T0)

        # Return the calculated pressure
        return b1 * (f**(7/3) - f**(5/3)) + b2 * ((f**(7/3) - f**(5/3)) * (f**(2/3) - 1)) + \
               g0 * (1 / V) * (1 / f)**q * (r * T * (theta / T)**(-3) * integral1 - r * self.T0 * (theta / self.T0)**(-3) * integral2)
# In[10]:





# In[ ]:





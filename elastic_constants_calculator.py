#!/usr/bin/env python
# coding: utf-8

# In[11]:


import numpy as np

class ElasticConstantsCalculator:
    def __init__(self):
        # Set fitting parameters
        self.popt1 = [309.4081118418427, 6376.992599744389, 7580.806966130982, -0.006393179366540877, -0.45888883056408414, 3.5486321545637804, -38.57637695477636, -22011.72555317583, 41602.402742501814]
        self.popt2 = [131.66872199794992, 1657.649598741598, 7271.260488588483, 0.004768355718547992, 0.0698809108133547, 0.5360909590126943, 9.177940178299652, 11226.6879757742, -20679.319641296155]
        self.popt3 = [198.82388015777929, 1674.745517497173, 1095.022475429396, -0.006895733786630956, -0.15635269293973722, 0.9448765892867974, -161.8693233249202, -3383.545549753873, -34427.2205065156]

        self.e0 = 576.6
        self.e1 = 1913.2
        self.e2 = 67861.1

    def Cij_fit(self, d, t, a0, a1, a2, b0, b1, b2, c0, c1, c2):
        """
        Fitting function to calculate the relationship between elastic constants and density and temperature.
        d: Input density (g/cm³)
        t: Input temperature (K)
        """
        d0 = 4.17
        f = ((d / d0) ** (2 / 3) - 1) * 0.5
        denominator = (t - self.e0 - self.e1 * f - self.e2 * f ** 2)
        denominator = np.where(denominator > 0, denominator, np.nan)  # Avoid negative values in the square root
        result = (a0 + a1 * f + a2 * f ** 2) + \
                 (b0 + b1 * f + b2 * f ** 2) * t + \
                 (c0 + c1 * f + c2 * f ** 2) / np.sqrt(denominator)
        return result

    def calculate_elastic_constants(self, density_value, temperature_value):
        """
        Calculate the elastic constants C11, C12, and C44 for the given density and temperature.
        """
        c11_value = self.Cij_fit(density_value, temperature_value, *self.popt1)  # Pass 10 parameters
        c12_value = self.Cij_fit(density_value, temperature_value, *self.popt2)  # Pass 10 parameters
        c44_value = self.Cij_fit(density_value, temperature_value, *self.popt3)  # Pass 10 parameters

        return c11_value, c12_value, c44_value

    def set_fitting_parameters(self, popt1, popt2, popt3):
        """
        Set fitting parameters. Use this method to update the fitting parameters if new ones are available.
        """
        self.popt1 = popt1
        self.popt2 = popt2
        self.popt3 = popt3
# In[10]:





# In[ ]:

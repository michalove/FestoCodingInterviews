#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demo 2: plot optimal pd-parameters over masses
"""

import numpy as np
import matplotlib.pyplot as plt

# values are computed offline (took about 2 minutes)

data = np.load('pd_parameters.npz')
masses = data['masses']
x_opt = data['x_opt'].T

print('Data is stored in "pd_parameters.txt"')
plt.plot(masses, x_opt)
plt.xlabel('Mass')
plt.ylabel('Optimal Controller Parameters')
plt.legend(['K_p', 'K_d'])
plt.show()

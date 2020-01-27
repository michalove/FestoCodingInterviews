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


#%% This is how to generate this data

#def make_obj_fun(m):
#    def objective_function(params):
#        kp = params[0]
#        kd = params[1]
#        sys =  Robot2([m, 0, 0])
#        ctrl = PDController(kp,kd)
#        
#        sim = Simulation(sys, ctrl, w, 20)
#        t_,y_,u_,w_ = sim.run()
#        return np.linalg.norm(y_-w_) + 0.01* np.linalg.norm(u_)
#    return objective_function 

  

#masses = np.linspace(0, 10, 51)
#x0 = np.array([40,3])
#x_opt = np.zeros((2,len(masses)))
#f_opt = np.zeros(len(masses))


#for i,m in enumerate(masses):
#    print('.',end='')
#    f = make_obj_fun(m)
#    results = optimize.minimize(f, x0)
#    x_opt[:,i] = results.x
#    f_opt[i] = results.fun
#    x0 = results.x
    
# np.savez('pd_parameters.npz', masses = masses, x_opt = x_opt, f_opt = f_opt)


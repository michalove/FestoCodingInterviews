#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demo 3 - identifying mass

leaving out center of gravity
"""
from systems import Robot2
from controllers import PDController
from simulation import ParticleFilter
from trajectories import jump_trajectory
import numpy as np
import matplotlib.pyplot as plt


#%%
# the 'true robot'
mass_true = 3
robot = Robot2( [mass_true, 0 , 0] )

controller = PDController(54.16, 14.04)

p0 = np.zeros((51, 3))
p0[:,0] = np.linspace(0,10,51)

pf = ParticleFilter(robot, Robot2, controller, p0, jump_trajectory, t_end = 20)

t, y, u, w, m, v = pf.run()
v = np.sqrt(v)

plt.figure(figsize=(7,10))
plt.subplot(2,1,1)
plt.plot(t, y, t, w,'--')
plt.ylabel('Trajectory')

plt.subplot(2,1,2)
plt.fill_between(t, m[:,0]-v[:,0], m[:,0]+v[:,0], color = '0.8')
plt.plot(t ,m[:,0],'k', t, np.full_like(m, mass_true),'--')
plt.ylim([0,10])
plt.ylabel('Mass estimate')
plt.xlabel('Time')
plt.show()
#%% The particle filter can also identify center of gravity

# param_true = [1, 0.1, -0.1]
    
# robot = Robot2(param_true)
# controller = PDController(52, 16)
# n_params = 3
# n_sample = 50
# p0 = np.random.rand(n_sample, n_params)
# p0[:,0] *=10
# p0[:,1] -= 0.5
# p0[:,2] -= 0.5
# p0[:,1] *= 0.2
# p0[:,2] *= 0.2
# p0[-1,:] = param_true

# t_end = 20

# pf = ParticleFilter(robot, Robot2, controller, p0, jump_trajectory, t_end)
# t, Y, U, W, M, v = pf.run()
# v = np.sqrt(v)

# plt.plot(t,Y, t,W,'--')
# plt.show()

# plt.autoscale(True, 'both', tight=True)
# plt.figure(figsize=(6,15))
# for i in range(3):
#     plt.subplot(3,1,i+1)
#     plt.fill_between(t, M[:,i]-v[:,i], M[:,i]+v[:,i], color = '0.8')
#     plt.plot(t,M[:,i],'k', t, np.full_like(M, param_true[i]),'--')

# plt.show()
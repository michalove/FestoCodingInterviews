#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demo 1 - Showcase: the correct controller is important
"""

from systems import Robot2
from controllers import PDController
from simulation import Simulation
from trajectories import jump_trajectory
import matplotlib.pyplot as plt

robot1 = Robot2( [1,0,0] ) # mass = 1, center of gravity = (0,0)
robot2 = Robot2( [10,0,0] ) # mass = 1, center of gravity = (0,0)

controller1 = PDController(51.89, 8.32) # kp and kd found by trial and error
controller2 = PDController(55.80, 25.52) # kp and kd found by trial and error

robots = [robot1, robot2]
controllers = [controller1, controller2]

simulations = [Simulation(r, c, jump_trajectory, t_end = 20) 
               for r in robots for c in controllers]

outputs = [s.run() for s in simulations]

t = [output[0] for output in outputs]
y = [output[1] for output in outputs]
w = [output[3] for output in outputs]

plt.figure(figsize=(15,10))

for i in range(4):
    plt.subplot(2,2,i+1)
    plt.plot(t[i], y[i], t[i], w[i],'--')

plt.subplot(2,2,1)
plt.title('controller for mass =1')
plt.ylabel('mass = 1')

plt.subplot(2,2,2)
plt.title('controller for mass = 10')

plt.subplot(2,2,3)
plt.ylabel('mass = 10')
    
plt.show()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demo 0 - hello robot
"""

from systems import Robot2
from controllers import PDController
from simulation import Simulation
from trajectories import jump_trajectory
import gui

robot = Robot2( [1,0,0] ) # mass = 1, center of gravity = (0,0)

controller = PDController(50, 20) # kp and kd found by trial and error

sim = Simulation(robot, controller, jump_trajectory, t_end = 20)
sim.init_run()

def robot_update():
    y,u,w = sim.step()
    return -y, -w

gui.set_update_function(robot_update)

gui.start_gui()
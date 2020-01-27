#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trajectories as input for the controll loop
"""
import numpy as np

def jump_trajectory(t):
    t = np.floor(0.25*t+0.75)
    pos = np.array([-np.cos(t)+1, 2*np.sin(1.7*t)])
    der = 0*np.array([np.sin(t), 3.4*np.cos(t)])
    return pos, der

def wiggle(t):
    pos = np.array([0, np.sin(10*t)])
    der = np.array([0, 10*np.cos(10*t)])
    return pos, der
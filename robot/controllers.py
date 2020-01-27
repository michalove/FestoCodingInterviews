#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PID and PD Controllers
"""
from scipy import optimize
import numpy as np

class Controller:
    
    def __init__(self, params):
        pass
    
    def control(y, w, dt):
        pass
    
    def reset():
        pass
  
class PIDController:
    
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.I = 0
        
    def control(self, y, dy, w, dw, dt):
        err = w - y
        derr = dw - dy
        self.I += err * dt
        
        u = self.kp * err + self.kd * derr + self.ki * self.I
        return u
    
class PDController():
    def __init__(self, kp, kd):
        self.kp = kp
        self.kd = kd
        
    def control(self, y, dy, w, dw, dt):
        err = w - y
        derr = dw - dy
        
        u = self.kp * err + self.kd * derr
        return u
    
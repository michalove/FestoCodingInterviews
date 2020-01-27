#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Provides two classes:
    - Simulation (runs controller and system in turn)
    - ParticleFilter (same as Simulation, but identifies mass etc.)
"""
import numpy as np
import matplotlib.pyplot as plt

class Simulation:
    
    def __init__(self, system, controller, w, t_end, dt = 1/60):
        self.system = system
        self.controller = controller
        self.w = w
        self.t_end = t_end
        self.dt = dt
        
        n_timesteps = int(self.t_end / self.dt) + 1
        self.t_idx = 0
        self.time = np.linspace(0, self.t_end, n_timesteps)
        self.i_iter = 0
        
    def init_run(self):
        self.system.reset()
        
        y = self.system.y
        dy = self.system.dy

        w, dw = self.w(0.)
        self.u = self.controller.control(y, dy, w, dw, self.dt)        
    
    def step(self):
        self.i_iter += 1
        t = self.dt * self.i_iter
        y, dy = self.system.step(self.u, self.dt)        
        w, dw = self.w(t)
        u = self.controller.control(y, dy, w, dw, self.dt)
        self.u = u
            
        return y, u, w
    
    def run(self):
        self.init_run()
        y = self.system.y
        
        y_list = np.zeros((self.time.size, len(y)))
        u_list = np.zeros((self.time.size, len(self.u)))
        w_list = np.zeros((self.time.size, len(y)))
        
        y_list[0,:] = y
        u_list[0,:] = self.u
        w_list[0,:] = self.w(0.)[0]
        
        self.i_iter = 0
        while self.i_iter < self.time.size-1:
            y, u, w = self.step()
            
            y_list[self.i_iter,:] = y
            u_list[self.i_iter,:] = u
            w_list[self.i_iter,:] = w  
            
        return self.time, y_list, u_list, w_list    
           
class ParticleFilter:
    
    def __init__(self, system, system_class, controller, p0, w, t_end, dt=1/60):
        self.system = system # real system
        self.system_class = system_class # class of real system

        self.controller = controller
        self.p0 = p0.copy()
        self.w = w
        self.t_end = t_end
        self.dt = dt
        n_timesteps = int(self.t_end / self.dt) + 1
        self.time = np.linspace(0, self.t_end, n_timesteps)
        
        self.system_list = [self.system_class(p) for p in self.p0]
        
        
    def run(self):
        self.system.reset()
        [system.reset() for system in self.system_list]
        y = self.system.y
        dy = self.system.dy
        
        n_param = self.p0.shape[1]
        sample_size = self.p0.shape[0]
        
        y_list = np.zeros((self.time.size, len(y)))
        y_list[0,:] = y
        
        u_list = np.zeros((self.time.size, len(y)))
        p_list = np.zeros((self.time.size, n_param))
        var_list = np.zeros((self.time.size, n_param))
        

        weights = np.ones((sample_size))
        uniform_weights = np.ones((sample_size))
        p_list[0] = self.p0.mean()
        var_list[0] = self.p0.var()
        
        sigma2 = 0.0001 # sigma squared
        alpha = 0.001 # probability of changing mass
        
        state = self.system.get_state()        
        [system.set_state(state) for system in self.system_list]        
          
        for i,t in enumerate(self.time[:-1]):                       
            w, dw = self.w(t)
            u = self.controller.control(y, dy, w, dw, self.dt)
            
            # get position for all systems
            y, dy = self.system.step(u, self.dt)
            Y = np.array([system.step(u, self.dt)[0] for system in self.system_list])
            
            y_list[i+1,:] = y
            u_list[i,:] = u

            # filter
            measurement = y
            residual = np.linalg.norm(Y-measurement[np.newaxis,:], axis=1)
            weight_update = np.exp(-residual/(2*sigma2))/np.sqrt(2*np.pi*sigma2)
            weights *= weight_update
            weights /= weights.mean()
            weights = (1-alpha)*weights + alpha * uniform_weights

            p_mean = np.average(self.p0, axis=0, weights = weights)
            p_var = np.average( (self.p0-p_mean)**2, axis=0, weights = weights)
            p_estimate = p_mean
            p_list[i+1] = p_estimate
            var_list[i+1] = p_var

            # recreate systems
            state = self.system.get_state()
            [system.set_state(state) for system in self.system_list]
            
            
        
        w, dw = self.w(t)
        u = self.controller.control(y, dy, w, dw, self.dt)
        u_list[-1,:] = u
        
        w_list = np.array([self.w(t)[0] for t in self.time])
        
        return self.time, y_list, u_list, w_list , p_list , var_list    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
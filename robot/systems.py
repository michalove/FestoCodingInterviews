#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Provides two exemplary systems, called Robot1 and Robot2
The final exercise only uses Robot2
"""
import numpy as np

class System:
    
    def __init__(self, params):
        pass
    
    def reset(self):
        pass
    
    def step(self, u, dt):
        pass
    
    def get_state(self):
        return self.y.copy(), self.dy.copy()
    
    def set_state(self,state):
        a,b = state
        self.y = a.copy()
        self.dy = b.copy()
        
    def step_response(self):
        self.reset()
        response = [self.step(1,1/60)[0] for i in range(60)]
        self.reset()
        return np.array(response)
        
    
class Robot1(System):
    
    def __init__(self, mass, friction):
        self.mass = mass
        self.friction = friction
        self.reset()
        
    def reset(self):
        self.y =np.array([ 0.0])
        self.dy = np.array([0.0])
        
    def step(self, u, dt):
        
        ddy = 1/self.mass * u - self.friction * self.dy
        self.dy += ddy * dt
        self.y += self.dy * dt
        
        return self.y, self.dy

        
    
class Robot2(System):
    l = [1, 0.8]
    m = [.2, 0.2]
    friction = np.array([.1, 0.1])
    amplify = np.array([5,1])
    g = 0
    
    def __init__(self, params):
        self.mo, self.xo, self.yo = params
        self.reset()
        
    def reset(self):
        self.y = np.array([0.,0.])
        self.dy = np.array([0.,0.])

    def print_params(self):
        print('mo = {}, xo = {}, yo = {}'.format(self.mo, self.xo, self.yo))
        
    def step(self, u, dt):
        angles = self.y.copy()
        omega = self.dy.copy()
                
        cosb = np.cos(angles[1])
        sinb = np.sin(angles[1])
        l0 = self.l[0]
        l1 = self.l[1]
        I0 = l0**2 * self.m[0] + \
            ((l0+cosb*l1)**2 + (sinb*l1)**2) * self.m[1] + \
            ((l0 + (l1+self.xo)*cosb-self.yo*sinb)**2 + \
                ((l1+self.xo)*sinb + self.yo*cosb)**2 )* self.mo
        I1 = l1**2 * self.m[1] + \
            ((l1+self.xo)**2 + self.yo**2) * self.mo
        
        I = np.array([I0, I1])
        #print(I)
        cosa = np.cos(angles[0])
        cosab = np.cos(angles[0]+angles[1])
        g0 = cosa * (self.m[0]+self.m[1]+self.mo) * self.g * l0
        g1 = cosab * (self.m[1]+self.mo) * self.g * l1
        u_gravity = np.array([g0,g1])

        a = (self.amplify*u+u_gravity)/I - self.friction * omega
        omega += a * dt
        angles += omega * dt
        
        self.y = angles
        self.dy = omega
        
        return self.y.copy(), self.dy.copy()
        
        
        
        
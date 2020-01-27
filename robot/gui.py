#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Functionality for displaying the robot on screen
"""

import pyglet
from pyglet.window import key
from math import pi
import numpy as np


keyboard = pyglet.window.key.KeyStateHandler()
pyglet.gl.glLineWidth(4)

batch = pyglet.graphics.Batch()
layer = [pyglet.graphics.OrderedGroup(i) for i in range(4)]

arm1 = pyglet.image.load('img/arm1.png')
arm1.anchor_x = 5
arm1.anchor_y = 50

arm2 = pyglet.image.load('img/arm2.png')
arm2.anchor_x = 16
arm2.anchor_y = 16+40

joint = pyglet.image.load('img/joint.png')
joint.anchor_x = 10
joint.anchor_y = 10

mount = pyglet.image.load('img/mount.png')
mount.anchor_x = 10
mount.anchor_y = 10

sprites = [
    pyglet.sprite.Sprite(arm1, batch=batch, group = layer[2], subpixel = True),
    pyglet.sprite.Sprite(arm2, batch=batch, group = layer[2], subpixel = True),
    pyglet.sprite.Sprite(mount, batch=batch, group = layer[3], subpixel = True),
    pyglet.sprite.Sprite(joint, batch=batch, group = layer[3], subpixel = True),
    pyglet.sprite.Sprite(arm1, batch=batch, group = layer[0], subpixel = True),
    pyglet.sprite.Sprite(arm2, batch=batch, group = layer[0], subpixel = True),
    pyglet.sprite.Sprite(joint, batch=batch, group = layer[1], subpixel = True),    
    ]

l1 = 1
l2 = 0.8
scale = 100

def update_coordinates(angles, w):
    x0 = 320
    y0 = 360
    
    x1 = -np.cos(angles[0]) * l1 * scale
    y1 =  np.sin(angles[0]) * l1 * scale
    
    x2 = -np.cos(angles[0]+angles[1]) * l2 * scale
    y2 =  np.sin(angles[0]+angles[1]) * l2 * scale
    
    sprites[0].x = x0 + 0.5*x1
    sprites[0].y = y0 + 0.5*y1
    sprites[0].rotation = angles[0] / pi * 180 + 90
    
    sprites[1].x = x0 + x1 + 0.5*x2
    sprites[1].y = y0 + y1 + 0.5*y2
    sprites[1].rotation = (angles[0]+angles[1])/pi*180+90
    
    sprites[2].x = x0
    sprites[2].y = y0
    
    sprites[3].x = x0 + x1
    sprites[3].y = y0 + y1  
    
    angles = w
    
    x1 = -np.cos(angles[0]) * l1 * scale
    y1 =  np.sin(angles[0]) * l1 * scale
    
    x2 = -np.cos(angles[0]+angles[1]) * l2 * scale
    y2 =  np.sin(angles[0]+angles[1]) * l2 * scale
    
    sprites[4].x = x0 + 0.5*x1
    sprites[4].y = y0 + 0.5*y1
    sprites[4].rotation = angles[0] / pi * 180 + 90
    sprites[4].opacity = 100
    
    sprites[5].x = x0 + x1 + 0.5*x2
    sprites[5].y = y0 + y1 + 0.5*y2
    sprites[5].rotation = (angles[0]+angles[1])/pi*180+90
    sprites[5].opacity = 100
    
    sprites[6].x = x0 + x1
    sprites[6].y = y0 + y1 
    sprites[6].opacity = 100    

def set_update_function(fun):
    def update(dt):
        y, w = fun()
        update_coordinates(y,w)
        
    pyglet.clock.schedule_interval(update, 1/60.0)



def start_gui():
    window = pyglet.window.Window()
    
    @window.event
    def on_draw():
        window.clear()
        pyglet.gl.glClearColor(0.8,0.8,0.8,1)
        batch.draw()
    
    pyglet.app.run()
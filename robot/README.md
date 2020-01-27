## Handling of unknown Objects

### Quickstart

Just run `demo0.py` to `demo3.py`.

The code uses `numpy`, `scipy.optimize`, `matplotlib.pyplot` and `pyglet` (for visualization).

### Approach
#### Challenges
  1. System description: find equations to model the robot's physics (given control input)
  2. Control: Given known physical parameters (mass and center of gravity), design a stable and reliable controller for the robot. The controller is a function of mass and center of gravity
  3. Identify mass and center of gravity based on sensor data. Sensors are in the robot joints and measure the robots position (angles, angular velocities)
  4. Put together an adaptive controller. Loop over these steps: (1) start controlling robot with an estimate of mass and center of gravity (e.g. mass = 0). Only do one timestep. (2) use sensor data to update estimates of mass and center of gravity. (3) Adapt controller parameters to mass and center of gravity
  5. Everything needs to be fast, so the robot can run in real-time. Might require offline-computations
  6. Inverse Kinematics 
  7. Compensate for gravity, if using a PID-Controller (the robot is elastic...).

#### Simplifications

Given the exercise description, I found 2., 3., 4. and 5. to be the most interesting. Therefore I made the following simplifications:

  1. System description: I assume a 2d-robot with only two joints. It still has enough degrees of freedom to identify mass and center of gravity. The model I chose is nonlinear (things can rotate, so many sine and cosines are involved). Many parameters in my model are tweaked to make the animation "look good". This is enough for a proof-of-concept. In a real industry setting, a model would probably come from the robot design department.
  2. Inverse Kinematics: To simplify this, I only worked in robot state space, not in cartesian space.
  3. Compensate for gravity: I assume zero gravity (you are looking at the robot from birds-eye-view). Mass can still be identified, because it makes the system more inert.
  
### Demos

#### Demo 0 - hello robot.

This is the robot. It is controlled to assume a sequence of positions.

#### Demo 1 - why do we need to identify mass etc.?
We test the robot in two situations. First with a light object (case 1), and then with a very heavy object (case 2). We try out both cases with two different controllers. One optimized for case 1 (->controller 1) and one optimized for case 2 (-> controller 2).

The output is shown in the plots (joint angles over time). If the controller does not match the case, then the robot is either slower than necessary or becomes unstable.

#### Demo 2 - Adapt controller to mass and center of gravity
For a given set of parameters (mass, center of gravity), we can find optimal controller parameters by mathematical optimization. The objective function is the squared deviation from the trajectory plus the squared effort.

For this and all other demos, we use a PD-Controller. So we only need to find two parameters K_p and K_d.

Optimization takes some time, so we cannot do it online. Instead, we sample the full space (m, x, y) of possible masses and centers of gravity and save the results in an offline phase. During runtime we can interpolate this data and find an "almost optimal" controller for any set of parameters.

For simplicity we consider the parameters only as a function of mass (an not of the center of gravity). This demo shows the plot of the two parameters K_p and K_d as a function of mass (between 0 and 10). Values were precomputed and saved.

#### Demo 3 - Identifying mass and center of gravity
These parameters are identified with a particle filter (similar to Kalman filter). We generate a sample of possible parameter values. In each time step, we predict the system response using the full sample (each sample point generates one prediction). We then compare the predictions with the actual measurement and reweight the particles. From time to time, we need to resample.

A particle filter has the advantage, that it does not assume the parameters to be constant over time. So if the mass changes, the robot can react quickly.

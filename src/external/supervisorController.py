from controller import *
from numpy import *
import sys
sys.path.append("/Users/Chelsea/Desktop/ASLresearch/codeRepo/src/src")
from controllerarena.controllers import refVec as rv

class SupervisorController (Supervisor): 
  def run(self):
    emitter = self.getEmitter('emitter')
    emitter.setChannel(1)    
    robot = self.getFromDef('PIONEER')
    # get initial state
    robot_loc = robot.getPosition()
    R = robot.getOrientation() # returns 9-vector
    robot_ang = pi + (pi - arccos(R[0]))*sign(R[6])
    
    # Initialize controller
    controller_flag = 3 # PD control
    # x0 is initial state. get from robot
    x0 = array([ [robot_loc[2]], [robot_loc[0]], [robot_ang] ])
    y=x0 # for tol and stopping purposes, y must be defined
    C = rv.refVec(x0, controller_flag)
    # initialize ref (where you want the robot to go)
    ref = array([[3], [2], [2]])   
    # initialize dt 
    dt = .032
    # simulation tolerance
    tol=.1
    
    
    while (abs(linalg.norm(y-ref)) > tol):
      self.step(32)  
      # get state
      robot_loc = robot.getPosition()
      R = robot.getOrientation() # returns 9-vector corresponding to a DCM representing the transformation between global and body coordinates
        # the following line obtains the orientation angle with the correct sign and magnitude, regardless of quadrant
      robot_ang = pi + (pi - arccos(R[0]))*sign(R[6])
      y = array([ [robot_loc[2]], [robot_loc[0]], [robot_ang] ])
        # here is the command that calls the refVec field
      u = C.get_output(ref, y, dt) 
    # translate v and w to wheel speeds
      wheelSpeeds = self.velocitiesToWheelSpeeds(u)
      emitter.send(wheelSpeeds)
      
  def velocitiesToWheelSpeeds(self, u):
    # need certain parameters that are a function of specific robot,
    # such as distance between wheels and radius of wheels. These numbers were obtained from the Pioneer 3dx model
    r = 0.0975 # wheel radius
    d = 0.136*2 # called "axle length"
    v = -u[0][0]
    w = u[1][0]
    ul = v/r - d*w/(2*r)
    ur = v/r + d*w/(2*r)
    wheelSpeeds = "%f, %f" % (ul, ur)
    return wheelSpeeds
      
controller = SupervisorController()
controller.run()

from controller import *
from math import pi
from numpy import arccos, sign, array
from socket import *

class SupervisorController (Supervisor):
  def startup(self):
    HOST = '127.0.0.1'
    PORT = 8082
    self.s = socket(AF_INET, SOCK_STREAM)
    self.s.bind((HOST, PORT))
    self.s.listen(1)
    self.conn, addr = self.s.accept()

  def velocitiesToWheelSpeeds(self, u):
    # need certain parameters that are a function of specific robot,
    # such as distance between wheels and radius of wheels
    r = 0.0975
    d = 0.136*2 # called "axle length"
    v = -u[0][0]
    w = u[1][0]
    ul = v/r - d*w/(2*r)
    ur = v/r + d*w/(2*r)
    wheelSpeeds = "%f, %f" % (ul, ur)
    #print wheelSpeeds
    return wheelSpeeds

  def run(self):
    emitter = self.getEmitter('emitter')
    emitter.setChannel(1)
    pioneer = self.getFromDef('PIONEER')
    # epuck = self.getFromDef('EPUCK')
    # epuck_trans = epuck.getField('translation')
    # epuck_rot = epuck.getField('rotation')
    # ref_z = -0.25
    # skp = 3000;
    while 1:
      self.step(32)
      datum = self.conn.recv(1024)
      if not datum:
        break
      datum = datum[1:-1].split('\n')
      u = map(lambda x: float(x.strip()[1:-1].strip()), datum)
      u = array([[u[0]], [u[1]]])
      command = self.velocitiesToWheelSpeeds(u)
      emitter.send(command)
      pos = pioneer.getPosition()
      ori = pi + (pi - arccos(pioneer.getOrientation()[0]))*sign(pioneer.getOrientation()[6])
      y = array([[pos[2]], [pos[0]], [ori]])
      y = str(y)
      self.conn.sendall(y)
    emitter.send('0,0')
    self.s.close()

controller = SupervisorController()
controller.startup()
controller.run()

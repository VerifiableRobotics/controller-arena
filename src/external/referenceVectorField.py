from controller import *
from numpy import *

class MyRobot (Robot):
  def run(self):
    # get receiver
    receiver = self.getReceiver('receiver')
    receiver.enable(32)
    # get motor instance
    wheelL = self.getMotor('left_wheel')
    wheelR = self.getMotor('right_wheel')
    # a silly thing you have to do, kind of a hack
    wheelL.setPosition(float('inf'))
    wheelR.setPosition(float('inf'))
    
    while (1):
      self.step(32);
      if receiver.getQueueLength()>0 :
        # parse the message
        message = receiver.getData()
        receiver.nextPacket()
        v = message.split(',')
        v = map(lambda x: float(x), v)
        # set motor speed
        wheelL.setVelocity(v[0])
        wheelR.setVelocity(v[1])
           
robot = MyRobot()
robot.run()

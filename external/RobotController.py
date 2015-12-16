from controller import *

class MyRobot (Robot):
  def run(self):
    left_wheel = self.getMotor('left_wheel')
    right_wheel = self.getMotor('right_wheel')
    receiver = self.getReceiver('receiver')
    receiver.setChannel(1);
    receiver.enable(32)
    left_wheel.setPosition(float('inf'))
    right_wheel.setPosition(float('inf'))
    while (1):
      self.step(32);
      if receiver.getQueueLength()>0 :
        message = receiver.getData()
        receiver.nextPacket()
        v = message.split(',')
        v = map(lambda x: float(x), v)
        left_wheel.setVelocity(v[0])
        right_wheel.setVelocity(v[1])
      #print "LEFT:", left_wheel.getVelocity()
      #print "RIGHT:", right_wheel.getVelocity()



robot = MyRobot()
robot.run()

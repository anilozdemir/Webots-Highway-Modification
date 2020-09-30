# antBot-controller, controlled by supervisor
from controller import Robot
import numpy as np
import sys

class antBot(Robot):
    timeStep = 32
    
    def __init__(self):
        super(antBot, self).__init__()
        self.camera_front = self.getCamera('camera_front')
        self.camera_front.enable(self.timeStep)              
        self.receiver = self.getReceiver('receiver')
        self.receiver.enable(self.timeStep)
        self.Images = []
        
    def run(self):
        while True:
            if self.receiver.getQueueLength() > 0:
                message = self.receiver.getData().decode('utf-8')
                self.receiver.nextPacket()
                if message == 'CAPTURE':
                    image = np.array(self.camera_front.getImageArray())
                    self.Images.append(image)
                elif message == 'FINISH':
                    break
            if self.step(self.timeStep) == -1:
                break

    def save(self, fileName):
        np.save(fileName ,np.stack(self.Images))
        print(f'>> {fileName}.npy is saved!')
        sys.exit(0)

agent = antBot()
agent.run()
agent.save('file')

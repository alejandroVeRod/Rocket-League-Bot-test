import numpy as np
class QTable:
    def __init__(self):
        self.actions=list()
        self.states=list()
    def addAction(self,throttle,steer):
        action={throttle,steer}
        print(action)
        self.actions.append(action)
    def saveActions(self):
        nparray=np.asarray(self.actions)
        print('saving actions...'+str(nparray))
        np.save('actions.npy',nparray)

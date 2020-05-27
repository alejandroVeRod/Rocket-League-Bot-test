import math
import random
from math import sqrt

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from util.orientation import Orientation
from util.vec import Vec3
'''
Links interesantes
https://www.geeksforgeeks.org/epsilon-greedy-algorithm-in-reinforcement-learning/
https://www.freecodecamp.org/news/an-introduction-to-q-learning-reinforcement-learning-14ac0b4493cc/
https://rocketleague.fandom.com/wiki/Points
'''

class MyBot(BaseAgent):
    MIN_DIST:float = 300
    DRAW_PREDICT:bool = False
    timer=60

    def initialize_agent(self):
        # This runs once before the bot starts up
        self.timer=60
        self.controller = SimpleControllerState()

        

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:

        self.timer-=1
        #print(self.timer)
        if(self.timer<0):
            self.timer=90
            self.controller.throttle=float(random.randint(-1,1))
            self.controller.steer=random.randint(-1,1)
            self.controller.pitch=random.randint(-1,1)
            self.controller.yaw=random.randint(-1,1)
            self.controller.roll=random.randint(-1,1)

            jump=random.randint(-1,1)
            if(jump>0):
                self.controller.jump=True
            else:
                self.controller.jump=False
            boost=random.randint(-1,1)
            if(boost>0):
                self.controller.boost=True
            else:
                self.controller.boost=False
            handbrake=random.randint(-1,1)
            if(handbrake>0):
                self.controller.handbrake=True
            else:
                self.controller.handbrake=False


        return self.controller
    


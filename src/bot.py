import math

from math import sqrt
import QTable
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
    qtable=QTable.QTable()

    def initialize_agent(self):
        # This runs once before the bot starts up
        self.controller = SimpleControllerState()
        self.bot_car=None
        self.bot_pos=None
        self.bot_yaw=None
        self.target=None
        self.actions=list
        

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        self.bot_car=packet.game_cars[self.index]
        self.bot_yaw = packet.game_cars[self.index].physics.rotation.yaw
        self.bot_pos = packet.game_cars[self.index].physics.location
        
        ball_location=Vec3(packet.game_ball.physics.location)
        car_location=Vec3(self.bot_car.physics.location)

        self.target=ball_location

        info = self.get_field_info()
        if self.bot_car.boost<=45:
            for boost_pad in info.boost_pads:
                if distanceTo(car_location,boost_pad.location) < self.MIN_DIST:
                    self.target=boost_pad.location
                    

        car_to_ball=ball_location-car_location
        dist_to_ball=car_to_ball.length()

        ball_pos = packet.game_ball.physics.location
        if self.bot_car.boost>45 and dist_to_ball<self.MIN_DIST:
            self.target=ball_pos
            self.controller.boost=True
        else:
            self.controller.boost=False

        if ball_location.z >0:
            self.controller.jump=True
        else:
            self.controller.jump=False

        self.controller.throttle = 1.0
        self.aim(self.target.x,self.target.y)

        self.qtable.addAction(self.controller.throttle,self.controller.steer)
        if(packet.game_info.game_time_remaining<290.0):
            self.qtable.saveActions()
        return self.controller
    
    def aim(self, target_x, target_y):
        angle_between_bot_and_target = math.atan2(target_y - self.bot_pos.y, target_x - self.bot_pos.x)

        angle_front_to_target = angle_between_bot_and_target - self.bot_yaw

        # Correct the values
        if angle_front_to_target < -math.pi:
            angle_front_to_target += 2 * math.pi
        if angle_front_to_target > math.pi:
            angle_front_to_target -= 2 * math.pi

        if angle_front_to_target < math.radians(-10):
            # If the target is more than 10 degrees right from the centre, steer left
            self.controller.steer = -1
        elif angle_front_to_target > math.radians(10):
            # If the target is more than 10 degrees left from the centre, steer right
            self.controller.steer = 1
        else:
            # If the target is less than 10 degrees from the centre, steer straight
            self.controller.steer = 0


def distanceTo(location1,location2):
    return Vec3(location2.x - location1.x, location2.y - location1.y, location2.z - location1.z).length()


def draw_debug_goal(renderer,car,goal):
    renderer.begin_rendering()
    renderer.draw_line_3d(car.physics.location,goal.location,renderer.white())
    renderer.end_rendering()


def draw_prediction(renderer,ball,predicted_location):
    renderer.begin_rendering()
    renderer.draw_line_3d(ball.physics.location,predicted_location,renderer.green())
    renderer.end_rendering()

def draw_debug(renderer, car, ball, action_display):
    renderer.begin_rendering()
    # draw a line from the car to the ball
    renderer.draw_line_3d(car.physics.location, ball.physics.location, renderer.white())

    # print the action that the bot is taking
    renderer.draw_string_3d(car.physics.location, 2, 2, action_display, renderer.white())
    renderer.end_rendering()

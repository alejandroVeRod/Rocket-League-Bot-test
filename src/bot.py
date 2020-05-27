import math
import reinforce_training
from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from util.orientation import Orientation
from util.vec import Vec3



class MyBot(BaseAgent):
    train=reinforce_training.RTrain()
    timer_updateQtable=60
    timer_actions=60
    timer_aim=1500
    bot_pos=None
    bot_yaw=None
    def initialize_agent(self):
        # This runs once before the bot starts up
        self.timer_updateQtable=60
        self.timer_actions=60
        self.controller_state = SimpleControllerState()

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        self.bot_pos=packet.game_cars[0].physics.location
        self.bot_yaw=packet.game_cars[0].physics.rotation.yaw
        self.timer_updateQtable-=1
        self.timer_actions-=1
        self.timer_aim-=1
        self.train.saveFrame(packet,self.controller_state)

        if(packet.game_info.game_time_remaining<1):
            self.train.save_stats(packet)

        if(packet.game_info.game_time_remaining<1):
            self.timer_updateQtable=10
            #self.train.updateQTable(packet,self.controller_state)
            self.train.build_episodes()
            self.train.update_qTable()
        #print(self.timer)
        if(self.timer_actions<0):
            self.timer_actions=100
            actions=self.train.getAction(packet)
            #print("Calculating new actions...")
            self.controller_state.throttle=actions[0]
            self.controller_state.steer=actions[1]
            self.controller_state.pitch=actions[2]
            self.controller_state.yaw=actions[3]
            if(actions[4]>0):
                self.controller_state.jump=True
            else:
                self.controller_state.jump=False
            if(actions[5]>0):
                self.controller_state.boost=True
            else:
                self.controller_state.boost=False
            if(actions[6]>0):
                self.controller_state.handbrake=True
            else:
                self.controller_state.handbrake=False
            self.controller_state.roll=actions[7]
        if(self.timer_aim<0):
            self.timer_aim=150
            self.aim(packet.game_ball.physics.location.x,packet.game_ball.physics.location.y)
        
        
        if(packet.game_info.game_time_remaining>299):
            actions=self.train.getAction(packet)
            self.controller_state.throttle=actions[0]
            self.controller_state.steer=actions[1]
            self.controller_state.pitch=actions[2]
            self.controller_state.yaw=actions[3]
            if(actions[4]>0):
                self.controller_state.jump=True
            else:
                self.controller_state.jump=False
            if(actions[5]>0):
                self.controller_state.boost=True
            else:
                self.controller_state.boost=False
            if(actions[6]>0):
                self.controller_state.handbrake=True
            else:
                self.controller_state.handbrake=False
            self.controller_state.roll=actions[7]




        return self.controller_state
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
            self.controller_state.steer = -1
        elif angle_front_to_target > math.radians(10):
            # If the target is more than 10 degrees left from the centre, steer right
            self.controller_state.steer = 1
        else:
            # If the target is less than 10 degrees from the centre, steer straight
            self.controller_state.steer = 0


def find_correction(current: Vec3, ideal: Vec3) -> float:
    # Finds the angle from current to ideal vector in the xy-plane. Angle will be between -pi and +pi.

    # The in-game axes are left handed, so use -x
    current_in_radians = math.atan2(current.y, -current.x)
    ideal_in_radians = math.atan2(ideal.y, -ideal.x)

    diff = ideal_in_radians - current_in_radians

    # Make sure that diff is between -pi and +pi.
    if abs(diff) > math.pi:
        if diff < 0:
            diff += 2 * math.pi
        else:
            diff -= 2 * math.pi

    return diff


def draw_debug(renderer, car, ball, action_display):
    renderer.begin_rendering()
    # draw a line from the car to the ball
    renderer.draw_line_3d(car.physics.location, ball.physics.location, renderer.white())
    # print the action that the bot is taking
    renderer.draw_string_3d(car.physics.location, 2, 2, action_display, renderer.white())
    renderer.end_rendering()

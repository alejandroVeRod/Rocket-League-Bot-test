import math
from math import sqrt

from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket

from util.orientation import Orientation
from util.vec import Vec3


class MyBot(BaseAgent):
    MIN_DIST:float = 300

    


    def initialize_agent(self):
        # This runs once before the bot starts up
        self.controller_state = SimpleControllerState()

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        info = self.get_field_info()

        ball_location = Vec3(packet.game_ball.physics.location)
        my_car = packet.game_cars[self.index]
        car_location = Vec3(my_car.physics.location)
        goal_to_score=info.goals[my_car.team]
        action_display=""

        car_to_ball = ball_location - car_location

        ball_prediction = self.get_ball_prediction_struct()

        
        

        if ball_prediction is not None:
            for i in range(0,ball_prediction.num_slices):
                prediction_slice=ball_prediction.slices[i]
                predicted_location=prediction_slice.physics.location
                draw_prediction(self.renderer,packet.game_ball,predicted_location)

        # Find the direction of our car using the Orientation class
        car_orientation = Orientation(my_car.physics.rotation)
        car_direction = car_orientation.forward

        steer_correction_radians = find_correction(car_direction, car_to_ball)

        if steer_correction_radians > 0:
            # Positive radians in the unit circle is a turn to the left.
            turn = -1.0  # Negative value for a turn to the left.
            action_display = "turn left"
        else:
            turn = 1.0
            action_display = "turn right"

        self.controller_state.throttle = 1.0
        self.controller_state.steer = turn

       
        #Checks distance to the ball and boost the car       
        dist_to_ball=car_to_ball.length()
        if dist_to_ball <= self.MIN_DIST:
            self.controller_state.boost=True        

        if ball_location.z > 0:
            self.controller_state.jump=True

        draw_debug(self.renderer, my_car, packet.game_ball, action_display)
        draw_debug_goal(self.renderer,my_car,goal_to_score)

        return self.controller_state


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

import numpy as np
import os
PATH_TO_STORE="C:/dev/UC3M_RLbot/UC3M_Rlbot/src/"

class QTable:
    def __init__(self):
        self.actions=list()
        self.states=list()
    def addAction(self,controllerState):
        action={'throttle':controllerState.throttle,\
            'steer':controllerState.steer,\
            'pitch':controllerState.pitch,\
            'yaw':controllerState.yaw,\
            'roll':controllerState.roll,\
            'jump':controllerState.jump,\
            'boost':controllerState.boost,\
            'handbrake':controllerState.handbrake}
        self.actions.append(action)
    def addState(self,packet):
        state={'car_location':tuple([packet.game_cars[0].physics.location.x,packet.game_cars[0].physics.location.y,packet.game_cars[0].physics.location.z]),\
            'car_velocity':tuple([packet.game_cars[0].physics.velocity.x,packet.game_cars[0].physics.velocity.y,packet.game_cars[0].physics.velocity.z]),\
            'ball_location':tuple([packet.game_ball.physics.location.x,packet.game_ball.physics.location.y,packet.game_ball.physics.location.z]),\
            'latest_hit':tuple([packet.game_ball.latest_touch.hit_location.x,packet.game_ball.latest_touch.hit_location.y,packet.game_ball.latest_touch.hit_location.z]),\
            'game_time_remaining':packet.game_info.game_time_remaining,\
            'seconds_elapsed':packet.game_info.seconds_elapsed}
        self.states.append(state)
    def save(self):
        npActions=np.asarray(self.actions)
        npStates=np.asarray(self.states)
        print('saving actions...'+str(npActions))
        print('saving states...'+str(npActions))
        np.save("C:/dev/UC3M_RLbot/UC3M_Rlbot/src/actions.npy",npActions,allow_pickle=True)
        np.save("C:/dev/UC3M_RLbot/UC3M_Rlbot/src/states.npy",npStates,allow_pickle=True)

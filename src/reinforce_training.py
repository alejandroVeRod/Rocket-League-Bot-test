import numpy as np

class RTrain():
    action_cent=np.load("C:/dev/UC3M_RLbot/UC3M_Rlbot/src/action_cents.npy")
    state_cent=np.load("C:/dev/UC3M_RLbot/UC3M_Rlbot/src/state_cents.npy")
    qtable=np.load("C:/dev/UC3M_RLbot/UC3M_Rlbot/src/qtable.npy")
    episodes=[]
    game_frames=[]
    learning_rate=0.4
    discount_factor=0.6

    stat_closed_ball=0
    stat_closed_goal=0
    stat_boosted_up=0
    
    def __init__(self):
        print("Loaded Qtable ",self.qtable)
        print("Loaded ",len(self.state_cent)," states centroids")
        print("Loaded ",len(self.action_cent)," actions centroids")
        print(np.all(self.qtable==0))

        pass
    def save_stats(self,packet):
        print("Saving bot stats...")
        array=np.array([self.stat_closed_ball,self.stat_closed_goal,self.stat_boosted_up,packet.teams[0].score,packet.teams[1].score])
        np.save("C:/dev/UC3M_RLbot/UC3M_Rlbot/src/stats.npy",array,allow_pickle=True)
        
    def closer_centroid(self,origin,centroids):
        distances=[]
        for i in range(0,len(centroids)):
            distances.append(np.linalg.norm(origin-centroids[i]))
        return distances.index(min(distances))
    def getAction(self,packet):
        actualState=self.build_state(packet)
        stateCloserCentroid=self.closer_centroid(actualState,self.state_cent)
        actionCentroid=np.argmax(self.qtable[stateCloserCentroid][:])
        
        return self.action_cent[actionCentroid]
    def convertToNP(self,location):
        npArray=np.zeros((3))
        npArray[0]=location.x
        npArray[1]=location.y
        npArray[2]=location.z
        return npArray
    def getAngle(self,u,v):
        c = np.dot(u,v)/np.linalg.norm(u)/np.linalg.norm(v) # -> cosine of the angle
        angle = np.arccos(np.clip(c, -1, 1)) # if you really want the angle
        return angle
    def saveFrame(self,packet,controller_state):
        game_frame=[packet,controller_state]
        self.game_frames.append(game_frame)
    def build_episodes(self):
        for frame in range(0,len(self.game_frames)-1):

            if(frame!=len(self.game_frames)):

                episode=tuple([self.game_frames[frame][0],self.game_frames[frame][1],self.game_frames[frame+1][0]])
                self.episodes.append(episode)
    def calculate_reward(self,episode):
        goal=np.asarray([0,5220,320])
        ball_position=np.asarray([episode[0].game_ball.physics.location.x,episode[0].game_ball.physics.location.y,episode[0].game_ball.physics.location.z])
        car_position=np.asarray([episode[0].game_cars[0].physics.location.x,episode[0].game_cars[0].physics.location.y,episode[0].game_cars[0].physics.location.z])
        boost_level = episode[0].game_cars[0].boost
        distance_to_goal=np.linalg.norm(goal-ball_position)
        distance_to_ball=np.linalg.norm(ball_position-car_position)
        reward=0
        reward+=13113/distance_to_ball 
        reward+=13113/distance_to_goal
        if(distance_to_ball<500):
            #reward=reward*1.2
            self.stat_closed_ball+=1
        if(distance_to_goal<500):
            reward=reward*1.2
            self.stat_closed_goal+=1
        if boost_level < 45.0:
            reward = reward*0.9
        if boost_level >= 45.0:
            reward +=5
            self.stat_boosted_up+=1
        return reward
    
    def update_qTable(self):
        print("Updating Q values...")
        print(self.qtable)
        for episode in self.episodes:
            actual_state=self.build_state(episode[0])
            actual_action=self.build_action(episode[1])
            next_state=self.build_state(episode[2])

            i=self.closer_centroid(actual_state,self.state_cent)
            j=self.closer_centroid(actual_action,self.action_cent)
            i_1=self.closer_centroid(next_state,self.state_cent)
            q_value=self.qtable[i][j]
            new_reward=self.calculate_reward(episode)
            '''Q′(st,at)=(1−ν)Q(st,at)+ν[r(st,at)+γmaxat+1Q(st+1,at+1)]'''
            #print("Previous Q Value",q_value)
            new_q_value=(1-self.learning_rate)*q_value+self.learning_rate*np.abs(new_reward+self.discount_factor*np.argmax(self.qtable[i_1][:]))
            #print("New Q Value",new_q_value)

            self.qtable[i][j]=new_q_value
        np.save("C:/dev/UC3M_RLbot/UC3M_Rlbot/src/qtable.npy",self.qtable,allow_pickle=True)




        

    def updateQTable(self,packet,controller_state):
        car_location=self.convertToNP(packet.game_cars[0].physics.location)
        ball_location=self.convertToNP(packet.game_ball.physics.location)
        last_hit_location=self.convertToNP(packet.game_ball.latest_touch.hit_location)
        car_direction=self.convertToNP(packet.game_cars[0].physics.velocity)
        car_to_ball=ball_location-car_location
        bot_yaw = abs(controller_state.yaw) % 65536 / 65536 * 360
        angle_front_to_ball=np.degrees(np.arctan2(car_location[1]-ball_location[1],car_location[0]-ball_location[0]))-bot_yaw
        print(angle_front_to_ball)
        actual_state=self.build_state(packet)
        actual_action=self.build_action(controller_state)
        
        index_action=self.closer_centroid(actual_action,self.action_cent)
        index_state=self.closer_centroid(actual_state,self.state_cent)
        distance_to_ball=np.linalg.norm((ball_location-car_location))
        distance_to_last_hit=np.linalg.norm((last_hit_location-car_location))
        if(distance_to_ball<300.0):
            print("Bot is near the ball...")
            self.update_reward(index_state,index_action,10000/distance_to_ball)
        #if((angle_front_to_ball<-120 and angle_front_to_ball>-90) or (angle_front_to_ball<120 and angle_front_to_ball>90)):
        #    print("Bot is facing the ball...")
        #    self.update_reward(index_state,index_action,2)
#
        #    print("Updating QTable...")
        if(distance_to_last_hit<300):
            print("Bot is near to touch...")
            self.update_reward(index_state,index_action,10000/distance_to_ball)

            print("Updating QTable...")
       # if(packet.teams[0].score>0):
       #     actual_reward=self.qtable[index_state,index_action]
       #     new_reward=actual_reward+100
       #     self.qtable[index_state,index_action]=new_reward
       # if(packet.game_cars[0].boost<45.0):
       #     actual_reward=self.qtable[index_state,index_action]
       #     new_reward=(actual_reward-1)*0.9
       #     self.qtable[index_state,index_action]=new_reward
       # if(packet.game_cars[0].boost>=45.0):
       #     print("Bot got the boost...")
       #     actual_reward=self.qtable[index_state,index_action]
       #     new_reward=(actual_reward+1)*1.1
       #     self.qtable[index_state,index_action]=new_reward
        if(packet.game_ball.latest_touch.player_index==0):
            print("Bot hit the ball!!!")
            self.update_reward(index_state,index_action,10)
            print("Updating QTable...")
    
    def update_reward(self,index_state,index_action,reward):
        actual_reward=self.qtable[index_state,index_action]
        next_max_reward=np.argmax(self.qtable[index_state][:])
        print("Centroid: ",index_state,index_action," Actual Reward: ",actual_reward)
        new_reward=actual_reward+(self.learning_rate*(reward+self.discount_factor*next_max_reward))
        print("Centroid: ",index_state,index_action," New Reward: ",new_reward)

        self.qtable[index_state,index_action]=new_reward

    def build_action(self,controller_state):
        actualAction=np.zeros((8))
        actualAction[0]=controller_state.throttle
        actualAction[1]=controller_state.steer
        actualAction[2]=controller_state.pitch
        actualAction[3]=controller_state.yaw

        actualAction[4]=controller_state.jump
        actualAction[5]=controller_state.boost
        actualAction[6]=controller_state.handbrake

        actualAction[7]=controller_state.roll
        return actualAction



        
    def build_state(self,packet):
        actualState=np.zeros((36))
        actualState[0]=packet.game_info.seconds_elapsed
        actualState[1]=packet.game_info.game_time_remaining
        actualState[2]=packet.game_ball.physics.location.x     
        actualState[3]=packet.game_ball.physics.location.y
        actualState[4]=packet.game_ball.physics.location.z
        
        actualState[5]=packet.game_ball.physics.rotation.pitch
        actualState[6]=packet.game_ball.physics.rotation.yaw
        actualState[7]=packet.game_ball.physics.rotation.roll

        actualState[8]=packet.game_ball.physics.velocity.x
        actualState[9]=packet.game_ball.physics.velocity.y
        actualState[10]=packet.game_ball.physics.velocity.z

        actualState[11]=packet.game_cars[0].physics.location.x
        actualState[12]=packet.game_cars[0].physics.location.y
        actualState[13]=packet.game_cars[0].physics.location.z
        actualState[14]=packet.game_cars[0].physics.rotation.pitch
        actualState[15]=packet.game_cars[0].physics.rotation.yaw
        actualState[16]=packet.game_cars[0].physics.rotation.roll
        actualState[17]=packet.game_cars[0].physics.velocity.x
        actualState[18]=packet.game_cars[0].physics.velocity.y
        actualState[19]=packet.game_cars[0].physics.velocity.z

        actualState[20]=packet.game_cars[0].boost
        actualState[21]=packet.game_cars[0].physics.angular_velocity.x
        actualState[22]=packet.game_cars[0].physics.angular_velocity.y
        actualState[23]=packet.game_cars[0].physics.angular_velocity.z

        actualState[24]=packet.game_cars[1].physics.location.x
        actualState[25]=packet.game_cars[1].physics.location.y
        actualState[26]=packet.game_cars[1].physics.location.z
        actualState[27]=packet.game_cars[1].physics.rotation.pitch
        actualState[28]=packet.game_cars[1].physics.rotation.yaw
        actualState[29]=packet.game_cars[1].physics.rotation.roll
        actualState[30]=packet.game_cars[1].physics.velocity.x
        actualState[31]=packet.game_cars[1].physics.velocity.y
        actualState[32]=packet.game_cars[1].physics.velocity.z
        actualState[33]=packet.game_cars[1].physics.angular_velocity.x
        actualState[34]=packet.game_cars[1].physics.angular_velocity.y
        actualState[35]=packet.game_cars[1].physics.angular_velocity.z



        return actualState






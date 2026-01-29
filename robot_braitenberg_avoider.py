################################################################################
# File Name                      : robot_braitenberg_avoider.py
# UE                             : LU3IN025 - IA & Jeux - TME01
# Writers                        : BENNOUNA Kamil - 21204602
#                                : KHENNOUSSI Hanane - 21318242
# Creation date                  : 29/01/2026
# Last update date               : 29/01/2026 @ 1215
# Description                    : Braitenberg, obstacle-avoiding robot
################################################################################


from robot import * 

nb_robots = 0
debug = True

class Robot_player(Robot):

    team_name = "Dumb"
    robot_id = -1
    iteration = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        sensor_to_wall = []
        sensor_to_robot = []
        for i in range (0,8):
            if  sensor_view[i] == 1:
                sensor_to_wall.append( sensors[i] )
                sensor_to_robot.append(1.0)
            elif  sensor_view[i] == 2:
                sensor_to_wall.append( 1.0 )
                sensor_to_robot.append( sensors[i] )
            else:
                sensor_to_wall.append(1.0)
                sensor_to_robot.append(1.0)

        if debug == True:
            if self.iteration % 100 == 0:
                print ("Robot",self.robot_id," (team "+str(self.team_name)+")","at step",self.iteration,":")
                print ("\tsensors (distance, max is 1.0)  =",sensors)
                print ("\t\tsensors to wall  =",sensor_to_wall)
                print ("\t\tsensors to robot =",sensor_to_robot)
                print ("\ttype (0:empty, 1:wall, 2:robot) =",sensor_view)
                print ("\trobot's name (if relevant)      =",sensor_robot)
                print ("\trobot's team (if relevant)      =",sensor_team)


        ### Avoider-specific behavior (multi-sensors) ###

        # Converting sensor input to danger levels:
        d_f  = 1 - sensors[sensor_front]
        d_fl = 1 - sensors[sensor_front_left]
        d_fr = 1 - sensors[sensor_front_right]

        d_b  = 1 - sensors[sensor_rear]
        d_bl = 1 - sensors[sensor_rear_left]
        d_br = 1 - sensors[sensor_rear_right]

        d_l  = 1 - sensors[sensor_left]
        d_r  = 1 - sensors[sensor_right]

        # Determining rotation (left vs right danger):
        danger_left  = d_fl + d_l + d_bl
        danger_right = d_fr + d_r + d_br
        rotation = danger_left - danger_right

        # Determining translation (front vs rear danger):
        danger_front = d_fl + d_f + d_fr
        danger_rear  = d_bl + d_b + d_br
        translation = 0.6 + 0.4 * (danger_rear - danger_front) - 0.1

        '''
        ### Side-notes ###
            - We use the 3 sensors on a side (example: front-left, left, rear-left) to
            give a general estimation of the danger on that side
            - We subtract a small constant (0.1) to make the robot slow down and 
            come to a stop before hitting the obstacle.
        '''

        translation = max(-1.0, min(1.0, translation))
        rotation    = max(-1.0, min(1.0, rotation))

        self.iteration = self.iteration + 1        
        return translation, rotation, False

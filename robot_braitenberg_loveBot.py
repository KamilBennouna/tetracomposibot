################################################################################
# File Name                      : robot_braitenberg_loveBot.py
# UE                             : LU3IN025 - IA & Jeux - TME01
# Writers                        : BENNOUNA Kamil - 21204602
#                                : KHENNOUSSI Hanane - 21318242
# Creation date                  : 29/01/2026
# Last update date               : 29/01/2026 @ 1235
# Description                    : Braitenberg, ignores walls, loves robots (aims at them).
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


        ### LoveBot-specific behavior ###

        # Converting robot distances to attraction levels:
        r_f  = 1 - sensor_to_robot[sensor_front]
        r_fl = 1 - sensor_to_robot[sensor_front_left]
        r_fr = 1 - sensor_to_robot[sensor_front_right]

        r_b  = 1 - sensor_to_robot[sensor_rear]
        r_bl = 1 - sensor_to_robot[sensor_rear_left]
        r_br = 1 - sensor_to_robot[sensor_rear_right]

        r_l  = 1 - sensor_to_robot[sensor_left]
        r_r  = 1 - sensor_to_robot[sensor_right]

        # Determining rotation (turn toward robots):
        robot_left  = r_fl + r_l + r_bl
        robot_right = r_fr + r_r + r_br
        rotation = robot_right - robot_left

        # Determining translation (move toward robots):
        robot_front = r_fl + r_f + r_fr
        robot_rear  = r_bl + r_b + r_br
        translation = 0.4 + 0.6*(robot_front - robot_rear) - 0.05

        translation = max(-1.0, min(1.0, translation))
        rotation    = max(-1.0, min(1.0, rotation))

        self.iteration = self.iteration + 1        
        return translation, rotation, False

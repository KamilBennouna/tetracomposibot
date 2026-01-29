################################################################################
# File Name                      : robot_braitenberg_loveWall.py
# UE                             : LU3IN025 - IA & Jeux - TME01
# Writers                        : BENNOUNA Kamil - 21204602
#                                : KHENNOUSSI Hanane - 21318242
# Creation date                  : 29/01/2026
# Last update date               : 29/01/2026 @ 1220
# Description                    : Braitenberg, ignores robots, loves walls (aims at them).
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


        ### LoveWall-specific behavior ###

        # Converting wall distances to attraction levels:
        w_f  = 1 - sensor_to_wall[sensor_front]
        w_fl = 1 - sensor_to_wall[sensor_front_left]
        w_fr = 1 - sensor_to_wall[sensor_front_right]

        w_b  = 1 - sensor_to_wall[sensor_rear]
        w_bl = 1 - sensor_to_wall[sensor_rear_left]
        w_br = 1 - sensor_to_wall[sensor_rear_right]

        w_l  = 1 - sensor_to_wall[sensor_left]
        w_r  = 1 - sensor_to_wall[sensor_right]

        # Determining rotation (turn toward walls):
        wall_left  = w_fl + w_l + w_bl
        wall_right = w_fr + w_r + w_br
        rotation = wall_right - wall_left

        # Determining translation (move toward walls):
        wall_front = w_fl + w_f + w_fr
        wall_rear  = w_bl + w_b + w_br
        translation = 0.4 + 0.6*(wall_front - wall_rear) - 0.05

        translation = max(-1.0, min(1.0, translation))
        rotation    = max(-1.0, min(1.0, rotation))

        self.iteration = self.iteration + 1        
        return translation, rotation, False

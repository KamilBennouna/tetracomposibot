################################################################################
# File Name                      : robot_subsomption.py
# UE                             : LU3IN025 - IA & Jeux - TME01
# Writers                        : BENNOUNA Kamil - 21204602
#                                : KHENNOUSSI Hanane - 21318242
# Creation date                  : 29/01/2026
# Last update date               : 29/01/2026 @ 1215
# Description                    : Exercice 2, architecture de subsomption (évite les murs, poursuit les robots)
################################################################################

from robot import *

nb_robots = 0
debug = False


class Robot_player(Robot):
    team_name = "Subsomption"
    iteration = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    # Comportement 1 : aller tout droit
    def go_straight(self):
        return 0.8, 0.0

    # Comportement 2 : éviter les murs (robots ignorés)
    def hate_wall(self, sensor_to_wall):
        w_f  = 1 - sensor_to_wall[sensor_front]
        w_fl = 1 - sensor_to_wall[sensor_front_left]
        w_fr = 1 - sensor_to_wall[sensor_front_right]
        w_b  = 1 - sensor_to_wall[sensor_rear]
        w_bl = 1 - sensor_to_wall[sensor_rear_left]
        w_br = 1 - sensor_to_wall[sensor_rear_right]
        w_l  = 1 - sensor_to_wall[sensor_left]
        w_r  = 1 - sensor_to_wall[sensor_right]

        wall_left = w_fl + w_l + w_bl
        wall_right = w_fr + w_r + w_br
        rotation = wall_left - wall_right

        wall_front = w_fl + w_f + w_fr
        wall_rear = w_bl + w_b + w_br
        translation = 0.4 + 0.6 * (wall_rear - wall_front) - 0.05

        translation = max(-1.0, min(1.0, translation))
        rotation = max(-1.0, min(1.0, rotation))
        return translation, rotation

    # Comportement 3 : aller vers les robots (murs ignorés)
    def love_bot(self, sensor_to_robot):
        r_f  = 1 - sensor_to_robot[sensor_front]
        r_fl = 1 - sensor_to_robot[sensor_front_left]
        r_fr = 1 - sensor_to_robot[sensor_front_right]
        r_b  = 1 - sensor_to_robot[sensor_rear]
        r_bl = 1 - sensor_to_robot[sensor_rear_left]
        r_br = 1 - sensor_to_robot[sensor_rear_right]
        r_l  = 1 - sensor_to_robot[sensor_left]
        r_r  = 1 - sensor_to_robot[sensor_right]

        robot_left = r_fl + r_l + r_bl
        robot_right = r_fr + r_r + r_br
        rotation = robot_right - robot_left

        robot_front = r_fl + r_f + r_fr
        robot_rear = r_bl + r_b + r_br
        translation = 0.4 + 0.6 * (robot_front - robot_rear) - 0.05

        translation = max(-1.0, min(1.0, translation))
        rotation = max(-1.0, min(1.0, rotation))
        return translation, rotation

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        # Filtrage des capteurs pour ignorer murs/robots selon le comportement
        sensor_to_wall = []
        sensor_to_robot = []
        for i in range(8):
            if sensor_view[i] == 1:      # mur
                sensor_to_wall.append(sensors[i])
                sensor_to_robot.append(1.0)
            elif sensor_view[i] == 2:    # robot
                sensor_to_wall.append(1.0)
                sensor_to_robot.append(sensors[i])
            else:                        # vide
                sensor_to_wall.append(1.0)
                sensor_to_robot.append(1.0)

        # Règles d'activation (subsomption)
        wall_close = (sensor_to_wall[sensor_front] < 0.7 or
                      sensor_to_wall[sensor_front_left] < 0.7 or
                      sensor_to_wall[sensor_front_right] < 0.7)

        robot_seen = (2 in sensor_view)

        # Ordre de priorité
        if wall_close:
            translation, rotation = self.hate_wall(sensor_to_wall)
        elif robot_seen:
            translation, rotation = self.love_bot(sensor_to_robot)
        else:
            translation, rotation = self.go_straight()

        self.iteration += 1
        return translation, rotation, False


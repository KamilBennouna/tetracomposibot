# Configuration file.

import arenas
import robot_subsomption



# general -- first three parameters can be overwritten with command-line arguments (cf. "python tetracomposibot.py --help")

display_mode = 0
arena = 1
position = False 
max_iterations = 501 #401*500

# affichage

display_welcome_message = False
verbose_minimal_progress = True # display iterations
display_robot_stats = False
display_team_stats = False
display_tournament_results = False
display_time_stats = True

# initialization : create and place robots at initial positions (returns a list containing the robots)

import robot_dumb

def initialize_robots(arena_size=-1, particle_box=-1):
    y_center = arena_size // 2 - particle_box / 2
    robots = []
    robots.append(robot_subsomption.Robot_player(4, y_center, 0, name="Hunter", team="A"))
    robots.append(robot_dumb.Robot_player(80, y_center, 180, name="Target", team="B"))
    return robots


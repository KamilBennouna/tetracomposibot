################################################################################
# File Name                      : robot_randomsearch2.py
# UE                             : LU3IN025 - IA & Jeux - TME02
# Writers                        : BENNOUNA Kamil - 21204602
#                                : KHENNOUSSI Hanane - 21318242
# Creation date                  : 05/02/2026
# Last update date               : 05/02/2026 @ 1325
# Description                    : Random search with initial condition variation (3 trials)
################################################################################

from robot import *
import math

nb_robots = 0
debug = False

class Robot_player(Robot):

    team_name = "RandomSearch2"
    robot_id = -1
    iteration = 0

    param = []
    best_param = []
    it_per_evaluation = 400
    evaluations = 0
    trial = 0

    score = 0.0
    trial_score = 0.0  # Score accumulated for current behavior
    best_score = -float("inf")
    best_trial = -1

    sub_trial = 0  # Counter for 3 evaluations per behavior
    sub_evaluations = 3  # Number of evaluations per behavior

    log_translation_at_start = 0.0
    log_rotation_at_start = 0.0

    replay_mode = False
    replay_iteration = 0
    replay_length = 1000

    x_0 = 0
    y_0 = 0
    theta_0 = 0 # in [0,360]

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a", evaluations=0, it_per_evaluation=0):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots += 1
        self.x_0 = x_0
        self.y_0 = y_0
        self.theta_0 = theta_0
        self.param = [random.randint(-1, 1) for i in range(8)]
        self.best_param = list(self.param)
        self.it_per_evaluation = it_per_evaluation if it_per_evaluation > 0 else 400
        self.evaluations = evaluations if evaluations > 0 else 500
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def reset(self):
        # Randomly draw initial orientation at each reset
        random_theta = random.uniform(0, 360)
        super().reset()
        # Update robot orientation
        self.theta = random_theta

    def _reset_log_tracking(self):
        """Reinitialize log tracking for the current trial."""
        self.log_translation_at_start = self.log_sum_of_translation
        self.log_rotation_at_start = self.log_sum_of_rotation

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        # Update score during evaluation (not in replay mode)
        if not self.replay_mode and self.iteration > 0 and self.iteration % self.it_per_evaluation != 0:
            delta_translation = self.log_sum_of_translation - self.log_translation_at_start
            delta_rotation = self.log_sum_of_rotation - self.log_rotation_at_start

            if delta_translation >= 0 and delta_rotation >= 0:
                rotation_effective = min(1.0, abs(delta_rotation))
                self.trial_score += delta_translation * (1 - rotation_effective)
                self._reset_log_tracking()

        # At each evaluation end (every it_per_evaluation iterations)
        if self.iteration % self.it_per_evaluation == 0:
            # Display results if not first iteration and not in replay mode
            if self.iteration > 0 and not self.replay_mode:
                print(f"\t[Sub-trial {self.sub_trial+1}/{self.sub_evaluations}] parameters = {self.param}")
                print(f"\t[Sub-trial {self.sub_trial+1}/{self.sub_evaluations}] score = {self.trial_score}")
                print(f"\t[Sub-trial {self.sub_trial+1}/{self.sub_evaluations}] translations = {self.log_sum_of_translation}; rotations = {self.log_sum_of_rotation}")
                print(f"\t[Sub-trial {self.sub_trial+1}/{self.sub_evaluations}] distance from origin = {math.sqrt((self.x - self.x_0) ** 2 + (self.y - self.y_0) ** 2)}")
                
                self.sub_trial += 1
                
                # If 3 evaluations completed for this behavior
                if self.sub_trial >= self.sub_evaluations:
                    self.score += self.trial_score  # Add total accumulated score
                    print(f"\n\tBehavior {self.trial} completed: total score = {self.score}")
                    
                    if self.score > self.best_score:
                        self.best_score = self.score
                        self.best_param = list(self.param)
                        self.best_trial = self.trial
                        print(f"\tNew best strategy: {self.best_trial}, score = {self.best_score}")
                        print(f"\tBest parameters = {self.best_param}\n")

                    # Move to next behavior
                    self.trial += 1
                    self.sub_trial = 0
                    
                    if self.trial <= self.evaluations:
                        self.param = [random.randint(-1, 1) for i in range(8)]
                        self.score = 0.0
                        self.trial_score = 0.0
                        self._reset_log_tracking()
                        print(f"Trying strategy no. {self.trial}")
                    else:
                        # Enter replay mode
                        self.replay_mode = True
                        self.param = list(self.best_param)
                        self.replay_iteration = 0
                        self._reset_log_tracking()
                        print("Budget exhausted.")
                        print(f"Best strategy was no. {self.best_trial} with score {self.best_score}")
                        print(f"Replaying best parameters: {self.best_param}")
                else:
                    # Reset for next sub-evaluation
                    self.trial_score = 0.0
                    self._reset_log_tracking()
                    print(f"Sub-trial {self.sub_trial} starting (with new random orientation)...")

            # Replay loop: reset every replay_length iterations
            if self.replay_mode:
                self.replay_iteration = (self.replay_iteration + 1) % self.replay_length
                if self.replay_iteration == 0:
                    self._reset_log_tracking()

            self.iteration += 1
            return 0, 0, True  # ask for reset

        # Control computation (Perceptron with tanh activation)
        translation = math.tanh(
            self.param[0]
            + self.param[1] * sensors[sensor_front_left]
            + self.param[2] * sensors[sensor_front]
            + self.param[3] * sensors[sensor_front_right]
        )
        rotation = math.tanh(
            self.param[4]
            + self.param[5] * sensors[sensor_front_left]
            + self.param[6] * sensors[sensor_front]
            + self.param[7] * sensors[sensor_front_right]
        )

        if debug == True:
            if self.iteration % 100 == 0:
                print("Robot", self.robot_id, "(team " + str(self.team_name) + ")", "at step", self.iteration, ":")
                print("\tsensors (distance, max is 1.0)  =", sensors)
                print("\ttype (0:empty, 1:wall, 2:robot) =", sensor_view)
                print("\trobot's name (if relevant)      =", sensor_robot)
                print("\trobot's team (if relevant)      =", sensor_team)

        self.iteration += 1
        return translation, rotation, False

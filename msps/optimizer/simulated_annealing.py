import math
from random import random

from msps.model.solution import Solution


class SimulatedAnnealing:

    def __init__(self, instance, t_stop, t_initial, termination_condition, t_value_change):
        self.instance = instance
        self.curr_t = t_initial
        self.t_min = t_stop
        self.termination_condition = termination_condition
        self.t_value_change = t_value_change

    def simulate_annealing(self):
        solution_candidate = Solution(self.instance)
        solution_candidate_eval = solution_candidate.evaluate()
        while not self.__is_cooled_down():
            for i in range(self.termination_condition):
                new_solution_candidate = Solution(self.instance, solution_candidate)
                new_solution_candidate_eval = new_solution_candidate.evaluate()
                if new_solution_candidate_eval < solution_candidate_eval or \
                        self.__is_accepted_with_prob(solution_candidate_eval, new_solution_candidate_eval):
                    solution_candidate = new_solution_candidate
                    solution_candidate_eval = new_solution_candidate_eval

            self.__modify_t_value()
        return solution_candidate

    # HALTING_CRITERION
    def __is_cooled_down(self):
        print("curr_t: " + str(self.curr_t))
        print("t_min: " + str(self.t_min))
        print("#####################################")
        return self.curr_t <= self.t_min

    def __modify_t_value(self):
        self.curr_t *= 1-self.t_value_change

    def __is_accepted_with_prob(self, old_solution, new_solution):
        rand = random()
        return rand < math.e ** ((old_solution - new_solution) / self.curr_t)

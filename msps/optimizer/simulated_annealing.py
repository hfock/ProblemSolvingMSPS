import math
from random import random

from msps.model.solution import Solution


class SimulatedAnnealing:
    T_VALUE_CHANGE = 0.1
    TERMINATION_CONDITION = 25

    def __init__(self, instance, t_min, t_max):
        self.instance = instance
        self.curr_t = t_max
        self.t_min = t_min

    def simulate_annealing(self):
        solution_candidate = Solution(self.instance)
        solution_candidate_eval = solution_candidate.evaluate()
        for j in range(self.__is_cooled_down()):
            for i in range(self.TERMINATION_CONDITION):
                new_solution_candidate = Solution(self.instance, solution_candidate_eval)
                new_solution_candidate_eval = new_solution_candidate.evaluate()
                if new_solution_candidate_eval < solution_candidate_eval or \
                        self.__is_accepted_with_prob(solution_candidate_eval, new_solution_candidate_eval):
                    solution_candidate = new_solution_candidate
                    solution_candidate_eval = new_solution_candidate_eval

            self.__modify_t_value()

    # HALTING_CRITERION
    def __is_cooled_down(self):
        return self.curr_t <= self.t_min

    def __modify_t_value(self):
        self.curr_t *= self.T_VALUE_CHANGE

    def __is_accepted_with_prob(self, old_solution, new_solution):
        rand = random()
        return rand < math.e ** ((old_solution - new_solution) / self.curr_t)

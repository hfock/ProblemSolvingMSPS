import math
from random import random

from msps.model.solution import Solution


class SimulatedAnnealing:
    T_VALUE_CHANGE = 0.05
    TERMINATION_CONDITION = 100
    HALTING_CRITERION = 25

    def __init__(self, initial_t, instance):
        self.instance = instance
        self.t_value = initial_t

    def simulate_annealing(self):
        solution_candidate = Solution(self.instance)
        solution_candidate_eval = solution_candidate.evaluate()
        for j in range(self.HALTING_CRITERION):
            for i in range(self.TERMINATION_CONDITION):
                new_solution_candidate = Solution(self.instance, solution_candidate_eval)
                new_solution_candidate_eval = new_solution_candidate.evaluate()
                if new_solution_candidate_eval < solution_candidate_eval or \
                        self.__is_accepted_with_prob(solution_candidate_eval, new_solution_candidate_eval):
                    solution_candidate = new_solution_candidate
                    solution_candidate_eval = new_solution_candidate_eval

            self.__modify_t_value()

    def __modify_t_value(self):
        self.t_value -= self.T_VALUE_CHANGE

    def __is_accepted_with_prob(self, old_solution, new_solution):
        rand = random()
        return rand < math.e ** ((old_solution - new_solution) / self.t_value)

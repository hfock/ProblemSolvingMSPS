class Solution:

    def __init__(self, instance_definition, origin=None):
        self.instance = instance_definition
        self.schedule = {x: 0 for x in range(self.instance.nActs)}
        # use useful_res as starting point
        self.res_used_by_act = {x: self.instance.useful_res[x] for x in range(self.instance.nActs)}

        if origin is None:
            self.__generate_solution_candidate()
        else:
            self.__generate_solution_in_neighbourhood(origin)

    def evaluate(self):
        return self.schedule[self.instance.nActs - 1]

    def __generate_solution_candidate(self):

        self.check_for_hard_constraints()
        pass

    def __generate_solution_in_neighbourhood(self, origin):

        self.check_for_hard_constraints()
        pass

    def check_for_hard_constraints(self):
        return self.__check_schedule_for_precedence_relation() and \
               self.__check_res_used_by_act_for_subset_of_useful_res() and \
               self.__check_if_skill_requirement_is_met() and \
               self.__check_if_no_resource_is_overlapping()

    def __check_schedule_for_precedence_relation(self):
        return False

    def __check_res_used_by_act_for_subset_of_useful_res(self):
        for act in range(self.instance.nActs):
            if not self.res_used_by_act[act] in self.instance.useful_res[act]:
                return False
        return True

    def __check_if_skill_requirement_is_met(self):
        return False

    def __check_if_no_resource_is_overlapping(self):
        return False

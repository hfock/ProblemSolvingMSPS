class InputParam:

    def __init__(self, param_number=None, t_stop=None, t_inital=None, termination_condition=None, t_value_change=None):
        self.param_number = param_number
        self.t_stop = t_stop
        self.t_initial = t_inital
        self.termination_condition = termination_condition
        self.t_value_change = t_value_change

    def __str__(self) -> str:
        string = "{\n"
        string += "\tparam_number: " + str(self.param_number) + ",\n"
        string += "\tt_stop: " + str(self.t_stop) + ",\n"
        string += "\tt_inital: " + str(self.t_initial) + ",\n"
        string += "\ttermination_condition: " + str(self.termination_condition) + ",\n"
        string += "\tt_value_change: " + str(self.t_value_change) + ",\n"
        string += "}"

        return string

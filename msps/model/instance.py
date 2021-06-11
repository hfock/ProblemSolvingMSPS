class Instance:

    def __init__(self):
        self.mint = None
        self.maxt = None
        self.nActs = None
        self.dur = None
        self.nSkills = None
        self.sreq = None
        self.nResources = None
        self.mastery = None
        self.nPrecs = None
        self.pred = None
        self.succ = None
        self.nUnrels = None
        self.unpred = None
        self.unsucc = None
        self.useful_res = None
        self.potential_act = None
        self.predecessors_by_activity = {}

    def set_predecessors_by_activity(self):
        for act in range(self.nActs):
            predecessors = []
            for prec in range(self.nPrecs):
                if self.succ[prec] == act:
                    predecessors.append(self.pred[prec])

            self.predecessors_by_activity[act] = predecessors



    def __str__(self) -> str:
        string = "{\n"
        string += "\tmint: " + str(self.mint) + ",\n"
        string += "\tmaxt: " + str(self.maxt) + ",\n"
        string += "\tnActs: " + str(self.nActs) + ",\n"
        string += "\tdur: " + str(self.dur) + ",\n"
        string += "\tnSkills: " + str(self.nSkills) + ",\n"
        string += "\tsreq: " + str(self.sreq) + ",\n"
        string += "\tnResources: " + str(self.nResources) + ",\n"
        string += "\tmastery: " + str(self.mastery) + ",\n"
        string += "\tnPrecs: " + str(self.nPrecs) + ",\n"
        string += "\tpred: " + str(self.pred) + ",\n"
        string += "\tsucc: " + str(self.succ) + ",\n"
        string += "\tnUnrels: " + str(self.nUnrels) + ",\n"
        string += "\tunpred: " + str(self.unpred) + ",\n"
        string += "\tunsucc: " + str(self.unsucc) + ",\n"
        string += "\tuseful_res: " + str(self.useful_res) + ",\n"
        string += "\tpotential_act: " + str(self.potential_act) + "\n"
        string += "}"

        return string

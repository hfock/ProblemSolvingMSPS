from os import listdir
from os.path import isfile, join

from msps.model.instance import Instance


class InstanceFileReader:

    @staticmethod
    def read_files_in_folder(instance_file_folder):
        onlyfiles = [instance_file_folder + "/" + f
                     for f in listdir(instance_file_folder) if isfile(join(instance_file_folder, f))]

        instances = []

        for file_name in onlyfiles:
            with open(file_name, "r") as file:
                instances.append(InstanceFileReader.read_file_to_instance(file))

        return instances

    @staticmethod
    def read_file_to_instance(file):
        curr_instance = Instance()
        curr_text = ""

        for line in file.readlines():
            # ignore comments
            if line.startswith("%"):
                continue

            curr_text += " " + line
            if ";" in line:
                InstanceFileReader.__read_text_to_instance(curr_text, curr_instance)
                curr_text = ""

        curr_instance.set_predecessors_by_activity()
        return curr_instance

    @staticmethod
    def __read_text_to_instance(text, curr_instance):
        text = text.strip().lower()

        if text.startswith("mint"):
            curr_instance.mint = InstanceFileReader.__read_line_to_int(text)
        elif text.startswith("maxt"):
            curr_instance.maxt = InstanceFileReader.__read_line_to_int(text)
        elif text.startswith("nacts"):
            curr_instance.nActs = InstanceFileReader.__read_line_to_int(text)
        elif text.startswith("nskills"):
            curr_instance.nSkills = InstanceFileReader.__read_line_to_int(text)
        elif text.startswith("nresources"):
            curr_instance.nResources = InstanceFileReader.__read_line_to_int(text)
        elif text.startswith("nprecs"):
            curr_instance.nPrecs = InstanceFileReader.__read_line_to_int(text)
        elif text.startswith("nunrels"):
            curr_instance.nUnrels = InstanceFileReader.__read_line_to_int(text)
        elif text.startswith("pred"):
            curr_instance.pred = InstanceFileReader.__read_line_to_int_array(text, minus=1)
        elif text.startswith("dur"):
            curr_instance.dur = InstanceFileReader.__read_line_to_int_array(text)
        elif text.startswith("succ"):
            curr_instance.succ = InstanceFileReader.__read_line_to_int_array(text, minus=1)
        elif text.startswith("unpred"):
            curr_instance.unpred = InstanceFileReader.__read_line_to_int_array(text, minus=1)
        elif text.startswith("unsucc"):
            curr_instance.unsucc = InstanceFileReader.__read_line_to_int_array(text, minus=1)
        elif text.startswith("sreq"):
            curr_instance.sreq = InstanceFileReader.__read_line_to_2_dim_int_array(text)
        elif text.startswith("mastery"):
            curr_instance.mastery = InstanceFileReader.__read_line_to_2_dim_bool_array(text)
        elif text.startswith("useful_res"):
            curr_instance.useful_res = InstanceFileReader.__read_line_to_array_of_sets(text, minus=1)
        elif text.startswith("potential_act"):
            curr_instance.potential_act = InstanceFileReader.__read_line_to_array_of_sets(text, minus=1)

    @staticmethod
    def __read_line_to_int(text, minus=0):
        return int(InstanceFileReader.__read_value_from_line(text)) - minus

    @staticmethod
    def __read_line_to_int_array(text, minus=0):
        # get only brackets and lists
        array_line = InstanceFileReader.__read_value_from_line(text)

        # remove brackets
        array_line = array_line[1:-1]

        # making the values commas
        return [int(f) - minus for f in array_line.split(",")]

    @staticmethod
    def __read_line_to_2_dim_array(text):
        # remove unnecessary brackets
        value = InstanceFileReader.__read_value_from_line(text).strip()[2:-2].strip()
        sets_list = value.split("|")
        return [[val.strip() for val in row.strip().split(",") if val.strip() != ''] for row in sets_list]

    @staticmethod
    def __read_line_to_2_dim_int_array(text, minus=0):
        return [[int(v) - minus for v in sets] for sets in InstanceFileReader.__read_line_to_2_dim_array(text)]

    @staticmethod
    def __read_line_to_2_dim_bool_array(text):
        return [[v.lower() == 'true' for v in sets] for sets in InstanceFileReader.__read_line_to_2_dim_array(text)]

    @staticmethod
    def __read_line_to_array_of_sets(text, minus=0):
        # get rid of the outer array brackets
        sets = InstanceFileReader.__read_value_from_line(text).strip()[1:-1]
        # split into actual sets by bracket
        sets = [t.strip() for t in sets.split("{") if t.strip() != ""]
        # then remove the second bracket as well
        sets = [t[:t.index("}")] for t in sets]
        # make sets to actual python lists
        set_of_sets = [t.split(",") for t in sets]

        # necessary to handle empty sets, which should be represented by an empty list
        ret_set = []
        for curr_set in set_of_sets:
            set_build = []
            for v in curr_set:
                if v == '':
                    continue
                set_build.append(int(v) - minus)
            ret_set.append(set_build)

        return ret_set

    @staticmethod
    def __read_value_from_line(text):
        rhs = text.split("=")[1].strip()
        rhs = rhs[:rhs.index(";")]
        return rhs

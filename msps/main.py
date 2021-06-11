import time

from msps.files.instance_file_reader import InstanceFileReader
from msps.optimizer.simulated_annealing import SimulatedAnnealing

if __name__ == '__main__':
    instances = InstanceFileReader.read_files_in_folder("../instances")
    for instance in instances:
        # mint, maxt, our_t, runtime, schedule, instance file name,
        # parameter: simulated_annealing: {t_stop, t_initial, T_VALUE_CHANGE, TERMINATION_CONDITION},
        t_stop = 0.1
        t_initial = 1
        termination_condition = 500
        t_value_change = 0.05
        print(instance.filename)
        print("t_stop: "+str(t_stop))
        print("t_initial: "+str(t_initial))
        print("termination condition: "+str(termination_condition))
        print("t value change: "+str(t_value_change))

        # with open("filename", "w") as file:
        #    file.writelines("blablabla")

        starting_time = time.time()
        simulated_annealing = SimulatedAnnealing(instance, t_stop, t_initial, termination_condition, t_value_change)
        instance_solution = simulated_annealing.simulate_annealing()
        end_time = time.time()

        runtime = end_time - starting_time

        print("instance min_t: " + str(instance.mint))
        print("solution t: " + str(instance_solution.evaluate()))
        print("instance max_t: " + str(instance.maxt))
        print("runtime: " + str(runtime))
        print("schedule: " + str(instance_solution.schedule))

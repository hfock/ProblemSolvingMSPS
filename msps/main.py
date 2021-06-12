import time
import statistics

from datetime import datetime
from msps.files.instance_file_reader import InstanceFileReader
from msps.model.input_param import InputParam
from msps.model.output_solution import OutputSolution
from msps.optimizer.simulated_annealing import SimulatedAnnealing

if __name__ == '__main__':
    instances = InstanceFileReader.read_files_in_folder("../instances")
    output_filename = "solution_" + datetime.today().strftime('%d-%m-%Y_%H-%M-%S') + ".log"

    countOfIterations = 5
    inputParams = [
        InputParam(0.1, 1, 200, 0.1),
        InputParam(0.1, 1, 200, 0.05),
        InputParam(0.1, 0.5, 200, 0.05),
        InputParam(0.1, 1, 400, 0.1),
        InputParam(0.1, 1, 400, 0.05),
        InputParam(0.1, 0.5, 400, 0.05),
    ]

    for instance in instances:
        # mint, maxt, our_t, runtime, schedule, instance file name,
        # parameter: simulated_annealing: {t_stop, t_initial, T_VALUE_CHANGE, TERMINATION_CONDITION},
        with open(output_filename, "a+") as file:
            file.writelines("These are the results of the instance: " + instance.filename + "\n\n")

        for inputParam in inputParams:
            solutions = []
            with open(output_filename, "a+") as file:
                file.writelines("Parameter we used: \n"
                "\tt_stop: " + str(inputParam.t_stop) + "\n"
                "\tt_initial: " + str(inputParam.t_initial) + "\n"
                "\ttermination condition: " + str(inputParam.termination_condition) + "\n"
                "\tt value change: " + str(inputParam.t_value_change) + "\n\n")

            for i in range(countOfIterations):
                print(instance.filename)
                print(inputParam.__str__())

                starting_time = time.time()
                simulated_annealing = SimulatedAnnealing(instance,
                                                         inputParam.t_stop,
                                                         inputParam.t_initial,
                                                         inputParam.termination_condition,
                                                         inputParam.t_value_change)
                instance_solution = simulated_annealing.simulate_annealing()
                end_time = time.time()

                runtime = end_time - starting_time

                outputSolution = OutputSolution()
                outputSolution.iterationNumber = i
                outputSolution.evaluated_t = instance_solution.evaluate()
                outputSolution.runtime = runtime

                solutions.append(outputSolution)

                print("instance min_t: " + str(instance.mint))
                print("solution t: " + str(outputSolution.evaluated_t))
                print("instance max_t: " + str(instance.maxt))
                print("runtime: " + str(outputSolution.runtime))
                print("schedule: " + str(instance_solution.schedule))

                with open(output_filename, "a+") as file:
                    file.writelines("This is the run #" + str(i) + "\n\n"
                                    "Solutions we got: \n"
                                    "\tinstance min_t: " + str(instance.mint) + "\n"
                                    "\tinstance max_t: " + str(instance.maxt) + "\n"
                                    "\tour best solution t: " + str(instance_solution.evaluate()) + "\n"
                                    "\truntime: " + str(runtime) + " seconds \n"
                                    "\tschedule: " + str(instance_solution.schedule) + "\n")

            bestSolution = OutputSolution()
            solution_results_t = []
            solution_times = []

            for solution in solutions:
                solution_results_t.append(solution.evaluated_t)
                solution_times.append(solution.runtime)
                if bestSolution.evaluated_t is None:
                    bestSolution = solution
                    continue
                if (solution.evaluated_t == bestSolution.evaluated_t and solution.runtime < bestSolution.runtime) or \
                        (solution.evaluated_t < bestSolution.evaluated_t):
                    bestSolution = solution

            with open(output_filename, "a+") as file:
                file.writelines("\n\n Statistical evaluation of the file" + str(instance.filename) + "\n\n"
                                "iterations: " + str(countOfIterations) + "\n"
                                "total time seconds: " + str(sum(solution_results_t)) + "\n"
                                "total time minutes: " + str(sum(solution_results_t) / 60) + "\n"
                                "total time hours: " + str(sum(solution_results_t) / 60 / 60) + "\n"
                                "instance_min_t: " + str(instance.mint) + "\n"
                                "instance_max_t: " + str(instance.maxt) + "\n\n"
                                                                          
                                "t_best " + str(bestSolution.evaluated_t) + "\n"
                                "runtime_of_best_iteration: " + str(bestSolution.runtime) + "\n"
                                "iteration_best_solution: " + str(bestSolution.iterationNumber) + "\n\n"
                                                                                          
                                "avg_t " + str(statistics.mean(solution_results_t)) + "\n"
                                "std_t:  " + str(statistics.stdev(solution_results_t)) + "\n\n"
                                "avg_runtime " + str(statistics.mean(solution_times)) + "\n"
                                "std_runtime: " + str(statistics.stdev(solution_times)) + "\n\n"
                                "#################################################################################\n\n"
                                )


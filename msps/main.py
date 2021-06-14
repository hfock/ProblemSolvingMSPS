import time
import statistics

from datetime import datetime
from msps.files.instance_file_reader import InstanceFileReader
from msps.model.input_param import InputParam
from msps.model.output_solution import OutputSolution
from msps.optimizer.simulated_annealing import SimulatedAnnealing

if __name__ == '__main__':
    instances = InstanceFileReader.read_files_in_folder("../instances")
    output_filename = "../generated_solutions/solution_" + datetime.today().strftime('%d-%m-%Y_%H-%M-%S') + ".log"
    output_filename_csv = "../generated_solutions/solution_" + datetime.today().strftime('%d-%m-%Y_%H-%M-%S') + ".csv"

    countOfIterations = 5
    inputParams = [
        InputParam(0, 0.1, 1, 200, 0.1),
        InputParam(1, 0.1, 1, 200, 0.05),
        InputParam(2, 0.1, 0.5, 200, 0.05),
        InputParam(3, 0.1, 1, 400, 0.1),
        InputParam(4, 0.1, 1, 400, 0.05),
        InputParam(5, 0.1, 0.5, 400, 0.05),
    ]

    with open(output_filename_csv, "w") as file:
        file.writelines("filename|param_number|"
                        "t_stop|t_initial|termination_condition|t_value_change|"
                        "min_t|max_t|"
                        "evaluated_t|runtime|"
                        "avg_t|std_t|avg_runtime|std_runtime\n")

    for instance in instances:
        # mint, maxt, our_t, runtime, schedule, instance file name,
        # parameter: simulated_annealing: {t_stop, t_initial, T_VALUE_CHANGE, TERMINATION_CONDITION},
        with open(output_filename, "a+") as file:
            file.writelines("These are the results of the instance: " + instance.filename + "\n\n")

        for inputParam in inputParams:
            solutions = []
            with open(output_filename, "a+") as file:
                file.writelines("Parameter we used: \n" +
                                "\tt_stop: " + str(inputParam.t_stop) + "\n" +
                                "\tt_initial: " + str(inputParam.t_initial) + "\n" +
                                "\ttermination condition: " + str(inputParam.termination_condition) + "\n" +
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
                outputSolution.schedule = instance_solution.schedule

                solutions.append(outputSolution)

                print("instance min_t: " + str(instance.mint))
                print("solution t: " + str(outputSolution.evaluated_t))
                print("instance max_t: " + str(instance.maxt))
                print("runtime: " + str(outputSolution.runtime))
                print("schedule: " + str(instance_solution.schedule))

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

            for solution in solutions:
                with open(output_filename, "a+") as file:
                    file.writelines("This is the run #" + str(solution.iterationNumber) + "\n\n" +
                                    "Solutions we got: \n" +
                                    "\tinstance min_t: " + str(instance.mint) + "\n" +
                                    "\tinstance max_t: " + str(instance.maxt) + "\n" +
                                    "\tour best solution t: " + str(solution.evaluated_t) + "\n" +
                                    "\truntime: " + str(solution.runtime) + " seconds \n" +
                                    "\tschedule: " + str(solution.schedule) + "\n")

                csv_values = "{filename}|{param_number}|{t_stop}|{t_initial}|{termination_condition}|{t_value_change}" \
                             "|{min_t}|{max_t}|{evaluated_t}|{runtime}" \
                             "|{avg_t}|{std_t}|{avg_runtime}|{std_runtime}\n"
                csv_values = csv_values.format(filename=instance.filename, param_number=inputParam.param_number,
                                               t_stop=inputParam.t_stop, t_initial=inputParam.t_initial,
                                               termination_condition=inputParam.termination_condition,
                                               t_value_change=inputParam.t_value_change,
                                               min_t=instance.mint, max_t=instance.maxt,
                                               evaluated_t=solution.evaluated_t,
                                               runtime=solution.runtime, avg_t=statistics.mean(solution_results_t),
                                               std_t=statistics.stdev(solution_results_t),
                                               avg_runtime=statistics.mean(solution_times),
                                               std_runtime=statistics.stdev(solution_times))
                print(csv_values)

                with open(output_filename_csv, "a+") as file:
                    file.writelines(csv_values)

            with open(output_filename, "a+") as file:
                file.writelines("\n\n Statistical evaluation of the file" + str(instance.filename) + "\n\n" +
                                "iterations: " + str(countOfIterations) + "\n" +
                                "total time seconds: " + str(sum(solution_results_t)) + "\n" +
                                "total time minutes: " + str(sum(solution_results_t) / 60) + "\n" +
                                "total time hours: " + str(sum(solution_results_t) / 60 / 60) + "\n" +
                                "instance_min_t: " + str(instance.mint) + "\n" +
                                "instance_max_t: " + str(instance.maxt) + "\n\n" +

                                "t_best " + str(bestSolution.evaluated_t) + "\n" +
                                "runtime_of_best_iteration: " + str(bestSolution.runtime) + "\n" +
                                "iteration_best_solution: " + str(bestSolution.iterationNumber) + "\n\n" +

                                "avg_t " + str(statistics.mean(solution_results_t)) + "\n" +
                                "std_t:  " + str(statistics.stdev(solution_results_t)) + "\n\n" +
                                "avg_runtime " + str(statistics.mean(solution_times)) + "\n" +
                                "std_runtime: " + str(statistics.stdev(solution_times)) + "\n\n" +
                                "#################################################################################\n\n"
                                )

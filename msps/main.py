from msps.files.instance_file_reader import InstanceFileReader
from msps.model.solution import Solution

if __name__ == '__main__':
    instances = InstanceFileReader.read_files_in_folder("../instances")
    for instance in instances:
        solution = Solution(instance)
        print(solution.schedule)
        print(solution.res_used_by_act)
        break

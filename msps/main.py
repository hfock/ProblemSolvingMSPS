from msps.files.instance_file_reader import InstanceFileReader

if __name__ == '__main__':
    instances = InstanceFileReader.read_files_in_folder("../instances")
    for instance in instances:
        print(instance)

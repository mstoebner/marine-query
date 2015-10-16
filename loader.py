from os import listdir as ls

def make_big_file():
    with open("big_file.txt", "w") as big_file:
        for file in ls():
            sensor_name = file.split("_")[0]
            with open(file) as data:
                for line in data:
                    if "Time" in line:
                        continue
                    big_file.write(sensor_name + "," + ",".join(line.split()) + "\n")

make_big_file()

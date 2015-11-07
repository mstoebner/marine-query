import sys
from itertools import ifilter, imap
from os import listdir as ls
import pdb 

def line_processor(sensor_name):
    def make_line((i, (line, next_line))):
        date, temp = line.split("\t")
        return "{},{},{}".format(sensor_name, date, temp)
    return make_line 

def include_line((i, (line, next_line))):
    try:
        if "" == line.split()[0]:
            return False
    except IndexError:
        return False
    return ("Time" not in line and "" != line.split()[0] 
            and parse_date(line) == parse_date(next_line) 
            and line.strip() != "")

def include_file(file):
    return file != "big_file.txt" and two_columns(file)

def two_columns(file):
    try:
        num_cols = len(next(open(file)).split("\t"))
    except StopIteration:
        sys.stderr.write("Skipping empty file %s\n" % file)
        return False 
    if num_cols != 2:
        sys.stderr.write("Skipping %s\n" % file)
        sys.stderr.flush()
        return False 
    return True 

def make_big_file():
    with open("big_file.txt", "w") as big_file:
        for file in ls("."):
            if include_file(file):
                print("processing %s" % file)
                sensor_name = file.split("_")[0]
                lines = open(file).readlines()
                big_file.writelines(imap(line_processor(sensor_name), 
                    ifilter(include_line, enumerate(zip(lines, lines[1:])))))

def parse_date(line):
    date, _ = line.split("\t")
    return date

def has_dups(file):
    f = open(file).readlines()
    for line, next_line in zip(f, f[1:]):
        if parse_date(line) == parse_date(next_line) and line.strip() != "":
            print(file, line, next_line)

            return True
    return False

def check_for_dups():
    for file in ls("."):
        if include_file(file):
            has_dups(file)

make_big_file()

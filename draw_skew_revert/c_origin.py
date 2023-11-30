import re
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str, required=True, help="which log file to parse")
parser.add_argument("-op", "--operations", type=float, required=True, help="which log file to parse")

args=parser.parse_args()

with open(args.file, 'r') as file:
    lines = file.readlines()

zipf = 0.1
with open(args.file + '_output', 'w', encoding='utf-8') as file:
    for line in lines:
        if 'abort' in line:
            abort = float(line.split('abort: ')[1].split(' ')[0])
            commit = float(line.split('commit: ')[1].split(' ')[0])

            file.write('@ sparkle partial; zipf=' + str(zipf) + '\n')
            zipf += 0.1
            file.write(f"average operations: {abort * args.operations / commit}\n")
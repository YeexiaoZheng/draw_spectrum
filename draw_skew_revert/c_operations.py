import re
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str, required=True, help="which log file to parse")
parser.add_argument("-op", "--operations", type=float, required=True, help="which log file to parse")

args=parser.parse_args()

with open(args.file, 'r') as file:
    lines = file.readlines()

temp = []
last_thread_line = ''

with open(args.file + '_output', 'w', encoding='utf-8') as file:
    for line in lines:
        if 'zipf' in line:
            if temp:
                # 计算每种延迟的均值
                mean_op = np.mean(temp)

                file.write(last_thread_line)
                file.write(f"average operations: {mean_op}\n")
                temp = []

            last_thread_line = line
        else:
            commit = float(line.split('commit: ')[1].split(' ')[0])
            op = float(line.split('operations: ')[1].split(',')[0])
            if op > 0: temp.append(op / commit - args.operations)
    file.write(last_thread_line)
    file.write(f"average operations: {mean_op}\n")

import re
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str, required=True, help="which log file to parse")

args=parser.parse_args()

with open(args.file, 'r') as file:
    lines = file.readlines()

temp = []
last_thread_line = ''

with open(args.file + '_output', 'w', encoding='utf-8') as file:
    for line in lines:
        if 'threads' in line:
            if temp:
                latency_data = re.findall(r'Worker \d+ latency: (\d+) us \(50%\) (\d+) us \(75%\) (\d+) us \(95%\) (\d+) us \(99%\)', ''.join(temp))
                temp = []

                # 将延迟数据转换为整数
                latency_data = [[int(x) for x in latency] for latency in latency_data]

                # 计算每种延迟的均值
                mean_latency = np.mean(latency_data, axis=0)

                file.write(last_thread_line)
                file.write(f"50% 均值: {mean_latency[0]} us\n")
                file.write(f"75% 均值: {mean_latency[1]} us\n")
                file.write(f"95% 均值: {mean_latency[2]} us\n")
                file.write(f"99% 均值: {mean_latency[3]} us\n\n")
            last_thread_line = line
        else:
            temp.append(line)
    file.write(last_thread_line)
    file.write(f"50% 均值: {mean_latency[0]} us\n")
    file.write(f"75% 均值: {mean_latency[1]} us\n")
    file.write(f"95% 均值: {mean_latency[2]} us\n")
    file.write(f"99% 均值: {mean_latency[3]} us\n\n")

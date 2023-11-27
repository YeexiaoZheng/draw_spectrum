import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str, required=True, help="which log file to parse")

args=parser.parse_args()

with open(args.file, 'r') as file:
    lines = file.readlines()

filtered_lines = [line for line in lines[1:1873] if 'threads' in line or 'latency' in line]

with open(args.file, 'w') as file:
    file.writelines(filtered_lines)
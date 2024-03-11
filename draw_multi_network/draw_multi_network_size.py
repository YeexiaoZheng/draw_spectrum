##### run by cmd #####
HELP = 'python draw_multi_threads_tps.py -f afilename'
##### run by cmd #####

from typing import List, Tuple
import pandas as pd
import argparse
import sys
sys.path.extend(['.', '..'])
import matplotlib.pyplot as plt
from parse import parse_meta, parse_record, parse_records_from_file
from plot import MyPlot
from common import adaptive_y, to_fomat, add_serial

X = "cross_ratio"
Y = "multi commit network size"
# if MyPlot.language == 'chinese':
XLABEL = "跨片率（%）"
YLABEL = "平均通信量（字节）"
# else:
# XLABEL = "Threads"
# YLABEL = "Troughput(KTxn/s)"

AVG = True
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(HELP)
    parser.add_argument("-w", "--workload", type=str, required=True, help="which workload")
    parser.add_argument("-o", "--output", type=str, required=False, help="output file name")
    parser.add_argument("-v", "--value", type=float, required=False, help="serial value")

    args = parser.parse_args()
    workload = args.workload

    log_files = [
        "./calvin-{workload}-uniform".format(workload=workload),
        "./no-batch-{workload}-uniform".format(workload=workload),
        "./batch-{workload}-uniform".format(workload=workload),
    ]

    legend_labels = [
        "Calvin(读取)",
        "Prophet$_\mathit{origin}$(读取)",
        "Prophet$_\mathit{batch}$(读取)",
        "Calvin(提交)",
        "Prophet$_\mathit{origin}$(提交)",
        "Prophet$_\mathit{batch}$(提交)",
    ]

    recses = []
    colors = ['#45C686', '#ED9F54', '#8E5344' , '#B9A89B']

    for file in log_files:
        if not file:
            print("file not found")
            sys.exit(1)
        else:
            # 读取log
            print(file)
            with open(file) as f:
                content = f.read()

            # 处理日志开始的实验参数, 目前只是打印了一下
            # meta = parse_meta(content.split("@")[0].strip())

            # 处理日志并生成一个data frame
            recs = parse_records_from_file(content)
            recs = recs[recs['cross_ratio'] != 0]
            # print(recs)
            recses.append(recs)

    x, xlabel = (X, XLABEL) 
    y, ylabel = (Y, YLABEL)

    p = MyPlot(1, 1)
    ax: plt.Axes = p.axes

    ax.grid(axis=p.grid, linewidth=p.border_width)
    ax.set_axisbelow(True)
    p.init(ax)

    for idx, records in enumerate(recses):

        print(((records['network size'] - records[y]) * (32 + 32 + 8 + 8 + 4) / records['average commit'] if AVG else (records['network size'] - records[y])) * 100)
        print((records[y] * ((8 + 8 + 8 + 4) if "no-batch" in log_files[idx] else (4 + 8 + 5 * 8 + 32)) / records['average commit'] if AVG else records[y]) * 100)
        
        max_y = 0
        ax.bar(
            [_ + (idx-1) * 0.3 for _ in range(records[x].size)], 
            ((records['network size'] - records[y]) * (32 + 32 + 8 + 8 + 4) / records['average commit'] if AVG else (records['network size'] - records[y])) * 100,
            color=colors[idx], label=legend_labels[idx],
            width=0.3,
            ec='black', ls='-', lw=1,
            # hatch=['xx', '//'][idx]
        )

        ax.bar(
            [_ + (idx-1) * 0.3 for _ in range(records[x].size)], 
            (records[y] * ((8 + 8 + 8 + 4) if "no-batch" in log_files[idx] else (4 + 8 + 5 * 8 + 32)) / records['average commit'] if AVG else records[y]) * 100,
            bottom=((records['network size'] - records[y]) * (32 + 32 + 8 + 8 + 4) / records['average commit'] if AVG else (records['network size'] - records[y])) * 100,
            color=colors[idx], label=legend_labels[idx + 3],
            width=0.3,
            ec='black', ls='-', lw=1,
            hatch='//'
        )

    ax.set_xlabel(xlabel, p.label_config_dic)
    ax.set_ylabel(ylabel, p.label_config_dic)
    tmp_max =  records[y].max() 
    if tmp_max > max_y: max_y = tmp_max

    ax.set_xticks(range(4), [1, 5, 10, 30])

    # uniform
    # ax.set_ylim(0, 540000)
    max_y = 5400
    step = 1000

    ax.set_yticks(
        range(0, max_y, step), 
        [str(x)[:-3] + 'K' if len(str(x)) >3 else str(x) for x in range(0, max_y, step)]
    )

    p.legend(ax, loc="upper center", ncol=3, anchor=(0.5, 1.20), kwargs={ 'size': 10 })
    p.save('./multi-network-{workload}-size.pdf'.format(workload=workload))
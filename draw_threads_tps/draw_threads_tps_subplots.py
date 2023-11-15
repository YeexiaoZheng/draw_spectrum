##### run by cmd #####
HELP = 'python draw_threads_tps_subplots.py -f1 afilename -f2 afilename -f3 afilename'
##### run by cmd #####

X = "threads"
XLABEL = "Threads"
Y = "average commit"
YLABEL = "Troughput(K tx/s)"

from typing import List, Tuple
import pandas as pd
import argparse
import sys
import os
sys.path.extend(['.', '..', '../../'])
import matplotlib.pyplot as plt
from parse import parse_meta, parse_record, parse_records_from_file
from plot import MyPlot
from common import adaptive_y, to_fomat, add_serial

def plot_by_protocol(
        p: MyPlot, ax: plt.Axes,
        records: pd.DataFrame, 
        x: tuple, y: tuple, 
        protocols: List[Tuple[str, Tuple[float, float, float]]], 
    ):
    x, xlabel = x
    y, ylabel = y

    max_y = 0
    for idx, (protocol, color, marker) in enumerate(protocols):
        p.plot(
            ax,
            records[records['protocol'] == protocol.lower()][x], 
            xlabel,
            records[records['protocol'] == protocol.lower()][y], 
            ylabel,
            legend_label=to_fomat(protocol),
            color=color, 
            marker=p.marker_list[-1 - idx]
        )
        tmp_max =  records[records['protocol'] == protocol.lower()][y].max() 
        if tmp_max > max_y: max_y = tmp_max

    ax.set_ylim(200, None)

    # 自适应Y轴变化
    max_y = int(max_y)
    step = adaptive_y(max_y)

    ax.set_xticks(
        range(6, 37, 6)
    )

    ax.set_yticks(
        range(0, max_y, step), 
        [str(x)[:-3] if len(str(x)) > 3 else str(x) for x in range(0, max_y, step)]
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(HELP)
    parser.add_argument("-f1", "--log_file1", type=str, required=True, help="which log file to parse")
    parser.add_argument("-f2", "--log_file2", type=str, required=True, help="which log file to parse")
    parser.add_argument("-f3", "--log_file3", type=str, required=True, help="which log file to parse")
    parser.add_argument("-o", "--output", type=str, required=False, help="output file name")
    parser.add_argument("-v", "--value", type=int, required=False, help="serial value")

    args = parser.parse_args()

    p = MyPlot(1, 3, (15, 4))
    tag = ['(a)  Uniform', '(b)  Skewed', '(c)  Synthetic']

    for idx, file in enumerate([args.log_file1, args.log_file2, args.log_file3]):
        ax: plt.Axes = p.axes[idx]

        # 读取log
        with open(file) as f:
            content = f.read()

        # 处理日志开始的实验参数, 目前只是打印了一下
        meta = parse_meta(content.split("@")[0].strip())

        # 处理日志并生成一个data frame
        recs = parse_records_from_file(content)
        
        recs = recs[recs['threads'] <= 36].reset_index(drop=True)
        add_serial(recs, 'threads', value=args.value if args.value else None)

        print(idx, recs)

        plot_by_protocol(
            p, ax,
            recs, 
            (X, XLABEL + "\n" + tag[idx]), (Y, YLABEL if idx == 0 else ""), 
            [
                # 里面是 (协议名称, 颜色(RGB格式)的元组)
                # ('sparkle original' , 'tab:blue'),
                # ('sparkle partial'  , 'orange'),
                # ('aria fb'          , 'green'),
                # ('Sparkle Original' , 'blue'),
                # ('Sparkle Partial'  , 'r'),
                # ('Aria FB'          , 'lime'),
                ('sparkle original' , '#ED9F54'    , None),
                ('sparkle partial'  , '#8E5344'    , None),
                ('aria fb'          , '#45C686'    , None),
                ('serial'           , '#B9A89B'    , None),
            ],
        )

    p.legend(ax, anchor=(-0.75, 1.20), ncol=4)

    dir = "/".join(args.output.split("/")[:-1])
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    if args.output:
        p.save(args.output)
    else:
        p.save("subplots" + ".pdf")

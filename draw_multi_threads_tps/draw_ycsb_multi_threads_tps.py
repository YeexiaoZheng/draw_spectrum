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

X = "threads"
Y = "average commit"
# if MyPlot.language == 'chinese':
XLABEL = "工作线程数"
YLABEL = "吞吐（交易 / 秒）"
# else:
# XLABEL = "Threads"
# YLABEL = "Troughput(KTxn/s)"
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(HELP)
    # parser.add_argument("-f", "--log_file", type=str, required=True, help="which log file to parse")
    parser.add_argument("-o", "--output", type=str, required=False, help="output file name")
    parser.add_argument("-v", "--value", type=float, required=False, help="serial value")

    args = parser.parse_args()

    log_files = [
        # "./no-batch-ycsb-uniform",
        # "./batch-ycsb-uniform",
        # "./calvin-ycsb-uniform",
        "./no-batch-ycsb-skewed",
        "./batch-ycsb-skewed",
        "./calvin-ycsb-skewed",
    ]

    legend_labels = [
        "Prophet$_\mathit{origin}$",
        "Prophet$_\mathit{batch}$",
        "Calvin",
    ]

    recses = []
    colors = ['#ED9F54', '#8E5344' , '#45C686', '#B9A89B']

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
            recs = recs[recs['threads'] <= 20]
            # print(recs)
            recses.append(recs)

    x, xlabel = (X, XLABEL) 
    y, ylabel = (Y, YLABEL)

    p = MyPlot(1, 1)
    ax: plt.Axes = p.axes

    for i, records in enumerate(recses):
        print(records[y] * 2 * 0.95)

        max_y = 0
        p.plot(
            ax,
            records[x], 
            xlabel,
            records[y] * 2 * 0.95, 
            ylabel,
            legend_label=legend_labels[i],
            color=colors[i], 
            # marker=marker,
        )
        tmp_max =  records[y].max() 
        if tmp_max > max_y: max_y = tmp_max

        # # uniform
        # ax.set_ylim(0, 359000)
        # max_y = 360000
        # step = 60000

        # zipf
        # ax.set_ylim(0, 260000)
        # max_y = 260000
        # step = 50000

        # cross 5 uniform
        # ax.set_ylim(0, 360000)
        # max_y = 360000
        # step = 80000

        # cross 5 zipf
        ax.set_ylim(0, 280000)
        max_y = 280000
        step = 60000

        # ax.set_xticks(
        #     range(12, 37, 6)
        # )
        
        ax.set_yticks(
            range(0, max_y, step), 
            [str(x)[:-3] + 'K' if len(str(x)) >3 else str(x) for x in range(0, max_y, step)]
        )

        p.legend(ax, loc="upper center", ncol=3, anchor=(0.5, 1.15))
        p.save('./multi-threads-tps-ycsb-.pdf')
        # if savefig: p.save(savepath)

        
            # plot_by_protocol(
            #     recs, 
            #     (X, XLABEL), (Y, YLABEL), 
            #     [
            #         # 里面是 (协议名称, 颜色(RGB格式), 标记的元组)
            #         ('sparkle original' , '#ED9F54'    , None),
            #         ('sparkle partial'  , '#8E5344'    , None),
            #         # ('sparkle partial-v2'  , '#B8448D'    , None),
            #         ('aria fb'          , '#45C686'    , None),
            #         ('serial'           , '#B9A89B'    , None),
            #     ],
            #     savefig=True,
            #     savepath=args.output if args.output else args.log_file + ".pdf"
            # )

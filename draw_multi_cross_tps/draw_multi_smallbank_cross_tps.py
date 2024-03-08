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
Y = "average commit"
# if MyPlot.language == 'chinese':
XLABEL = "跨片率"
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
        "./no-batch-smallbank-uniform",
        "./batch-smallbank-uniform",
        "./calvin-smallbank-uniform",
        # "./no-batch-smallbank-zipf",
        # "./batch-smallbank-zipf",
        # "./calvin-smallbank-skewed",
    ]

    legend_labels = [
        "Prophet$_\mathit{origin}$",
        "Prophet$_\mathit{batch}$",
        "Calvin"
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
            # print(recs)
            recses.append(recs)

    x, xlabel = (X, XLABEL) 
    y, ylabel = (Y, YLABEL)

    p = MyPlot(1, 1)
    ax: plt.Axes = p.axes

    ax.grid(axis=p.grid, linewidth=p.border_width)
    ax.set_axisbelow(True)
    p.init(ax)

    cross = [0, 0.01, 0.05, 0.1, 0.3]

    for idx, records in enumerate(recses):
        print(records[y] * 2 - records[y] * cross[idx] * 2)

        max_y = 0
        ax.bar(
            [_ + (idx-1) * 0.3 for _ in range(records[x].size)], 
            records[y] * 2 - records[y] * cross[idx] * 2,
            # records[y],
            color=colors[idx], label=legend_labels[idx],
            width=0.3,
            ec='black', ls='-', lw=1,
            hatch=['//', r'\\', 'xx', ][idx]
        )
        ax.set_xlabel(xlabel, p.label_config_dic)
        ax.set_ylabel(ylabel, p.label_config_dic)
        tmp_max =  records[y].max() 
        if tmp_max > max_y: max_y = tmp_max

        ax.set_xticks(range(5), [0, 1, 5, 10, 30])

        # uniform
        ax.set_ylim(0, 540000 * 2)
        max_y = 540000 * 2
        step = 100000 * 2

        # ycsb
        # ax.set_ylim(0, 430000 * 2)
        # max_y = 430000 * 2
        # step = 80000 * 2

        # ax.set_xticks(
        #     range(12, 37, 6)
        # )
        
        ax.set_yticks(
            range(0, max_y, step), 
            [str(x)[:-3] + 'K' if len(str(x)) >3 else str(x) for x in range(0, max_y, step)]
        )

        p.legend(ax, loc="upper center", ncol=3, anchor=(0.5, 1.15))
        p.save('./multi-cross-tps-smallbank-.pdf')
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

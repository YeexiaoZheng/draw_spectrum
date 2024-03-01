##### run by cmd #####
HELP = 'python draw_threads_tps.py -f afilename'
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
if MyPlot.language == 'chinese':
    XLABEL = "工作线程数"
    YLABEL = "吞吐（交易 / 秒）"
else:
    XLABEL = "Threads"
    YLABEL = "Troughput(KTxn/s)"

def plot_by_protocol(
        records: pd.DataFrame, 
        x: tuple, y: tuple, 
        protocols: List[Tuple[str, Tuple[float, float, float]]], 
        figsize=None, 
        savefig: bool=None,
        savepath: str=None
        ):
    x, xlabel = x
    y, ylabel = y

    p = MyPlot(1, 1)
    ax: plt.Axes = p.axes

    max_y = 0
    for idx, (protocol, color, marker) in enumerate(protocols):
        p.plot(
            ax,
            records[records['protocol'] == protocol.lower()][x], 
            xlabel,
            records[records['protocol'] == protocol.lower()][y], 
            ylabel,
            legend_label=to_fomat(protocol, True if 'pre' in savepath else False),
            color=color, 
            marker=marker,
        )
        tmp_max =  records[records['protocol'] == protocol.lower()][y].max() 
        if tmp_max > max_y: max_y = tmp_max

    ax.set_ylim(0, None)

    # 自适应Y轴变化
    max_y = int(max_y)
    step = adaptive_y(max_y)

    ax.set_xticks(
        range(12, 37, 6)
    )
    
    ax.set_yticks(
        range(0, max_y, step), 
        [str(x)[:-3] + 'K' if len(str(x)) >3 else str(x) for x in range(0, max_y, step)] if MyPlot.language == 'chinese' \
        else [str(x)[:-3] if len(str(x)) >3 else str(x) for x in range(0, max_y, step)]
    )

    p.legend(ax, loc="upper center", ncol=2, anchor=None)
    if savefig: p.save(savepath)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(HELP)
    parser.add_argument("-f", "--log_file", type=str, required=True, help="which log file to parse")
    parser.add_argument("-o", "--output", type=str, required=False, help="output file name")
    parser.add_argument("-v", "--value", type=float, required=False, help="serial value")

    args = parser.parse_args()

    # 读取log
    with open(args.log_file) as f:
        content = f.read()

    # 处理日志开始的实验参数, 目前只是打印了一下
    meta = parse_meta(content.split("@")[0].strip())

    # 处理日志并生成一个data frame
    recs = parse_records_from_file(content)
    add_serial(recs, 'threads', value=args.value if args.value else None)

    recs = recs[recs['threads'] >= 6].reset_index(drop=True)

    # print(recs)
    # recs = recs[recs["threads"].isin([
    #     # 1, 6, 11, 16, 21, 26, 31, 36, 41, 46, 51, 56, 61, 66, 71, 76, 81, 86, 91, 96, 101, 106, 111
    #       1, 6, 11, 16, 21, 26, 31, 36, 41,     51,         66,             86,                   111
    # ])]

    plot_by_protocol(
        recs, 
        (X, XLABEL), (Y, YLABEL), 
        [
            # 里面是 (协议名称, 颜色(RGB格式), 标记的元组)
            ('sparkle original' , '#ED9F54'    , None),
            ('sparkle partial'  , '#8E5344'    , None),
            ('sparkle partial-v2'  , '#B8448D'    , 'p'),
            ('aria fb'          , '#45C686'    , None),
            # ('serial'           , '#B9A89B'    , None),
        ] if 'pre' in args.log_file else 
        [
            # 里面是 (协议名称, 颜色(RGB格式), 标记的元组)
            ('sparkle original' , '#ED9F54'    , None),
            ('sparkle partial'  , '#8E5344'    , None),
            # ('sparkle partial-v2'  , '#B8448D'    , None),
            ('aria fb'          , '#45C686'    , None),
            ('serial'           , '#B9A89B'    , None),
        ],
        savefig=True,
        savepath=args.output if args.output else args.log_file + ".pdf"
    )

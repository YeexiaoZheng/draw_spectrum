##### run by cmd #####
HELP = 'python draw_skew_tps.py -f afilename'
##### run by cmd #####

X = "zipf"
XLABEL = "Skew"
Y = "average commit"
YLABEL = "Troughput(K tx/s)"

from typing import List, Tuple
import pandas as pd
import argparse
import sys
sys.path.extend(['.', '..'])
import matplotlib.pyplot as plt
from parse import parse_meta, parse_record, parse_records_from_file
from plot import MyPlot
from common import adaptive_y, to_fomat, add_serial

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
    for protocol, color, marker in protocols:
        p.plot(
            ax,
            records[records['protocol'] == protocol][x], 
            xlabel,
            records[records['protocol'] == protocol][y], 
            ylabel,
            legend_label=to_fomat(protocol).replace(" ", "\n"),
            color=color, 
            marker=marker
        )
        tmp_max =  records[records['protocol'] == protocol][y].max() 
        if tmp_max > max_y: max_y = tmp_max

    ax.set_ylim(0, None)

    # 自适应Y轴变化
    max_y = int(max_y)
    step = adaptive_y(max_y)

    ax.set_yticks(
        range(0, max_y, step), 
        [str(x)[:-3] if len(str(x)) > 4 else str(x) for x in range(0, max_y, step)]
    )

    p.legend(ax, anchor=(0.5, 1.16), ncol=3)
    if savefig: p.save(savepath)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(HELP)
    parser.add_argument("-f", "--log_file", type=str, required=True, help="which log file to parse")
    
    args = parser.parse_args()

    # 读取log
    with open(args.log_file) as f:
        content = f.read()

    # 处理日志开始的实验参数, 目前只是打印了一下
    meta = parse_meta(content.split("@")[0].strip())

    # 处理日志并生成一个data frame
    recs = parse_records_from_file(content)
    add_serial(recs, 'zipf')

    plot_by_protocol(
        recs, 
        (X, XLABEL), (Y, YLABEL), 
        [
            # 里面是 (协议名称, 颜色(RGB格式), 标记的元组)
            ('sparkle partial'  , '#8E5344'    , None),
            ('sparkle original' , '#ED9F54'    , None),
            # ('sparkle partial-sched'  , '#45C686'    , None),
            # ('aria fb'          , '#45C686'    , None),
            ('serial'           , '#B9A89B'    , None),
        ],
        savefig=True,
        savepath=args.log_file + ".png"
    )

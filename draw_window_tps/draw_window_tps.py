##### run by cmd #####
HELP = 'python draw_window_tps.py -f afilename'
##### run by cmd #####

X = "window size"
XLABEL = "Window Size"
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
from common import adaptive_y, to_fomat

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
    for protocol, color in protocols:
        p.plot(
            ax,
            [str(_) for _ in records[records['protocol'] == protocol][x]], 
            # records[records['protocol'] == protocol][x],
            xlabel,
            records[records['protocol'] == protocol][y], 
            ylabel,
            legend_label=to_fomat(protocol),
            color=color, 
        )
        tmp_max =  records[records['protocol'] == protocol][y].max() 
        if tmp_max > max_y: max_y = tmp_max

    # ax.set_ylim(0, None)

    # 自适应Y轴变化
    max_y = int(max_y)
    step = adaptive_y(max_y)

    ax.set_yticks(
        range(20000, max_y, step), 
        [str(x)[:-3] if len(str(x)) > 4 else str(x) for x in range(20000, max_y, step)]
    )

    p.legend(ax, loc="upper center", ncol=len(protocols), anchor=(0.5, 1.17))
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

    print(recs)

    plot_by_protocol(
        recs, 
        (X, XLABEL), (Y, YLABEL), 
        [
            # 里面是 (协议名称, 颜色(RGB格式)的元组)
            ('sparkle partial'  , 'red'),
        ],
        savefig=True,
        savepath=args.log_file + ".png"
    )

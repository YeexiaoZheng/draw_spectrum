##### run by cmd #####
HELP = 'python draw_skew_abortrate.py -f afilename'
##### run by cmd #####

X = "zipf"
XLABEL = "Skew"
Y = "average abort"
YLABEL = "Abort rate"

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
    for idx, (protocol, color, marker) in enumerate(protocols):
        p.plot(
            ax,
            records[records['protocol'] == protocol.lower()][x], 
            xlabel,
            records[records['protocol'] == protocol][y].reset_index(drop=True).div(records[records['protocol'] == protocol]['average commit'].reset_index(drop=True)), 
            ylabel,
            legend_label=to_fomat(protocol).replace(" ", "\n"),
            color=color, 
            marker=marker
        )
        tmp_max =  records[records['protocol'] == protocol.lower()][y].max() 
        if tmp_max > max_y: max_y = tmp_max

    # ax.set_yticks([0, 3, 6, 9], [0, 3, 6, 9])

    p.legend(ax, loc="upper center", ncol=len(protocols), anchor=None)
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

    plot_by_protocol(
        recs, 
        (X, XLABEL), (Y, YLABEL), 
        [
            # 里面是 (协议名称, 颜色(RGB格式), 标记的元组)
            ('sparkle partial'  , '#8E5344'    , 'o'),
            ('aria fb'          , '#45C686'    , 'v'),
            ('sparkle original' , '#ED9F54'    , 's'),
            
        ],
        savefig=True,
        savepath=args.log_file.strip('.').strip('\\') + ".png"
    )

##### run by cmd #####
HELP = 'python draw_skew_revert.py -f afilename'
##### run by cmd #####

X = "zipf"
XLABEL = "Skew"
Y = "revert length"
YLABEL = "Revert length"

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
    y_, ylabel_ = 'original revert length', 'Expected Revert Length'

    p = MyPlot(1, 1)
    ax: plt.Axes = p.axes

    ax2 = ax.twinx()

    max_y = 0
    for idx, (protocol, color) in enumerate(protocols):
        if idx == 0:
            ax.bar(
                [_ + (idx-0.5) * 0.4 for _ in range(records[records['protocol'] == protocol][x].size)], 
                # records[records['protocol'] == protocol][y_].reset_index(drop=True).div(records[records['protocol'] == protocol]['average commit'].reset_index(drop=True)), 
                records[records['protocol'] == protocol][y_],
                color=color, label=ylabel_,
                width=0.4
            )
            continue

        ax.bar(
            [_ + (idx-0.5) * 0.4 for _ in range(records[records['protocol'] == protocol][x].size)], 
            # records[records['protocol'] == protocol][y].reset_index(drop=True).div(records[records['protocol'] == protocol]['average commit'].reset_index(drop=True)), 
            records[records['protocol'] == protocol][y],
            color=color, label="Partial Revert Length",
            width=0.4
        )
        tmp_max =  records[records['protocol'] == protocol][y].max() 
        if tmp_max > max_y: max_y = tmp_max

    p.plot(
        ax2,
        range(records[records['protocol'] == protocols[0][0]][x].size),
        "",
        records[records['protocol'] == protocols[0][0]][y].reset_index(drop=True).div(records[records['protocol'] == protocols[1][0]][y_].reset_index(drop=True)),
        # records[records['protocol'] == protocols[0][0]][y].reset_index(drop=True).div(records[records['protocol'] == protocols[0][0]]['average commit'].reset_index(drop=True)).reset_index(drop=True).div(records[records['protocol'] == protocols[1][0]][y_].reset_index(drop=True).div(records[records['protocol'] == protocols[1][0]]['average commit'].reset_index(drop=True)).reset_index(drop=True)),
        "",
        legend_label="Rate(Partial / Expected)",
        color="grey",
        nogrid=True
    )

    print(records[records['protocol'] == protocols[0][0]][y].reset_index(drop=True), records[records['protocol'] == protocols[1][0]][y_].reset_index(drop=True))
    print(records[records['protocol'] == protocols[0][0]][y].reset_index(drop=True).div(records[records['protocol'] == protocols[1][0]][y_].reset_index(drop=True)))

    ax.set_xlabel(xlabel, fontdict=p.label_config_dic)
    ax.set_ylabel(ylabel, fontdict=p.label_config_dic)
    ax.set_ylim(5000, None)

    # ax1.grid(axis="y", linewidth=BWIDTH)
    # ax2.grid(axis="y", linewidth=BWIDTH)

    ax.set_xticks(range(11), [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1], rotation=45)
    
    ax.tick_params(axis='y', which="minor", length=5, width=1, labelsize=10, labelcolor = "0.25")
    ax.tick_params(axis='x', which='minor', length=0, width=0)
    ax.minorticks_on()

    ax.set_yscale('log', base=10)

    p.legend(ax, anchor=(0.5, 1.16))
    p.legend(ax2, anchor=(0.5, 1.25))
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
    # recs = recs[recs['zipf'].isin([0.00, 0.12, 0.24, 0.36, 0.48, 0.60, 0.72, 0.84, 0.96])]
    # recs = recs[recs['zipf'].isin([0.00, 0.24, 0.48, 0.72, 0.96])]
    print(recs)

    plot_by_protocol(
        recs, 
        (X, XLABEL), (Y, YLABEL), 
        [
            # 里面是 (协议名称, 颜色(RGB格式)的元组)
            # ('sparkle original' , 'orange'),
            ('sparkle partial'  , 'black'),
            ('sparkle partial'  , 'red'),
        ],
        savefig=True,
        savepath=args.log_file.strip('.').strip('\\') + ".png"
    )

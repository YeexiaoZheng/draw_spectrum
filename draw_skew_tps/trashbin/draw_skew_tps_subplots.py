##### run by cmd #####
HELP = 'python draw_skew_tps_subplots.py -f1 afilename -f2 afilename'
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
            records[records['protocol'] == protocol][x], 
            xlabel,
            records[records['protocol'] == protocol][y], 
            ylabel,
            legend_label=to_fomat(protocol),
            color=color, 
            marker=p.marker_list[-1 - idx]
        )
        tmp_max =  records[records['protocol'] == protocol.lower()][y].max() 
        if tmp_max > max_y: max_y = tmp_max

    ax.set_ylim(0, None)

    # 自适应Y轴变化
    max_y = int(max_y)
    step = adaptive_y(max_y)

    ax.set_yticks(
        range(0, max_y, step), 
        [str(x)[:-3] if len(str(x)) > 3 else str(x) for x in range(0, max_y, step)]
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(HELP)
    parser.add_argument("-f1", "--log_file1", type=str, required=True, help="which log file to parse")
    parser.add_argument("-f2", "--log_file2", type=str, required=True, help="which log file to parse")

    args = parser.parse_args()

    p = MyPlot(1, 2, (10, 4))

    for idx, file in enumerate([args.log_file1, args.log_file2]):
        ax: plt.Axes = p.axes[idx]

        # 读取log
        with open(file) as f:
            content = f.read()

        # 处理日志开始的实验参数, 目前只是打印了一下
        meta = parse_meta(content.split("@")[0].strip())

        # 处理日志并生成一个data frame
        recs = parse_records_from_file(content)
        add_serial(recs, 'zipf')

        plot_by_protocol(
            p, ax,
            recs, 
            (X, XLABEL), (Y, YLABEL if idx == 0 else ""), 
            [
                # 里面是 (协议名称, 颜色(RGB格式), 标记的元组)
                ('sparkle partial'  , 'r'       , None),
                ('sparkle original' , 'blue'    , None),
                ('aria fb'          , 'lime'    , None),
                ('serial'           , 'grey'    , None),
            ],
        )

    p.legend(ax, anchor=(-0.15, 1.17), ncol=4)
    p.save("subplots" + ".pdf")

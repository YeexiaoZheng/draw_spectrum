##### run by cmd #####
HELP = 'python draw_latency_per_tx.py -f afilename'
##### run by cmd #####

X = "percentile"
XLABEL = "Percentile"
Y = "latency"
YLABEL = "Latency(us)"

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
    for idx, (protocol, color) in enumerate(protocols):
        ax.bar(
            # records[records['protocol'] == protocol][x], 
            [_ + (idx-1.5) * 0.2 for _ in range(records[records['protocol'] == protocol][x].size)], 
            records[records['protocol'] == protocol][y], 
            label=to_fomat(protocol).replace(" ", "\n"),
            color=color, 
            width=0.2,
            ec='black', ls='-', lw=1,
            hatch='xx'
        )
        tmp_max =  records[records['protocol'] == protocol][y].max() 
        if tmp_max > max_y: max_y = tmp_max

    ax.set_xlabel(xlabel, fontdict=p.label_config_dic)
    ax.set_ylabel(ylabel, fontdict=p.label_config_dic)
    # ax.set_ylim(0, None)
    ax.set_xticks(range(3), ['50%', '95%', '99%'])

    # 自适应Y轴变化
    # max_y = int(max_y)
    # step = adaptive_y(max_y)

    step=adaptive_y(int(max_y), 4)

    ax.set_yticks(
        range(0, max_y, 80), 
        [str(x)[:-3] if len(str(x)) >3 else str(x) for x in range(0, max_y, 80)]
    )

    p.legend(ax, loc="upper center", ncol=len(protocols) // 2, anchor=None)
    if savefig: p.save(savepath)

if __name__ == '__main__':
    # parser = argparse.ArgumentParser(HELP)
    # parser.add_argument("-f", "--log_file", type=str, required=True, help="which log file to parse")

    # args = parser.parse_args()

    # # 读取log
    # with open(args.log_file) as f:
    #     content = f.read()

    # # 处理日志开始的实验参数, 目前只是打印了一下
    # meta = parse_meta(content.split("@")[0].strip())

    # # 处理日志并生成一个data frame
    # recs = parse_records_from_file(content)
    recs = pd.DataFrame(columns=['protocol', 'percentile', 'latency'])

    data_uniform = {
        'Serial': [17, 19, 25, 34],
        'Sparkle Original': [48, 53, 60, 77],
        'Sparkle Partial': [30, 35, 45, 53],
        'Aria FB': [110, 115, 125, 216],
        'Aria FB Worker 0': [492, 497, 508, 752]
    }

    data_skewed = {
        'Serial': [17, 19, 25, 34],
        'Sparkle Original': [72, 120, 226, 325],
        'Sparkle Partial': [63, 102, 186, 265],
        'Aria FB': [124, 180, 234, 289],
        'Aria FB Worker 0': [492, 497, 508, 752]
    }

    data=data_uniform

    for proto in data.keys():
        for idx, perc in enumerate(['50%', '75%', '95%', '99%']):
            if idx == 1: continue
            recs.loc[len(recs.index)] = [proto, perc, data[proto][idx]]
    print(recs)

    plot_by_protocol(
        recs, 
        (X, XLABEL), (Y, YLABEL), 
        [
            # 里面是 (协议名称, 颜色(RGB格式)的元组)
            # ('sparkle original' , 'tab:blue'),
            # ('sparkle partial'  , 'orange'),
            # ('aria fb'          , 'green'),
            ('Serial'           , '#B9A89B'),
            ('Sparkle Partial'  , '#8E5344'),
            ('Sparkle Original' , '#ED9F54'),
            ('Aria FB'          , '#45C686'),
        ],
        savefig=True,
        savepath='smallbank' + ".png"
    )

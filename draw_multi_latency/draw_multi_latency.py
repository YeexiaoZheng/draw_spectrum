##### run by cmd #####
HELP = 'python draw_latency_per_tx.py -f afilename'
##### run by cmd #####

X = "percentile"
XLABEL = "分位数"
Y = "latency"
YLABEL = "延迟（微秒）"

from typing import List, Tuple
import pandas as pd
import argparse
import sys
sys.path.extend(['.', '..'])
import matplotlib.pyplot as plt
from parse import parse_meta, parse_record, parse_records_from_file
from plot import MyPlot
from common import adaptive_y, to_fomat

parser = argparse.ArgumentParser(HELP)
# parser.add_argument("-f", "--file", type=str, required=True, help="which log file to parse")
# parser.add_argument("-t", "--threads", type=int, required=True, help="threads")

args = parser.parse_args()

legend_labels = [
    "不采用复用策略",
    "采用复用策略",
]


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

    ax.grid(axis=p.grid, linewidth=p.border_width)
    ax.set_axisbelow(True)

    max_y = 0
    for idx, (protocol, color) in enumerate(protocols):
        protocol=protocol.lower()
        # tmp = [
        #     [-0.1 + 0.2, 0.9 - 0.2],
        #     [0.1 + 0.2, 1.1 - 0.2],
        # ]
        ax.bar(
            # records[records['protocol'] == protocol][x], 
            [_ + (idx-0.5) * 0.3 for _ in range(records[records['protocol'] == protocol][x].size)], 
            records[records['protocol'] == protocol][y], 
            label=legend_labels[idx],
            color=color, 
            width=0.3,
            ec='black', ls='-', lw=1,
            hatch=['xx', '//'][1-idx]
        )
        tmp_max =  records[records['protocol'] == protocol][y].max() 
        if tmp_max > max_y: max_y = tmp_max

    ax.set_xlabel(xlabel, fontdict=p.label_config_dic)
    ax.set_ylabel(ylabel, fontdict=p.label_config_dic)
    # ax.set_ylim(-0.2, 1.2)
    # ax.set_xlim(-0.2, 1.2)
    ax.set_xticks(range(3), ['50%', '95%', '99%'])

    # 自适应Y轴变化
    max_y = int(max_y)
    step=adaptive_y(int(max_y), 4)
    # step=60

    ax.set_yticks(
        range(0, max_y, step), 
        # [str(x)[:-3] if len(str(x)) >3 else str(x) for x in range(0, max_y, step)]
    )

    p.legend(ax, loc="upper center", ncol=len(protocols), anchor=(0.5, 1.15))
    if savefig: p.save(savepath)


# with open(args.file, 'r', encoding='utf-8') as file:
#     lines = file.readlines()

# 提取数据
protocols = ['no-batch-smallbank', 'batch-smallbank', 'no-batch-ycsb', 'batch-ycsb']
mean_values = {protocol: [] for protocol in protocols}

# data = {
#     'no-batch-smallbank':[119, 160, 319],
#     'batch-smallbank': [209, 347, 204],
#     'no-batch-ycsb': [129, 160, 441],
#     'batch-ycsb': [245, 420, 333]
# }

data = {
    # 'no-batch-smallbank':[124, 210, 622],
    # 'batch-smallbank': [279, 536, 344],
    # 'no-batch-ycsb': [119, 203, 649],
    # 'batch-ycsb': [322, 593, 467],
    'batch-no-advance-smallbank': [314, 640, 654],
    'batch-advance-smallbank': [269, 444, 476],
    'batch-no-advance-ycsb': [459, 903, 1017],
    'batch-advance-ycsb': [395, 658, 722],
}

print(data)

recs = pd.DataFrame(columns=['protocol', 'percentile', 'latency'])

for proto in data.keys():
    for idx, perc in enumerate(['50%', '95%', '99%']):
        recs.loc[len(recs.index)] = [proto, perc, data[proto][idx]]

print(recs)

# '#', '#8E5344'
# '#ED9F54', '#8E5344'
plot_by_protocol(
    recs, 
    (X, XLABEL), (Y, YLABEL), 
    [
        # 里面是 (协议名称, 颜色(RGB格式)的元组)
        ('batch-no-advance-ycsb'           , '#ED9F54'),
        ('batch-advance-ycsb'  , '#8E5344'),
        # ('Sparkle Original' , '#ED9F54'),
        # ('Aria FB'          , '#45C686'),
    ],
    savefig=True,
    savepath="ycsb" + ".pdf"
)
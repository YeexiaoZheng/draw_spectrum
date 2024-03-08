##### run by cmd #####
HELP = 'python draw_latency_per_tx.py -f afilename'
##### run by cmd #####

X = "percentile"
XLABEL = "节点数"
Y = "latency"
YLABEL = "吞吐（交易 / 秒）"

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
    "Prophet$_\mathit{origin}$",
    "Prophet$_\mathit{batch}$",
    "Calvin",
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
            [_ + (idx-1) * 0.3 for _ in range(records[records['protocol'] == protocol][x].size)], 
            records[records['protocol'] == protocol][y], 
            label=legend_labels[idx],
            color=color, 
            width=0.3,
            ec='black', ls='-', lw=1,
            hatch=['//', r'\\', 'xx'][idx]
        )
        tmp_max =  records[records['protocol'] == protocol][y].max() 
        if tmp_max > max_y: max_y = tmp_max

    ax.set_xlabel(xlabel, fontdict=p.label_config_dic)
    ax.set_ylabel(ylabel, fontdict=p.label_config_dic)
    # ax.set_ylim(-0.2, 1.2)
    # ax.set_xlim(-0.2, 1.2)
    ax.set_xticks(range(3), ['2P', '4P', '8P'])

    # 自适应Y轴变化
    max_y = int(max_y)
    step=int(adaptive_y(int(max_y), 4)) // 65000 * 65000
    # step=60

    ax.set_yticks(
        range(0, max_y, step), 
        [str(x)[:-3] + 'K' if len(str(x)) >3 else str(x) for x in range(0, max_y, step)]
    )

    p.legend(ax, loc="upper center", ncol=len(protocols), anchor=(0.5, 1.15))
    if savefig: p.save(savepath)


# with open(args.file, 'r', encoding='utf-8') as file:
#     lines = file.readlines()

# 提取数据
# protocols = ['no-batch-smallbank', 'batch-smallbank', 'no-batch-ycsb', 'batch-ycsb']
# mean_values = {protocol: [] for protocol in protocols}

# data = {
#     'no-batch-smallbank':   [194220,	220590,	276363],
#     'batch-smallbank':      [288133,	459277,	538746],
#     'calvin-smallbank':     [128445,	100706,	91957],
# }

data = {
    'no-batch-ycsb': [90099,	101326,	129336],
    'batch-ycsb': [129777,	239767,	275238],
    'calvin-ycsb': [66731,	61286,	45271],
}

print(data)

recs = pd.DataFrame(columns=['protocol', 'percentile', 'latency'])

for proto in data.keys():
    for idx, perc in enumerate(['2P', '4P', '8P']):
        recs.loc[len(recs.index)] = [proto, perc, data[proto][idx]]

print(recs)

# '#', '#8E5344'

colors = ['#ED9F54', '#8E5344' , '#45C686', '#B9A89B']

plot_by_protocol(
    recs, 
    (X, XLABEL), (Y, YLABEL), 
    [
        # 里面是 (协议名称, 颜色(RGB格式)的元组)
        # ('no-batch-smallbank'   , colors[0]),
        # ('batch-smallbank'      , colors[1]),
        # ('calvin-smallbank'     , colors[2]),
        ('no-batch-ycsb'        , colors[0]),
        ('batch-ycsb'           , colors[1]),
        ('calvin-ycsb'          , colors[2]),
        # ('Sparkle Original' , '#ED9F54'),
        # ('Aria FB'          , '#45C686'),
    ],
    savefig=True,
    savepath="ycsb" + ".pdf"
)
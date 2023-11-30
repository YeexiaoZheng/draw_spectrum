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

parser = argparse.ArgumentParser(HELP)
parser.add_argument("-f", "--file", type=str, required=True, help="which log file to parse")
parser.add_argument("-t", "--threads", type=int, required=True, help="threads")

args = parser.parse_args()


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
        ax.bar(
            # records[records['protocol'] == protocol][x], 
            [_ + (idx-1.5) * 0.2 for _ in range(records[records['protocol'] == protocol][x].size)], 
            records[records['protocol'] == protocol][y], 
            label=to_fomat(protocol).replace(" ", "\n"),
            color=color, 
            width=0.2,
            ec='black', ls='-', lw=1,
            hatch=['--', 'xx', '//', r'\\'][idx]
        )
        tmp_max =  records[records['protocol'] == protocol][y].max() 
        if tmp_max > max_y: max_y = tmp_max

    ax.set_xlabel(xlabel, fontdict=p.label_config_dic)
    ax.set_ylabel(ylabel, fontdict=p.label_config_dic)
    # ax.set_ylim(0, None)
    ax.set_xticks(range(2), ['50%', '99%'])

    # 自适应Y轴变化
    max_y = int(max_y)
    step=adaptive_y(int(max_y), 4)
    # step=60

    ax.set_yticks(
        range(0, max_y, step), 
        [str(x)[:-3] if len(str(x)) >3 else str(x) for x in range(0, max_y, step)]
    )

    p.legend(ax, loc="upper center", ncol=len(protocols) // 2, anchor=None)
    if savefig: p.save(savepath)


with open(args.file, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# 提取数据
protocols = ['serial', 'sparkle partial', 'aria fb', 'sparkle original']
mean_values = {protocol: [] for protocol in protocols}
thread = args.threads
print(args.threads)

data = {
    'serial':[],
    'sparkle partial': [],
    'aria fb': [],
    'sparkle original': []
}

for protocol in protocols:
    flag=False
    for line in lines:
        if flag and '%' in line:
            data[protocol].append(float(line.split(' ')[-2]))
        if protocol == 'serial' and protocol in line:
            flag=True
            continue
        if f'{protocol}; threads={thread}' in line:
            flag=True
            continue
        if flag and '%' not in line:
            break

print(data)

recs = pd.DataFrame(columns=['protocol', 'percentile', 'latency'])

for proto in data.keys():
    for idx, perc in enumerate(['50%', '75%', '95%', '99%']):
        if idx == 1: continue
        if idx == 2: continue
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
    savepath=args.file + ".pdf"
)
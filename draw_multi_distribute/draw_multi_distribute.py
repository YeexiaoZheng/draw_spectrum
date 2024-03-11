##### run by cmd #####
HELP = 'python draw_latency_per_tx.py -w workload'
##### run by cmd #####

X = "partition_num"
XLABEL = "分片数"
Y = "throughput"
YLABEL = "吞吐（交易 / 秒）"

import pandas as pd
import argparse
import sys
sys.path.extend(['.', '..'])
import matplotlib.pyplot as plt
from plot import MyPlot

#################### 参数解析 ####################
parser = argparse.ArgumentParser(HELP)
parser.add_argument("-w", "--workload", type=str, required=True, help="workload: smallbank or ycsb")
args = parser.parse_args()
assert args.workload in ['smallbank', 'ycsb']
workload = args.workload

#################### 数据准备 ####################
data = {
    'smallbank': {
        'Calvin':                       [100988,	183022,	221884],
        'Prophet$_\mathit{origin}$':    [194220,	220590,	276363],
        'Prophet$_\mathit{batch}$':     [288133,	459277,	538746],
    },
    'ycsb': {
        'Calvin':                       [62840,	    103078,	113291],
        'Prophet$_\mathit{origin}$':    [90099,	    101326,	129336],
        'Prophet$_\mathit{batch}$':     [129777,	239767,	275238],
    }
}
data = data[workload]

recs = pd.DataFrame(columns=['schema', 'partition_num', 'throughput'])
for schema in data.keys():
    for idx, perc in enumerate(['2', '4', '8']):
        recs.loc[len(recs.index)] = [schema, perc, data[schema][idx]]

schemas = [
    # 里面是 (协议名称, 颜色(RGB格式)的元组)
    ('Calvin'                       , '#45C686'),
    ('Prophet$_\mathit{origin}$'    , '#ED9F54'),
    ('Prophet$_\mathit{batch}$'     , '#8E5344'),
]

#################### 画图 ####################
p = MyPlot(1, 1)
ax: plt.Axes = p.axes
ax.grid(axis=p.grid, linewidth=p.border_width)
ax.set_axisbelow(True)

for idx, (schema, color) in enumerate(schemas):
    p.bar(
        ax, 
        [_ + (idx-1) * 0.3 for _ in range(recs[recs['schema'] == schema][X].size)], 
        recs[recs['schema'] == schema][Y], 
        schema, 
        color, 
        width=0.3,
        hatch=['xx', '//', r'\\'][idx]
    )

# 设置X轴标签
ax.set_xticks(range(3), ['2', '4', '8'])

# 自适应Y轴变化
p.format_yticks(ax, suffix='K')

# 设置label
p.set_labels(ax, XLABEL, YLABEL)

# 设置图例
p.legend(ax, loc="upper center", ncol=len(schemas), anchor=(0.5, 1.15))

# 保存
p.save(workload + '.pdf')
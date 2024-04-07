##### run by cmd #####
HELP = 'python draw_threads_tps.py -w workload -c contention'
##### run by cmd #####

X = "threads"
Y = "latency"
XLABEL = "Percentile"
YLABEL = "Latency(us)"

import pandas as pd
import argparse
import sys

sys.path.extend(['.', '..', '../..'])
import matplotlib.pyplot as plt
from plot.plot import MyPlot
from Schemas import schemas

#################### 参数解析 ####################
parser = argparse.ArgumentParser(HELP)
parser.add_argument("-w", "--workload", type=str, required=True, help="workload: smallbank or ycsb")
parser.add_argument("-c", "--contention", type=str, required=True, help="contention: uniform or skewed")
parser.add_argument("-t", "--threads", type=int, required=True, help="threads")
args = parser.parse_args()
assert args.workload in ['smallbank', 'ycsb']
workload = args.workload
assert args.contention in ['uniform', 'skewed']
contention = args.contention

savepath = f'threads-tps-{workload}-{contention}.pdf'

#################### 数据准备 ####################
recs = pd.read_csv(f'./data/{workload}_{contention}.csv')
assert args.threads in recs['threads'].unique()
threads = args.threads
recs = recs[recs['threads'] == threads]
inner_schemas = recs['protocol'].unique()
print(inner_schemas)

#################### 画图 ####################
p = MyPlot(1, 1)
ax: plt.Axes = p.axes
ax.grid(axis=p.grid, linewidth=p.border_width)
p.init(ax)

percentiles = ['50%', '99%']
percentiles_label = ['latency_50', 'latency_99']

for pdx, pl in enumerate(percentiles_label):
    for idx, (schema, color) in enumerate(schemas):
        records = recs[recs['protocol'] == schema]
        print(records)
        p.bar(
            ax,
            xdata=[_ + (idx-1.5) * 0.2 for _ in range(2)],
            ydata=records[percentiles_label[pdx]],
            color=color, legend_label=schema,
            hatch=['/', '\\', '|', '-', '+', 'x'][idx % 6],
        )

# 设置X轴标签
# ax.set_xticks(percentiles)

# 自适应Y轴变化
p.format_yticks(ax)
# ax.set_ylim(None, p.max_y_data * 1.15)       # 折线图的Y轴上限设置为数据最大值的1.15倍

# 设置label
p.set_labels(ax, XLABEL, YLABEL)

# 设置图例
p.legend(ax, loc="upper center", ncol=3, anchor=(0.5, 1.25))

# 保存
p.save(savepath)
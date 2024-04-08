##### run by cmd #####
HELP = 'python draw_threads_tps.py -w workload -c contention'
##### run by cmd #####

X = "threads"
Y = "commit"
XLABEL = "Threads"
YLABEL = "Troughput(Txn/s)"

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
args = parser.parse_args()
assert args.workload in ['smallbank', 'ycsb', 'tpcc']
workload = args.workload
assert args.contention in ['uniform', 'skewed']
contention = args.contention

savepath = f'threads-tps-{workload}-{contention}.pdf'

#################### 数据准备 ####################
recs = pd.read_csv(f'./data/{workload}_{contention}.csv')
inner_schemas = recs['protocol'].unique()
print(inner_schemas)

#################### 画图 ####################
p = MyPlot(1, 1)
ax: plt.Axes = p.axes
ax.grid(axis=p.grid, linewidth=p.border_width)
p.init(ax)

for idx, (schema, color) in enumerate(schemas):
    records = recs[recs['protocol'] == schema]
    # print(records[Y])
    p.plot(
        ax,
        xdata=records[X],
        ydata=records[Y],
        color=color, legend_label=schema,
        # marker=['v', 's', 'o'][idx]
    )

print(type(recs['threads'].unique()), recs['threads'].unique())
# 设置X轴标签
ax.set_xticks([int(t) for t in recs['threads'].unique()])

# 自适应Y轴变化
p.format_yticks(ax, suffix='K', step=140000 if workload == 'smallbank' and contention == 'skewed' else None)
# ax.set_ylim(None, p.max_y_data * 1.15)       # 折线图的Y轴上限设置为数据最大值的1.15倍

# 设置label
p.set_labels(ax, XLABEL, YLABEL)

# 设置图例
p.legend(ax, loc="upper center", ncol=3, anchor=(0.5, 1.25))

# 保存
p.save(savepath)
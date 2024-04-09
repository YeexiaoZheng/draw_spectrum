##### run by cmd #####
HELP = 'python draw_skew_tps.py -w workload -c contention'
##### run by cmd #####

X = "zipf"
Y = "commit"
XLABEL = "Contention Degree (Zipf)"
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
parser.add_argument("-t", "--threads", type=int, required=True, help="threads")
args = parser.parse_args()
assert args.workload in ['smallbank', 'ycsb', 'tpcc']
workload = args.workload
if workload == 'tpcc':
    XLABEL = "Number of Items"

threads = args.threads

savepath = f'skew-tps-{workload}-{threads}.pdf'

#################### 数据准备 ####################
recs = pd.read_csv(f'./data/{workload}_{threads}.csv')
# recs = recs[recs['zipf'] >= 0.9].reset_index(drop=True)
# recs = recs[recs['zipf'] <= 1.3].reset_index(drop=True)
inner_schemas = recs['protocol'].unique()
print(inner_schemas)

schemas = [
    ('Sparkle'      ,   '#595959'),
    ('Spectrum'     ,   '#D95353'),
]

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
        marker=['s', 'o'][idx]
    )

print(type(recs['zipf'].unique()), recs['zipf'].unique())
# 设置X轴标签
# ax.set_xticks(range(len(recs['zipf'].unique())), [str(t) for t in recs['zipf'].unique()])

# 自适应Y轴变化
p.format_yticks(ax, suffix='M' if workload == 'smallbank' else 'K', step=14000 if workload == 'tpcc' else None)
# ax.set_ylim(None, p.max_y_data * 1.15)       # 折线图的Y轴上限设置为数据最大值的1.15倍

# 设置label
p.set_labels(ax, XLABEL, YLABEL)

# 设置图例
p.legend(ax, loc="upper center", ncol=3, anchor=(0.5, 1.15))

# 保存
p.save(savepath)
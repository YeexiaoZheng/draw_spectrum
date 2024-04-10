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
assert args.contention in ['uniform', 'skewed', '5orderlines', '10orderlines', '20orderlines', 'compare']
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

schemas_dict = None
if contention == 'compare':
    schemas = [
        ('SpectrumCOPYONWRITE'      ,   '#D62728'),
        ('SpectrumSTRAWMAN'         ,   '#3A5FAD'),
        ('SpectrumNoPartialBASIC'   ,   '#595959'),
    ]
    schemas_dict = {
        'SpectrumCOPYONWRITE'       :   'EVMCoW\n (Partial)',
        'SpectrumSTRAWMAN'          :   'EVMStraw\n  (Partial)',
        'SpectrumNoPartialBASIC'    :   '     EVM\n(Complete)',
    }

for idx, (schema, color) in enumerate(schemas):
    records = recs[recs['protocol'] == schema]
    # print(records[Y])
    p.plot(
        ax,
        xdata=records[X],
        ydata=records[Y],
        color=color, legend_label=schemas_dict[schema] if schemas_dict else schema,
        # marker=['v', 's', 'o'][idx]
    )

print(type(recs['threads'].unique()), recs['threads'].unique())
# 设置X轴标签
ax.set_xticks([int(t) for t in recs['threads'].unique()])

# 自适应Y轴变化
step = None
if workload == 'smallbank' and contention == 'skewed':
    step = 140000
elif workload == 'tpcc' and contention == '10orderlines':
    step = 11000
p.format_yticks(ax, suffix='K', step=step)
# ax.set_ylim(None, p.max_y_data * 1.15)       # 折线图的Y轴上限设置为数据最大值的1.15倍

# 设置label
p.set_labels(ax, XLABEL, YLABEL)
# ax.set_ylabel(YLABEL, labelpad=-10)
# box1: plt.Bbox = ax.get_window_extent()
# box2: plt.Bbox = ax.get_tightbbox()

# 设置图例
p.legend(
    ax, 
    loc="upper center", 
    ncol=3, 
    anchor=(0.5, 1.18) if contention == 'compare' else (0.5, 1.25), 
    kwargs={ 'size': 11 } if contention == 'compare' else None
)

# 保存
p.save(savepath)
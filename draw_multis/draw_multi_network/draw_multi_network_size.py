##### run by cmd #####
HELP = 'python draw_multi_cross_tps.py -w workload'
##### run by cmd #####

X = "cross_ratio"
Y = "multi commit network size"
# if MyPlot.language == 'chinese':
XLABEL = "跨片率"
YLABEL = "平均通信量（字节）"
# else:
# XLABEL = "Threads"
# YLABEL = "Troughput(KTxn/s)"

import pandas as pd
import argparse
import sys

sys.path.extend(['.', '..'])
from plot.parse import parse_records_from_file
import matplotlib.pyplot as plt
from plot.plot import MyPlot

#################### 参数解析 ####################
parser = argparse.ArgumentParser(HELP)
parser.add_argument("-w", "--workload", type=str, required=True, help="workload: smallbank or ycsb")
args = parser.parse_args()
assert args.workload in ['smallbank', 'ycsb']
workload = args.workload

savepath = 'multi-network-' + workload + '-size.pdf'

#################### 数据准备 ####################
log_files = [
    "./data/calvin-{workload}-uniform".format(workload=workload),
    "./data/no-batch-{workload}-uniform".format(workload=workload),
    "./data/batch-{workload}-uniform".format(workload=workload),
]
schemas = [
    "Calvin-L",
    "Prophet$_\mathit{origin}$",
    "Prophet$_\mathit{batch}$",
]

recses = []
for schema, file in zip(schemas, log_files):
    print("read:", file)
    if not file:
        print("file not found")
        sys.exit(1)
    else:
        with open(file) as f:
            content = f.read()
        rec = parse_records_from_file(content)
        rec = rec[rec['cross_ratio'] != 0]
        rec['schema'] = schema
        recses.append(rec)

recs = pd.concat(recses, ignore_index=True)

schemas = [
    # 里面是 (协议名称, 颜色(RGB格式)的元组)
    ('Calvin-L'                     , '#45C686'),
    ('Prophet$_\mathit{origin}$'    , '#ED9F54'),
    ('Prophet$_\mathit{batch}$'     , '#8E5344'),
]

#################### 画图 ####################
p = MyPlot(1, 1)
ax: plt.Axes = p.axes
ax.grid(axis=p.grid, linewidth=p.border_width)
p.init(ax)

for idx, (schema, color) in enumerate(schemas):
    records = recs[recs['schema'] == schema]
    p.bar(
        ax,
        xdata=[_ + (idx-1) * 0.3 for _ in range(records[X].size)],
        ydata=(records[Y] * ((8 + 8 + 8 + 4) if "origin" in schema else (4 + 8 + 5 * 8 + 32)) / records['average commit']) * 100 + (((records['network size'] - records[Y]) * (32 + 32 + 8 + 8 + 4) / records['average commit'])) * 100,
        color=color, legend_label=schema + '(提交)',
        width=0.3,
        hatch='//'
    )
    
    p.bar(
        ax,
        xdata=[_ + (idx-1) * 0.3 for _ in range(records[X].size)],
        ydata=(((records['network size'] - records[Y]) * (32 + 32 + 8 + 8 + 4) / records['average commit'])) * 100,
        color=color, legend_label=schema + '(读取)',
        width=0.3,
        # hatch=['xx', '//', r'\\'][idx]
    )
    

# 设置X轴标签
ax.set_xticks(range(4), [1, 5, 10, 30])

# 自适应Y轴变化
p.format_yticks(ax, suffix='K')

# 设置label
p.set_labels(ax, XLABEL, YLABEL)

# 设置图例
p.legend(ax, loc="upper center", ncol=len(schemas), anchor=(0.5, 1.20), kwargs={ 'size': 10 })

# 保存
p.save(savepath)
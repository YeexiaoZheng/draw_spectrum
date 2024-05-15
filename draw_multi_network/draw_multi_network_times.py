##### run by cmd #####
HELP = 'python draw_multi_cross_tps.py -w workload'
##### run by cmd #####

X = "cross_ratio"
Y = "multi commit network size"
# if MyPlot.language == 'chinese':
XLABEL = "跨片率"
YLABEL = "平均交互次数"
# else:
# XLABEL = "Threads"
# YLABEL = "Troughput(KTxn/s)"

import pandas as pd
import argparse
import sys

sys.path.extend(['.', '..', '../..'])
from plot.parse import parse_records_from_file
import matplotlib.pyplot as plt
from plot.plot import MyPlot
from name import NAME

#################### 参数解析 ####################
parser = argparse.ArgumentParser(HELP)
parser.add_argument("-w", "--workload", type=str, required=True, help="workload: smallbank or ycsb")
args = parser.parse_args()
assert args.workload in ['smallbank', 'ycsb']
workload = args.workload

savepath = 'multi-network-' + workload + '.pdf'

#################### 数据准备 ####################
log_files = [
    "./data/calvin-{workload}-uniform".format(workload=workload),
    "./data/sparkle-{workload}-uniform".format(workload=workload),
    "./data/no-batch-{workload}-uniform".format(workload=workload),
    "./data/batch-{workload}-uniform".format(workload=workload),
]
schemas = [
    "Calvin-L",
    "Sparkle",
    NAME + "$_\mathit{origin}$",
    NAME + "$_\mathit{batch}$",
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
    ('Sparkle'                      , '#808080'),
    (NAME + '$_\mathit{origin}$'    , '#ED9F54'),
    (NAME + '$_\mathit{batch}$'     , '#8E5344'),
]

#################### 画图 ####################
p = MyPlot(1, 1)
ax: plt.Axes = p.axes
ax.grid(axis=p.grid, linewidth=p.border_width)
p.init(ax)

data = {}

for idx, (schema, color) in enumerate(schemas):
    records = recs[recs['schema'] == schema]
    p.bar(
        ax,
        xdata=[_ + (idx-1.5) * 0.2 for _ in range(records[X].size)],
        ydata=(records['network size'] / records['average commit']) * 100,
        color=color, legend_label=schema + '(C)',
        width=0.2,
        hatch='//'
    )
    data[schema + ' all'] = (records['network size'] / records['average commit']) * 100

    p.bar(
        ax,
        xdata=[_ + (idx-1.5) * 0.2 for _ in range(records[X].size)],
        ydata=((records['network size'] - records[Y]) / records['average commit']) * 100,
        color=color, legend_label=schema + '(R)',
        width=0.2,
        # hatch=['xx', '//', r'\\'][idx]
    )
    data[schema + ' read'] = ((records['network size'] - records[Y]) / records['average commit']) * 100
    data[schema + ' commit'] = data[schema + ' all'] - data[schema + ' read']
    

# 设置X轴标签
ax.set_xticks(range(4), [1, 5, 10, 30])

# 自适应Y轴变化
p.format_yticks(ax, suffix=None)

# 设置label
p.set_labels(ax, XLABEL, YLABEL)

# 设置图例
p.legend(ax, loc="upper center", ncol=len(schemas), anchor=(0.5, 1.15), columnspacing=0.3, kwargs={ 'size': 8 })
# handles, labels = ax.get_legend_handles_labels()
# print(handles, labels)
# h1 = ax.bar(0, 0, color='white', ec='black', ls='-', lw=1, label='提交', hatch='//')
# h2 = ax.bar(0, 0, color='white', ec='black', ls='-', lw=1, label='读取')
# handles_ = [handle for idx, handle in enumerate(handles) if idx % 2 == 1]# + [h1, h2]
# labels_ = [label for idx, label in enumerate(labels) if idx % 2 == 1]# + ['提交', '读取']
# p.legend(
#     ax, 
#     handles=handles_,
#     labels=labels_,
#     loc="upper center", 
#     ncol=2, 
#     anchor=(0.5, 1.20), 
#     # columnspacing=0.3, 
#     kwargs={ 'size': 10 }
# )

# 保存
p.save(savepath)

with open(savepath.split(".")[0], 'w') as f:
    for k, v in data.items():
        f.write(k + '\n')
        for i in v:
            f.write(str(i) + '\n')
        f.write('\n')
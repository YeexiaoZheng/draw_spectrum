##### run by cmd #####
HELP = 'python draw_multi_latency.py -w workload'
##### run by cmd #####

X = "percentile"
Y = "latency"
# if MyPlot.language == 'chinese':
XLABEL = "分位数"
YLABEL = "延迟（微秒）"
# else:
# XLABEL = "Threads"
# YLABEL = "Troughput(KTxn/s)"

import pandas as pd
import argparse
import sys

sys.path.extend(['.', '..', '../..'])
import matplotlib.pyplot as plt
from plot.plot import MyPlot

#################### 参数解析 ####################
parser = argparse.ArgumentParser(HELP)
parser.add_argument("-w", "--workload", type=str, required=True, help="workload: smallbank or ycsb")
args = parser.parse_args()
assert args.workload in ['smallbank', 'ycsb']
workload = args.workload

savepath = 'multi_latency_' + workload + '.pdf'

#################### 数据准备 ####################
data = {
    'smallbank': {
        '不采用复用策略':   [314, 640, 654],
        '采用复用策略':     [269, 444, 476],
    },
    'ycsb': {
        '不采用复用策略':   [459, 903, 1017],
        '采用复用策略':     [395, 658, 722],
    }
}
data = data[workload]

recs = pd.DataFrame(columns=['schema', 'percentile', 'latency'])
for schema in data.keys():
    for idx, perc in enumerate(['50%', '95%', '99%']):
        recs.loc[len(recs.index)] = [schema, perc, data[schema][idx]]


schemas = [
    # 里面是 (协议名称, 颜色(RGB格式)的元组)
    ('不采用复用策略'    , '#ED9F54'),
    ('采用复用策略'     , '#8E5344'),
]

#################### 画图 ####################
p = MyPlot(1, 1)
ax: plt.Axes = p.axes
ax.grid(axis=p.grid, linewidth=p.border_width)
p.init(ax)

for idx, (schema, color) in enumerate(schemas):
    records = recs[recs['schema'] == schema]
    print(records[Y])
    p.bar(
        ax,
        xdata=[_ + (idx-0.5) * 0.3 for _ in range(records[X].size)],
        ydata=records[Y],
        color=color, legend_label=schema,
        width=0.3,
        hatch=['//', 'xx', r'\\'][idx]
    )

# 设置X轴标签
ax.set_xticks(range(3), ['50%', '95%', '99%'])

# 自适应Y轴变化
p.format_yticks(ax, suffix=None)

# 设置label
p.set_labels(ax, XLABEL, YLABEL)

# 设置图例
p.legend(ax, loc="upper center", ncol=len(schemas), anchor=(0.5, 1.15))

# 保存
p.save(savepath)
##### run by cmd #####
HELP = 'python draw_skew_tps.py -w workload -t threads'
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
from Schemas import schemas, schemas_for_pre
schemas = [
    ('SpectrumNoPartial'    ,   '#595959'),
    ('Spectrum'             ,   '#D95353')
]

schemas_dict = {
    'SpectrumNoPartial'     :   'Spectrum-C',
    'Spectrum'              :   'Spectrum-P'
}

#################### 参数解析 ####################
parser = argparse.ArgumentParser(HELP)
parser.add_argument("-w", "--workload", type=str, required=True, help="workload: smallbank or ycsb")
parser.add_argument("-t", "--threads", type=str, required=True, help="threads")
args = parser.parse_args()
assert args.workload in ['smallbank', 'ycsb', 'tpcc', 'pre']
workload = args.workload
if workload == 'tpcc':
    XLABEL = "Number of Items"
if workload == 'pre':
    schemas = schemas_for_pre
    schemas_dict = {
        'SpectrumPreSched': 'Spectrum-P$_\mathit{Sched}$',
        'Spectrum': 'Spectrum-P',
        'SpectrumNoPartial': 'Spectrum-C',
    }

threads = args.threads

savepath = f'skew-tps-{workload}-{threads}.pdf'

#################### 数据准备 ####################
recs = pd.read_csv(f'./data/{workload}_{threads}.csv')
# recs = recs[recs['zipf'] >= 0.9].reset_index(drop=True)
# recs = recs[recs['zipf'] <= 1.3].reset_index(drop=True)
inner_schemas = recs['protocol'].unique()
print(inner_schemas)

#################### 画图 ####################
p = MyPlot(1, 1)
ax: plt.Axes = p.axes
ax.grid(axis=p.grid, linewidth=p.border_width)
p.init(ax)

annotation_points = []

for idx, (schema, color) in enumerate(schemas):
    if threads == '36' and schema == 'Aria': continue
    records = recs[recs['protocol'] == schema]
    # print(schema, records[Y])
    p.plot(
        ax,
        xdata=records[X],
        ydata=records[Y],
        color=color, legend_label=schemas_dict[schema] if schemas_dict.get(schema) else schema,
        # marker=['s', 'o', ][idx]
    )
    if schema == 'Spectrum':
        annotation_points = [records[X].values, records[Y].values]

points = [(annotation_points[0][i], annotation_points[1][i]) for i in range(len(annotation_points[0]))]
label_points = recs[recs['protocol'] == schemas[1][0]][Y].reset_index(drop=True) / recs[recs['protocol'] == schemas[0][0]][Y].reset_index(drop=True)
print(label_points)

# 只标注0, 2, 4位置
def position(index, point):
    match workload:
        case "ycsb":
            match index:
                case 0: return (point[0] + 0.01, point[1] - 10000)
                case 1: return (point[0] + 0.01, point[1] + 10000)
                case 2: return (point[0]       , point[1] + 10000)
                case 3: return (point[0] - 0.01, point[1] + 10000)
                case 4: return (point[0] - 0.02, point[1] + 15000)
                case _: return None
        case "tpcc":
            match index:
                case 0: return (point[0] + 1  , point[1] - 1000)
                case 1: return (point[0] + 0.5, point[1] + 1000)
                case 2: return (point[0] + 0.3, point[1] + 1200)
                case 3: return (point[0] - 0.5, point[1] + 2000)
                case 4: return (point[0] - 1.6, point[1] + 2500)
                case _: return None
        case "smallbank":
            match index:
                case 0: return (point[0] + 0.015, point[1] - 10000)
                case 1: return (point[0] + 0.01, point[1] + 10000)
                case 2: return (point[0] + 0.01, point[1] + 10000)
                case 3: return (point[0] - 0.01, point[1] + 50000)
                case 4: return (point[0] - 0.034, point[1] + 70000)
                case _: return None
        case _: return None

for i in range(5):
    point = points[i]
    plt.annotate(
        str(round(label_points[i], 2)) + 'x', 
        xy=(point[0], point[1]), 
        xytext=position(i, point),
        color='black',
    ) 

# print(recs[recs['protocol'] == schemas[0][0]][Y])
# print(recs[recs['protocol'] == schemas[1][0]][Y])
# print(recs[recs['protocol'] == schemas[1][0]][Y].reset_index(drop=True) / recs[recs['protocol'] == schemas[0][0]][Y].reset_index(drop=True))

print(type(recs['zipf'].unique()), recs['zipf'].unique())
# 设置X轴标签
# ax.set_xticks(range(len(recs['zipf'].unique())), [str(t) for t in recs['zipf'].unique()])

# 自适应Y轴变化
p.format_yticks(ax, suffix='M' if workload == 'smallbank' else 'K', step=14000 if workload == 'tpcc' else None)
# ax.set_ylim(None, p.max_y_data * 1.15)       # 折线图的Y轴上限设置为数据最大值的1.15倍

# 设置label
p.set_labels(ax, XLABEL, YLABEL)

# 设置图例
if workload == 'pre':
    handles, labels = ax.get_legend_handles_labels()
    if threads == '36':
        label_order = ['Spectrum-P$_\mathit{Sched}$', 'Sparkle', 'Spectrum-P', 'AriaFB', 'Spectrum-C', 'Calvin']
    else:
        label_order = ['Spectrum-P$_\mathit{Sched}$', 'Spectrum-P', 'Spectrum-C', 'AriaFB', 'Aria', 'Sparkle', 'Calvin']
    handles = [handles[i] for i in [labels.index(label) for label in label_order]]
    labels = label_order
    p.legend(ax, loc="upper center", ncol=3, anchor=(0.5, 1.20) if threads == '36' else (0.5, 1.25), columnspacing=0.5,
            handles=handles, labels=labels, kwargs={ 'size': 10 })
else:
    p.legend(ax, loc="upper center", ncol=3, anchor=(0.5, 1.25) if workload == 'pre' else (0.5, 1.15))

# 保存
p.save(savepath)
##### run by cmd #####
HELP = 'python draw_sched_overhead -f afilename'
##### run by cmd #####

X = "zipf"
XLABEL = "工作负载"
Y = "average commit"
YLABEL = "吞吐(交易/秒)"

from typing import List, Tuple
import pandas as pd
import argparse
import sys
sys.path.extend(['.', '..'])
import matplotlib.pyplot as plt
from parse import parse_meta, parse_record, parse_records_from_file
from plot import MyPlot
from common import adaptive_y, to_fomat

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

    for idx, (workload, protocol, color, _) in enumerate(protocols):
        print([_ + (idx-0.5) * 0.3 for _ in range(records[records['protocol'] == protocol][x].size)])
        tmp = [
            [-0.1 + 0.2, 0.9 - 0.2],
            [0.1 + 0.2, 1.1 - 0.2],
        ]
        if idx // 2 == 0:
            ax.bar(
                # [_ + (idx-0.5) * 0.3 for _ in range(records[records['protocol'] == protocol][x].size)], 
                tmp[idx],
                # workload,
                # records[records[records['protocol'] == protocol]['workload'] == workload][y], 
                # records.loc[idx, 'average commit'],
                records[records['protocol'] == protocol][y],
                color=color, label='不采用检查点' if to_fomat(protocol) == 'Sparkle' else '采用检查点',
                width=0.18,
                ec='black', ls='-', lw=1,
                hatch='xx' if idx == 1 else '//'
            )
            tmp_max =  records[records['protocol'] == protocol][y].max() 
            if tmp_max > max_y: max_y = tmp_max

    ax.set_xlim(-0.2, 1.2)
    ax.set_xticks([0.2, 0.8], ['YCSB', 'Smallbank'])
    

    ystart = 0

    ax.set_ylim(ystart, max_y * 1.1)
    ax.set_xlabel(xlabel, p.label_config_dic)
    ax.set_ylabel(ylabel, p.label_config_dic)

    # 自适应Y轴变化
    max_y = int(max_y)
    step=adaptive_y(int(max_y) - ystart, 4)

    ax.set_yticks(
        range(ystart, max_y, step), 
        [str(x)[:-3] + 'K' if len(str(x)) >3 else str(x) for x in range(ystart, max_y, step)]
    )
    
    p.legend(ax, loc="upper center", ncol=1, anchor=None)
    if savefig: p.save(savepath)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(HELP)
    parser.add_argument("-f1", "--log_file1", type=str, required=True, help="which log file to parse")
    parser.add_argument("-f2", "--log_file2", type=str, required=True, help="which log file to parse")

    args = parser.parse_args()

    # 读取log
    with open(args.log_file1) as f1:
        content1 = f1.read()
    # 处理日志开始的实验参数, 目前只是打印了一下
    meta1 = parse_meta(content1.split("@")[0].strip())
    # 处理日志并生成一个data frame
    recs1 = parse_records_from_file(content1)
    # 添加一列数据workload为ycsb
    recs1['workload'] = 'ycsb'

    # 读取log
    with open(args.log_file2) as f2:
        content2 = f2.read()
    # 处理日志开始的实验参数, 目前只是打印了一下
    meta2 = parse_meta(content2.split("@")[0].strip())
    # 处理日志并生成一个data frame
    recs2 = parse_records_from_file(content2)
    # 添加一列数据workload为smallbank
    recs2['workload'] = 'smallbank'

    # 合并两个dataframe
    recs = pd.concat([recs1, recs2]).reset_index(drop=True)
    print(recs)

    # recs = recs[recs['zipf'] >= 0.9].reset_index(drop=True)
    # recs = recs[recs['zipf'] < 1.4].reset_index(drop=True)
    # recs = recs[recs['zipf'].isin([0.00, 0.12, 0.24, 0.36, 0.48, 0.60, 0.72, 0.84, 0.96])]
    # recs = recs[recs['zipf'].isin([0.00, 0.24, 0.48, 0.72, 0.96])]
    # print(recs)

    plot_by_protocol(
        recs, 
        (X, XLABEL), (Y, YLABEL), 
        [
            # 里面是 (协议名称, 颜色(RGB格式)的元组)
            ('ycsb',        'sparkle original' , '#595959'    , None),
            ('ycsb',        'sparkle partial'  , '#D95353'    , None),
            ('smallbank',   'sparkle original' , '#595959'    , None),
            ('smallbank',   'sparkle partial'  , '#D95353'    , None),
        ],
        savefig=True,
        savepath='overhead' + ".pdf"
    )

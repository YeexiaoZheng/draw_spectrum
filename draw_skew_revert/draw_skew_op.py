##### run by cmd #####
HELP = 'python comp-original -f afilename'
##### run by cmd #####

X = "zipf"
XLABEL = "Contention Degree (Zipf)"
Y = "average operations"
YLABEL = "Rollback OPs(K) / Commit"

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
        _records: pd.DataFrame, 
        x: tuple, y: tuple, 
        protocols: List[Tuple[str, Tuple[float, float, float]]], 
        figsize=None, 
        savefig: bool=None,
        savepath: str=None
        ):
    x, xlabel = x
    y, ylabel = y
    y_, ylabel_ = 'original revert length', 'Complete Rollback OPs'

    p = MyPlot(1, 1)
    ax: plt.Axes = p.axes

    ax.grid(axis=p.grid, linewidth=p.border_width)
    ax.set_axisbelow(True)

    # ax2 = ax.twinx()

    max_y = _records[y].max()
    for idx, (protocol, color) in enumerate(protocols):

        if idx == 0:
            records = _records[_records['revert'] == 'original']
            ax.bar(
                [_ + (idx-0.5) * 0.4 for _ in range(records[x].size)], 
                records[y],
                color=color, label=ylabel_,
                width=0.4,
                ec='black', ls='-', lw=1,
                hatch='//'
            )
            continue
        
        records = _records[_records['revert'] == 'revert']
        ax.bar(
            [_ + (idx-0.5) * 0.4 for _ in range(records[x].size)], 
            records[y],
            color=color, label="Partial Rollback OPs",
            width=0.4,
            ec='black', ls='-', lw=1,
            hatch='xx'
        )
        
    # ax2.plot(
    #     range(records[records['protocol'] == protocols[0][0]][x].size),
    #     # records[records['protocol'] == protocols[0][0]][y].reset_index(drop=True).div(records[records['protocol'] == protocols[1][0]][y_].reset_index(drop=True)),
    #     records[records['protocol'] == protocols[1][0]][y].reset_index(drop=True).div(records[records['protocol'] == protocols[1][0]]['average commit'].reset_index(drop=True)).reset_index(drop=True).div(records[records['protocol'] == protocols[0][0]][y_].reset_index(drop=True).div(records[records['protocol'] == protocols[0][0]]['average commit'].reset_index(drop=True)).reset_index(drop=True)),
    #     color="grey", label="Rate", marker=p.marker_list[-1], markersize=p.marker_size, linewidth=p.line_width
    # )

    ax.set_xlabel(xlabel, fontdict=p.label_config_dic)
    ax.set_ylabel(ylabel, fontdict=p.label_config_dic)

    ax.set_xticks(range(5), [i / 10 for i in range(9, 14, 1)])

    # ax.set_yscale('symlog')
    # 自适应Y轴变化
    max_y = int(max_y)
    print(max_y)
    # step=adaptive_y(int(max_y), 5)
    step=200

    ax.set_yticks(
        range(0, max_y, step), 
        [str(x / 1000) if x!= 0 else 0 for x in range(0, max_y, step)]
    )

    p.legend(ax, anchor=None, ncol=1, loc="upper center")
    # p.legend(ax2, anchor=(0.5, 1.25))
    if savefig: p.save(savepath)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(HELP)
    parser.add_argument("-f1", "--log_file1", type=str, required=True, help="which log file to parse")
    parser.add_argument("-f2", "--log_file2", type=str, required=True, help="which log file to parse")

    args = parser.parse_args()

    # 读取log
    with open(args.log_file1, encoding='utf-8') as f1:
        content1 = f1.read()
    # 处理日志开始的实验参数, 目前只是打印了一下
    meta1 = parse_meta(content1.split("@")[0].strip())
    # 处理日志并生成一个data frame
    recs1 = parse_records_from_file(content1)
    # 添加一列数据workload为ycsb
    recs1['revert'] = 'original'

    # 读取log
    with open(args.log_file2, encoding='utf-8') as f2:
        content2 = f2.read()
    # 处理日志开始的实验参数, 目前只是打印了一下
    meta2 = parse_meta(content2.split("@")[0].strip())
    # 处理日志并生成一个data frame
    recs2 = parse_records_from_file(content2)
    # 添加一列数据workload为smallbank
    recs2['revert'] = 'revert'

    # 合并两个dataframe
    recs = pd.concat([recs1, recs2]).reset_index(drop=True)

    recs = recs[recs['zipf'] >= 0.88].reset_index(drop=True)
    recs = recs[recs['zipf'] < 1.4].reset_index(drop=True)

    print(recs)

    plot_by_protocol(
        recs, 
        (X, XLABEL), (Y, YLABEL), 
        [
            # 里面是 (协议名称, 颜色(RGB格式)的元组)
            # ('sparkle original' , 'black'),
            # ('sparkle partial'  , 'red'),
            # ('sparkle partial'  , '#fb8402'),
            ('sparkle partial'  , '#595959'), #FFA500 #FF6F61 #D3D3D3 #8F9779 #6F8D75 #CD5A3D #FF5733 #FF8C66 #D95353
            ('sparkle partial'  , '#D95353'), #008080 #6A5ACD #87CEEB #CDBCB3 #A6725E #A36E5C #4B0082 #663399 #555555
        ],
        savefig=True,
        savepath=('ycsb_op_rollback' if 'ycsb' in args.log_file1 else 'smallbank_op_rollback') + ".pdf"
    )

##### run by cmd #####
HELP = 'python draw_skew_cascade.py -f afilename'
##### run by cmd #####

X = "zipf"
XLABEL = "倾斜程度 ($\mathit{Zipf}$)"
Y = "average abort"
YLABEL = "平均中止数"

from typing import List, Tuple
import pandas as pd
import argparse
import sys
sys.path.extend(['.', '..'])
import matplotlib.pyplot as plt
from parse import parse_meta, parse_record, parse_records_from_file
from plot import MyPlot
from common import adaptive_y, to_fomat

p = MyPlot(1, 1)
ax: plt.Axes = p.axes

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

    max_y = 0
    for idx, (workload, protocol, color, marker) in enumerate(protocols):
        records = _records[_records['workload'] == workload.lower()]
        print(records[records['protocol'] == protocol][y].reset_index(drop=True).div(records[records['protocol'] == protocol]['average commit'].reset_index(drop=True)) * 1000000)
        p.plot(
            ax,
            [str(round(i, 1)) for i in records[records['protocol'] == protocol.lower()][x]], 
            xlabel,
            # records[records['protocol'] == protocol.lower()][y], 
            records[records['protocol'] == protocol][y].reset_index(drop=True).div(records[records['protocol'] == protocol]['average commit'].reset_index(drop=True)) * 1000000, 
            ylabel,
            legend_label=('部分回滚' if 'partial' in protocol.lower() else '完全回滚') + '(' + to_fomat(workload) + ')',
            color=color,
            marker=marker
        )
        tmp_max = records[records['protocol'] == protocol][y].reset_index(drop=True).div(records[records['protocol'] == protocol]['average commit'].reset_index(drop=True)).max() * 1000000
        if tmp_max > max_y: max_y = tmp_max

    # 自适应Y轴变化
    max_y = int(max_y)
    step=adaptive_y(int(max_y), 4)

    ax.set_yticks(
        range(0, max_y, step), 
        [str(x)[:-6]+'M' if len(str(x)) >6 else str(x) for x in range(0, max_y, step)]
    )

    # p.legend(ax, loc="upper center", ncol=len(protocols), anchor=(0.5, 1.166))
    # if savefig: p.save(savepath)

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

    recs = recs[recs['zipf'] >= 0.9].reset_index(drop=True)
    recs = recs[recs['zipf'] < 1.4].reset_index(drop=True)

    plot_by_protocol(
        recs, 
        (X, XLABEL), (Y, YLABEL), 
        [
            # 里面是 (协议名称, 颜色(RGB格式), 标记的元组)
            ('ycsb', 'sparkle original' , '#595959'    , 's'),
            ('smallbank', 'sparkle original' , '#595959'    , '^'),
            ('ycsb', 'sparkle partial'  , '#D95353'    , 'o'),
            
            ('smallbank', 'sparkle partial'  , '#D95353'    , 'v'),
        ],
        savefig=True,
        savepath="cascade" + ".pdf"
    )
    
    p.legend(ax, loc="upper center", ncol=2, anchor=(0.5, 1.24))
    p.save("cascade.pdf")

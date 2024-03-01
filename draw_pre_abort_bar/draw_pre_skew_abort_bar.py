##### run by cmd #####
HELP = 'python draw_skew_tps.py -f afilename'
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
from common import adaptive_y, to_fomat, add_serial

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

    p = MyPlot(1, 1)
    ax: plt.Axes = p.axes

    ax.grid(axis=p.grid, linewidth=p.border_width)
    ax.set_axisbelow(True)

    max_y = 0
    for idx, (protocol, color, marker) in enumerate(protocols):
        records = _records[_records['protocol'] == protocol]
        print(records[y].div(records['average commit']) * 1000000,)
        ax.bar(
            [_ + (idx-1.5) * 0.2 for _ in range(records[x].size)], 
            records[y].div(records['average commit']) * 1000000,
            # records[y],
            color=color, label=to_fomat(protocol, True),
            width=0.2,
            ec='black', ls='-', lw=1,
            hatch=['++', r'\\', 'xx', '//'][idx]
        )
        tmp_max =  records[records['protocol'] == protocol][y].max() 
        # tmp_max =  records[y].div(records['average commit']).max()
        if tmp_max > max_y: max_y = tmp_max

    ax.set_xticks(range(5), [str(x / 10) for x in range(9, 14)])

    ax.set_yscale('log')

    # 自适应Y轴变化
    # max_y = int(max_y)
    # step = int(adaptive_y(max_y))
    # step = 80000

    # ax.set_yticks(
    #     range(0, max_y, step), 
    #     [str(x)[:-3] if len(str(x)) > 4 else str(x) for x in range(0, max_y, step)]
    # )

    ax.set_xlabel(xlabel, fontdict=p.label_config_dic)
    ax.set_ylabel(ylabel, fontdict=p.label_config_dic)

    p.legend(ax, anchor=None, ncol=2)

    if savefig:
        p.save(savepath)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(HELP)
    parser.add_argument("-f", "--log_file", type=str, required=True, help="which log file to parse")
    
    args = parser.parse_args()

    # 读取log
    with open(args.log_file) as f:
        content = f.read()

    # 处理日志开始的实验参数, 目前只是打印了一下
    meta = parse_meta(content.split("@")[0].strip())

    # 处理日志并生成一个data frame
    recs = parse_records_from_file(content)
    add_serial(recs, 'zipf', 27543.8)

    recs = recs[recs['zipf'] >= 0.9].reset_index(drop=True)
    recs = recs[recs['zipf'] < 1.4].reset_index(drop=True)

    plot_by_protocol(
        recs, 
        (X, XLABEL), (Y, YLABEL), 
        [
            # 里面是 (协议名称, 颜色(RGB格式), 标记的元组)
            ('sparkle partial-v2'  , '#B8448D'    , None),
            ('aria fb'          , '#45C686'    , None),
            ('sparkle partial'  , '#8E5344'    , None),
            ('sparkle original' , '#ED9F54'    , None),
        ],
        savefig=True,
        savepath=args.log_file + ".pdf"
    )

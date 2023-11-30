##### run by cmd #####
HELP = 'python draw_threads_tps.py -f afilename'
##### run by cmd #####

X = "threads"
XLABEL = "Execution Schemes"
Y = "average commit"
YLABEL = "Latency(us)"

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
        records: pd.DataFrame, 
        x: tuple, y: tuple, 
        protocols: List[Tuple[str, Tuple[float, float, float]]], 
        figsize=None, 
        savefig: bool=None,
        savepath: str=None
        ):
    x, xlabel = x
    y, ylabel = y

    p = MyPlot(2, 1, kwargs={'sharex': True})
    p.fig.clear()
    gs = p.fig.add_gridspec(4, 4, hspace=0.4)
    ax1 = p.fig.add_subplot(gs[:1, :])
    ax2 = p.fig.add_subplot(gs[1:, :])
    p.init(ax1)
    p.init(ax2)
    # ax1.sharex(ax2)
    ax1.grid(axis=p.grid, linewidth=p.border_width*2)
    ax1.set_axisbelow(True)
    ax2.grid(axis=p.grid, linewidth=p.border_width)
    ax2.set_axisbelow(True)

    max_y = 0
    for idx, (protocol, color, marker) in enumerate(protocols): 
        # if protocol.lower() == 'serial': 
        ax1.bar(
            # records[records['protocol'] == protocol][x], 
            to_fomat(protocol),
            1 / records[records['protocol'] == protocol][y] * 100 * 1000000 if protocol.lower() == 'serial' else 0, 
            label=to_fomat(protocol),
            color=color, 
            width=0.5,
            ec='black', ls='-', lw=1,
            hatch='--',
        )  

        print(protocol, ':', 1 / records[records['protocol'] == protocol][y] * 100 * 1000000)

        ax2.bar(
            # records[records['protocol'] == protocol][x], 
            to_fomat(protocol),
            1 / records[records['protocol'] == protocol][y] * 100 * 1000000, 
            label=to_fomat(protocol),
            color=color, 
            width=0.5,
            ec='black', ls='-', lw=1,
            hatch=['xx', '//', r'\\', '--'][idx],
        )
        tmp_max =  records[records['protocol'] == protocol][y].max() 
        if tmp_max > max_y: max_y = tmp_max

    ax1.spines.bottom.set_visible(False)
    ax2.spines.top.set_visible(False)

    # ax1.tick_params(axis='x',length=0)
    # ax2.xaxis.tick_bottom()
    ax1.set_xticks([])

    ax1.set_ylim(3400, 3600)
    ax2.set_ylim(0, 350)

    # 创建轴断刻度线，d用于调节其偏转角度
    d = 0.5  # proportion of vertical to horizontal extent of the slanted line
    kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
                linestyle="none", color='k', mec='k', mew=p.tick_width, clip_on=False)
    ax1.plot([0, 1], [0, 0], transform=ax1.transAxes, **kwargs)
    ax2.plot([0, 1], [1, 1], transform=ax2.transAxes, **kwargs)

    # # 自适应Y轴变化
    # max_y = int(max_y)
    # step = adaptive_y(max_y)

    # ax.set_xticks(
    #     range(6, 37, 6)
    # )
    
    # ax.set_yticks(
    #     range(0, max_y, step), 
    #     [str(x)[:-3] if len(str(x)) >3 else str(x) for x in range(0, max_y, step)]
    # )

    p.legend(ax2, loc="upper center", ncol=len(protocols) // 2, anchor=(0.5, 1.68))
    ax2.set_xlabel(xlabel, fontdict=p.label_config_dic)
    ax2.set_ylabel(ylabel, fontdict=p.label_config_dic, loc='top', labelpad=12)
    if savefig: p.save(savepath)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(HELP)
    parser.add_argument("-f", "--log_file", type=str, required=True, help="which log file to parse")
    parser.add_argument("-t", "--threads", type=int, required=True, help="threads")
    parser.add_argument("-o", "--output", type=str, required=False, help="output file name")
    parser.add_argument("-v", "--value", type=float, required=False, help="serial value")

    args = parser.parse_args()

    # 读取log
    with open(args.log_file) as f:
        content = f.read()

    # 处理日志开始的实验参数, 目前只是打印了一下
    meta = parse_meta(content.split("@")[0].strip())

    # 处理日志并生成一个data frame
    recs = parse_records_from_file(content)
    add_serial(recs, 'threads', value=args.value if args.value else None)

    # recs = recs[recs["threads"].isin([
    #     # 1, 6, 11, 16, 21, 26, 31, 36, 41, 46, 51, 56, 61, 66, 71, 76, 81, 86, 91, 96, 101, 106, 111
    #       1, 6, 11, 16, 21, 26, 31, 36, 41,     51,         66,             86,                   111
    # ])]
    recs = recs[recs["threads"].isin([1, args.threads])]

    # data = {
    #     'serial': 1 / recs[recs['protocol'] == 'serial']['average commit'].values[0] * 100 * 1000000,
    #     'sparkle partial': 1 / recs[recs['protocol'] == 'sparkle partial']['average commit'].values[0] * 100 * 1000000,
    #     'aria fb': 1 / recs[recs['protocol'] == 'aria fb']['average commit'].values[0] * 100 * 1000000,
    #     'sparkle original': 1 / recs[recs['protocol'] == 'sparkle original']['average commit'].values[0] * 100 * 1000000,
    # }

    # recs = pd.Series(data)
    # print(recs)

    plot_by_protocol(
        recs, 
        (X, XLABEL), (Y, YLABEL), 
        [
            # 里面是 (协议名称, 颜色(RGB格式), 标记的元组)
            ('sparkle partial'  , '#8E5344'    , None),
            ('sparkle original' , '#ED9F54'    , None),
            ('aria fb'          , '#45C686'    , None),
            ('serial'           , '#B9A89B'    , None),
        ],
        savefig=True,
        savepath=args.output if args.output else args.log_file + ".pdf"
    )

##### run by cmd #####
HELP = 'python draw_threads_tps.py -f afilename'
##### run by cmd #####

X = "threads"
XLABEL = "许可链系统"
Y = "average commit"
YLABEL = "吞吐量（交易 / 秒）"

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

    p = MyPlot(2, 1, figsize=(5.5, 5.5), kwargs={'sharex': True})
    p.fig.clear()
    gs = p.fig.add_gridspec(5, 5, hspace=0.2)
    ax1 = p.fig.add_subplot(gs[:3, :])
    ax2 = p.fig.add_subplot(gs[3:, :])
    p.init(ax1)
    p.init(ax2)
    # ax1.sharex(ax2)
    # ax1.grid(axis=p.grid, linewidth=p.border_width)
    ax1.set_axisbelow(True)
    # ax2.grid(axis=p.grid, linewidth=p.border_width)
    ax2.set_axisbelow(True)
    ax2.set_xticks([0, 1, 2], ['Quroum', 'Fabric', 'FastFabric'])
    ax2.tick_params(axis='x',length=0)

    max_y = 0
    for idx, (protocol, color, marker) in enumerate(protocols): 
        # if protocol.lower() in ['quroum', 'fabric']: 
        ax1.bar(
            # records[records['protocol'] == protocol][x], 
            to_fomat(protocol),
            records[records['protocol'] == protocol][y], 
            label=to_fomat(protocol),
            color=color, 
            width=0.5,
            ec='black', ls='-', lw=1,
            hatch=r'\\',
        )  

        ax2.bar(
            # records[records['protocol'] == protocol][x], 
            to_fomat(protocol),
            records[records['protocol'] == protocol][y], 
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

    ax1.set_ylim(35000, 125000)
    ax1.set_yticks([40000, 60000, 80000, 100000, 120000], ['40K', '60K', '80K', '100K', '120K'])
    ax2.set_ylim(0, 18600)

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

    ax2.set_yticks([2000, 4000, 10000], ['2K', '4K', '10K'])

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            #设置图例字体、位置、数值等等
            plt.text(rect.get_x(), 500 + height, '               ≈%sTPS' %
                    int(height), size=13, family="Times new roman", color='black', ha='center', va='bottom')
    
    autolabel(ax2.patches)

    p.legend(ax2, loc="upper center", ncol=3, anchor=(0.5, 2.9))
    ax2.set_xlabel(xlabel, fontdict=p.label_config_dic)
    ax1.set_ylabel(ylabel, fontdict=p.label_config_dic, loc='bottom', labelpad=12)
    if savefig: p.save(savepath)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(HELP)
    parser.add_argument("-o", "--output", type=str, required=False, help="output file name")
    parser.add_argument("-v", "--value", type=float, required=False, help="serial value")

    args = parser.parse_args()

    recs = pd.DataFrame({
        'protocol': ['Quroum', 'Fabric', 'FastFabric', 'NNN'],
        'average commit': [1500, 3000, 18000, 0]
    })

    print(recs)

    plot_by_protocol(
        recs, 
        (X, XLABEL), (Y, YLABEL), 
        [
            # 里面是 (协议名称, 颜色(RGB格式), 标记的元组)
            ('Quroum'   , '#8E5344'    , None),
            ('Fabric'   , '#ED9F54'    , None),
            ('FastFabric'      , '#45C686'    , None),
            # ('NNN'      , '#4C7D7B'    , None),
        ],
        savefig=True,
        savepath="compare.png"
    )

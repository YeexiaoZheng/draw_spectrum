##### run by cmd #####
HELP = 'python draw_skew_tps.py -x "zipf" -xl "Skew" -y "average commit" -yl "Troughput(K tx/s)" -f afilename'
##### run by cmd #####

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
        protocols: List[Tuple[str, Tuple[float, float, float]]], 
        figsize=None, 
        savefig: bool=None,
        savepath: str=None
        ):
    
    p = MyPlot(1, 1, (10, 4))
    ax: plt.Axes = p.axes

    max_y = 0
    for idx, (protocol, color, marker) in enumerate(protocols):
        p.plot(
            ax,
            records[protocol].index, 
            "time",
            records[protocol].values,
            "Troughtput(K tx/s)",
            legend_label=to_fomat(protocol),
            color=color, 
            marker=marker
        )
        tmp_max =  records[protocol].values.max() 
        if tmp_max > max_y: max_y = tmp_max

    ax.set_ylim(0, None)

    # 自适应Y轴变化
    max_y = int(max_y)
    step = adaptive_y(max_y)

    ax.set_yticks(
        range(0, max_y, step), 
        [str(x)[:-3] if len(str(x)) > 4 else str(x) for x in range(0, max_y, step)]
    )

    p.legend(ax, loc="upper center", ncol=len(protocols), anchor=(0.5, 1.17))
    if savefig: p.save(savepath)

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
    original_recs = parse_records_from_file(content)
    'commit at sec {i}'
    condition = (1.05, 1.15)
    original_recs = original_recs[(original_recs['zipf'] > 1.05) & (original_recs['zipf'] < 1.15)]

    def get_from_original(protocol, sec) -> int:
        return original_recs[original_recs['protocol'] == protocol]['commit at sec ' + str(sec)].values[0]

    seconds = list(range(100))
    recs = pd.DataFrame(
        {
            'sparkle original': [get_from_original('sparkle original', sec) for sec in seconds],
            'sparkle partial': [get_from_original('sparkle partial', sec) for sec in seconds],
            'aria fb': [get_from_original('aria fb', sec) for sec in seconds]
        },
        index=seconds
    )

    plot_by_protocol(
        recs, 
        [
            # 里面是 (协议名称, 颜色(RGB格式), 标记的元组)
            ('sparkle original' , '#ED9F54'    , 'None'),
            ('sparkle partial'  , '#8E5344'    , 'None'),
            ('aria fb'          , '#45C686'    , 'None'),
        ],
        savefig=True,
        savepath="t_tps" + ".png"
    )

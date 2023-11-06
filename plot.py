from collections.abc import Iterable
from typing import List
import matplotlib.pyplot as plt

class MyPlot:
    ##### 参数 #####

    # 全局
    # font = 'Arial'          # 字体
    font = 'Microsoft YaHei'
    dpi = 300
    weight = 'bold'

    # 图例相关
    anchor = (0.5, 1.23)    # 相对位置
    legend_word_size = 13   # 图例字体大小

    # 画布相关
    figsize = (5, 4)        # 画布大小
    facecolor = 'white'     # 背景颜色

    # 边框相关
    border_width = 1.5      # 边框宽度
    grid = 'y'              # 网格线

    # 刻度相关
    tick_length = 10            # 刻度长度
    tick_width = border_width   # 刻度宽度默认和边框宽度相同
    tick_word_size = 15         # 刻度字体大小
    tick_toward = 'out'         # 刻度朝向

    # label标签相关
    label_config_dic = {
        'family': font,
        'weight': weight,       # 粗细：normal bold
        'size': 17,             # 大小
    }

    # 线相关
    line_width = 2              # 线的宽度

    # 点相关
    # marker_list = ['o', 's', 'v', '^', '<', '>', '1', '2', '3', '4']    # 点的形状
    marker_list = ['>', '<', '^', 'v', 's', 'o']        # 点的形状 pop
    marker_size = 7                                                      # 点大小

    ##### 变量 #####
    fig: plt.Figure = None
    axes: List[plt.Axes] = None

    def init(self, ax):
        ax: plt.Axes = ax
        ax.spines['bottom'].set_linewidth(self.border_width)
        ax.spines['left'].set_linewidth(self.border_width)
        ax.spines['top'].set_linewidth(self.border_width)
        ax.spines['right'].set_linewidth(self.border_width)
        ax.tick_params(
            which='major', 
            length=self.tick_length, 
            width=self.tick_width, 
            labelsize=self.tick_word_size,
            direction=self.tick_toward,
        )

    def __init__(
        self,
        nrows: int,     # 行数
        ncols: int,     # 列数
        figsize: tuple=None,
    ):
        plt.rcParams['font.sans-serif'] = [self.font]
        plt.rcParams['font.size'] = self.legend_word_size
        plt.rcParams['font.weight'] = self.weight
        plt.rcParams ['savefig.dpi'] = 300
        
        self.fig, self.axes = plt.subplots(
            nrows=nrows, 
            ncols=ncols,
            figsize=figsize or self.figsize,
            facecolor=self.facecolor
        )

        if isinstance(self.axes, Iterable):
            for axs in self.axes:
                if isinstance(axs, Iterable):
                    for ax in axs:
                        self.init(ax)
                else: self.init (axs)
        else: self.init(self.axes)       
    
    def plot(
        self,
        ax: plt.Axes,
        xdata: list,
        xlabel: str,
        ydata: list,
        ylabel: str,
        legend_label: str,
        color: str,
        marker: str=None,
        nogrid: bool=False
    ):
        ax.plot(
            xdata,
            ydata,
            color=color,
            label=legend_label,
            marker=None if marker == 'None' else marker or self.marker_list.pop(),
            markersize=self.marker_size,
            linewidth=self.line_width
        )
        ax.set_xlabel(xlabel, self.label_config_dic)
        ax.set_ylabel(ylabel, self.label_config_dic)
        if not nogrid: ax.grid(axis=self.grid, linewidth=self.border_width)

    def legend(
        self, 
        ax: plt.Axes, 
        loc="upper center", 
        ncol=3, 
        anchor=None,
        frameon=False
    ):
        ax.legend(
            loc=loc, 
            ncol=ncol, 
            bbox_to_anchor=anchor or self.anchor, 
            frameon=frameon,
        )

    def save(self, path, bbox_inches='tight'):
        plt.savefig(path, bbox_inches=bbox_inches)
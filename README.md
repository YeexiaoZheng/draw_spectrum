# README

## 架构

以每个draw_xxx_xxx文件夹下的py为画图 -f 参数表示文件路径，此py会调用parse.py解析log，并调用plot.py初始化一些plt参数

parse.py为解析log的函数，天骥写，我略作修改的

plot.py为MyPlot类，初始化了很多变量，就不需要在每个函数里重新写一遍全局变量，其中封装了新的plot函数，稍微方便一丢丢ax.plot()，也可以使用p.axes成员变量按照plt.Axes类的方式直接画图，例如draw_skew_revert就是采用MyPlot初始化，ax方法画图

## py文件运行

文件现只包含-f参数，运行以下命令：

```shell
python draw_xxx_xxx.py -f filename
```

即可生成与filename同名的pdf文件，需注意每个图的label是写死在代码中的，参考每个py文件的最上方X, XLABEL等全局变量
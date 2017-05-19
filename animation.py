import matplotlib
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from IPython.display import HTML, Image
import pandas
from matplotlib.path import Path
import matplotlib.patches as patches
import matplotlib.image as plti

###########读取数据################

info = pandas.read_csv('/Users/james/Desktop/nba.csv')
info.columns = ['number', 'team_id', 'player_id', 'x_loc', 'y_loc', 'radius', 'moment', 'game_clock', 'shot_clock', 'player_name', 'player_jersey']

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlim(-5, 100)
ax.set_ylim(-5, 55)

##########绘制球场图################
court = plti.imread("fullcourt.png")
plt.imshow(court, zorder=0, extent=[-5,100,55,-5])


##################################
##########判断是否作为边界###########
##################################

import math
#获取基准点的下标
def get_leftbottompoint(p):
    k = 0
    for i in range(1, len(p)):
        if p[i][1] < p[k][1] or (p[i][1] == p[k][1] and p[i][0] < p[k][0]):
            k = i
    return k

#叉乘计算方法
def multiply(p1, p2, p0):
    return (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (p1[1] - p0[1])

#获取极角，通过求反正切得出，考虑pi / 2的情况
def get_arc(p1, p0):
    # 兼容sort_points_tan的考虑
    if (p1[0] - p0[0]) == 0:
        
        if ((p1[1] - p0[1])) == 0:
            return -1;
        else:
            return math.pi / 2

    tan = float((p1[1] - p0[1])) / float((p1[0] - p0[0]))
    arc = math.atan(tan)
    if arc >= 0:
        return arc
    else:
        return math.pi + arc
#对极角进行排序
def sort_points_tan(p, k):
    p2 = []
    for i in range(0, len(p)):
        p2.append({"index": i, "arc": get_arc(p[i], p[k])})
    p2.sort(key=lambda k: (k.get('arc', 0)))
    p_out = []
    for i in range(0, len(p2)):
        p_out.append(p[p2[i]["index"]])
    return p_out


def graham_scan(p):
    k = get_leftbottompoint(p)
    p_sort = sort_points_tan(p, k)
    
    p_result = [None] * len(p_sort)
    p_result[0] = p_sort[0]
    p_result[1] = p_sort[1]
    p_result[2] = p_sort[2]
    
    top = 2
    for i in range(3, len(p_sort)):
        #叉乘为正则符合条件
        while (top >= 1 and multiply(p_sort[i], p_result[top], p_result[top - 1]) > 0):
            top -= 1
        top += 1
        p_result[top] = p_sort[i]
    
    for i in range(len(p_result) - 1, -1, -1):
        if p_result[i] == None:
            p_result.pop()

    return p_result

#############绘图开始###############



############动图开始################

#######构造开始帧函数

def init():

    ####1#####第一支队球员
    x_1 = info.x_loc[1:6]
    y_1 = info.y_loc[1:6]
    matrix= [x_1,y_1]
    z_1 = list(zip(*matrix))
    n_1 = info.player_jersey[1:6]
    #利用边界函数寻找作为边界的点
    z_1 = graham_scan(z_1)
    t_1 = len(z_1)
    z_1.append(z_1[0])
    #需计算此时有几个边界点！重复元素没有计入len中。
    verts = z_1
    
    
    #codes根据verts的数量而定
    codes = [Path.MOVETO]+ [Path.LINETO]*(t_1-1)+ [Path.CLOSEPOLY]
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor='yellow', alpha=0.5, lw=2)
    ax.add_patch(patch)
    
    
    ####2#####第二支队球员
    x_2 = info.x_loc[6:11]
    y_2 = info.y_loc[6:11]
    matrix= [x_2,y_2]
    z_2 = list(zip(*matrix))
    n_2 = info.player_jersey[6:11]
    #利用边界函数寻找作为边界的点
    z_2 = graham_scan(z_2)
    t_2 = len(z_2)
    z_2.append(z_2[0])
    verts = z_2
    
    
    
    codes = [Path.MOVETO]+ [Path.LINETO]*(t_2-1)+ [Path.CLOSEPOLY]
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor='blue', alpha=0.5, lw=2)
    ax.add_patch(patch)
    
    #散点图画在上层
    plt.scatter(x_1, y_1, c='green', s=60)
    plt.scatter(x_2, y_2, c='red', s=60)
    ####3#####球
    x_3 = info.x_loc[0:1]
    y_3 = info.y_loc[0:1]
    ax.scatter(x_3, y_3, c='black', s=30)


#########构造自定义动画函数animate，用来更新每一帧，参数表示第i帧：

def animate(i):
    ####1#####第一支队球员
    ax.cla()
    court = plti.imread("fullcourt.png")
    plt.imshow(court, zorder=0, extent=[-5,100,55,-5])
    x_1 = info.x_loc[11*i+1:11*i+6]
    y_1 = info.y_loc[11*i+1:11*i+6]
    matrix= [x_1,y_1]
    z_1 = list(zip(*matrix))
    
    #利用边界函数寻找作为边界的点
    z_1 = graham_scan(z_1)
    t_1 = len(z_1)
    z_1.append(z_1[0])
    
    
    verts = z_1
    codes = [Path.MOVETO]+ [Path.LINETO]*(t_1-1)+ [Path.CLOSEPOLY]
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor='yellow', alpha=0.5, lw=2)
    ax.add_patch(patch)
    ####2#####第二支队球员
    x_2 = info.x_loc[11*i+6:11*i+11]
    y_2 = info.y_loc[11*i+6:11*i+11]
    matrix= [x_2,y_2]
    z_2 = list(zip(*matrix))
    
    #利用边界函数寻找作为边界的点
    z_2 = graham_scan(z_2)
    t_2 = len(z_2)
    z_2.append(z_2[0])
    
    
    verts = z_2
    codes = [Path.MOVETO]+ [Path.LINETO]*(t_2-1)+ [Path.CLOSEPOLY]
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor='blue', alpha=0.5, lw=2)
    ax.add_patch(patch)
    
    plt.scatter(x_1, y_1, c='green', s=60)
    plt.scatter(x_2, y_2, c='red', s=60)
        ####3#####球
    x_3 = info.x_loc[11*i:11*i+1]
    y_3 = info.y_loc[11*i:11*i+1]
    ax.scatter(x_3, y_3, c='black', s=30)



#动画 interval更新频率，frame总帧数
anim = animation.FuncAnimation(fig=fig, func=animate, init_func=init, frames=500, interval=40, blit=False)


#保存为mp4 fps每秒25帧
anim.save('animation.mp4', fps=None, extra_args=['-vcodec', 'libx264'])










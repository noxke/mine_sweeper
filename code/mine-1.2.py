"""
扫雷v1.2，预期解决清空空白格子问题，加入游戏胜利判断
"""
#判断地图的列数a和行数b（不一定需要调用）
"""def map_size(map):
    a = 0
    b = 0
    for key in map:
        if (key[0] == 0) & (key[1] == 0):
            a += 1
            b += 1
        elif key[0] == 0:
            a += 1
        elif key[1] == 0:
            b += 1
    return(a,b)
"""

import random
import os

#创建a*b大小地图，c个地雷
def create_map(a,b,c):
    ismine = False #是否为地雷
    tag = 0 #标记（0为未标记，1为插旗，2为问号,3为已点击）
    state = 0 #周围地雷个数
    map = {}
    for i in range(b):
        for j in range(a):
            map[(i,j)] = [ismine,tag,state]
    #随机生成c个地雷
    count = 0
    while count < c:
        i = random.randint(0,b - 1)
        j = random.randint(0,a - 1)
        if not map[(i,j)][0]:
            map[(i,j)][0] = True
            count += 1
    return(map)

#清空屏幕
def clear():
    if os.name == 'nt':
        i = os.system('cls')
    else:
        i = os.system('clear')

#判断地雷图标
def mine(mine):
    if mine[1] == 0:
        return(' ')
    elif mine[1] == 1:
        return('~')
    elif mine[1] == 2:
        return('?')
    elif (not mine[0]) & (mine[1] == 3):
        return(str(mine[2]))
    else:
        return(' ')

#打印地图
def show_map(map):
    clear() #清空屏幕
    #打印a*b大小地图
    print('#' * 3,end='')
    for j in range(a):
        print("#  {:02d}  ".format(j + 1),end='')
    print('#')
    print('#' * (7 * a + 4))
    for i in range(b):
        print("{:02d}".format(i + 1),end=' ')
        for j in range(a):
            print("#  {}{}  ".format(mine(map[(i,j)]),mine(map[(i,j)])),end='')
        print('#')
        print("{:02d}".format(i + 1),end=' ')
        for j in range(a):
            print("#  {}{}  ".format(mine(map[(i,j)]),mine(map[(i,j)])),end='')
        print('#')
        print('#' * (7 * a + 4))

#判断周围地雷个数
def count_mine(map):
    for key in map:
        count = 0
        for i in range(key[0] - 1,key[0] + 2):
            if (i == -1) | (i == a):
                continue
            for j in range(key[1] - 1,key[1] + 2):
                if (j == -1) | (j == b) | ((i,j) == key):
                    continue
                elif map[(i,j)][0]:
                    count += 1
        map[key][2] = count
    return(map)

#点中空白时清空周围
def clear_around(map,key):
    for key in map:
        for i in range(key[0] - 1,key[0] + 2):
            if (i == -1) | (i == a):
                continue
            for j in range(key[1] - 1,key[1] + 2):
                if (j == -1) | (j == b) | ((i,j) == key):
                    continue
                elif (map[(i,j)][2] == 0) & (map[(i,j)][1] == 0):
                    map[(i,j)][1] = 3
                    map = clear_around(map,(i,j))
                elif (map[(i,j)][1] == 0):
                    map[(i,j)][1] = 3
    return(map)

#点击功能
def click(i,j,map):
    if map[(i - 1,j - 1)][0]:
        #失败，游戏结束
        print("你点中了地雷")
        end()        
    elif map[(i - 1,j - 1)][1] == 3:
        #提醒重复点击
        print("重复点击")
    else:
        map[(i - 1,j - 1)][1] = 3
        if (map[(i - 1,j - 1)][2] == 0):
            map = clear_around(map,(i - 1,j - 1))
    return(map)

#开始程序
def start():
    while True:
        string = input("输入地图大小(形如5x5)：")
        a = string.split('x',2)[0]
        b = string.split('x',2)[1]
        a = int(a)
        b = int(b)
        c = int(input("请输入地雷个数："))
        if c >= a * b:
            print("地雷个数过多，请确保地雷个数小于总格数")
            continue
        else:
            break
    return(a,b,c)

#游戏程序
def game(map):
    show_map(map)
    print(map)
    map = count_mine(map)
    print(map)
    while True:
        string = input("输入要操作的格子坐标(形如4,3),输入q退出游戏:")
        if string == 'q':
            print("游戏已退出")
            break
        try:
            i = string.split(',',2)[0]
            j = string.split(',',2)[1]
            i = int(i)
            j = int(j)
        except:
            print("输入格式错误，请重新输入:")
        if (i <= 0) | (j <= 0) | (i > a) | (j > b):
            print("输入错误，请重新输入:")
            continue
        else:
            act = input("请确定要进行的操作，输入1进行点击操作，输入2进行~标记，输入3进行?标记，输入其他重新选择:")
            if act == '1':
                map = click(i,j,map)
            elif act == '2':
                map[(i,j)][1] = 1
            elif act == '3':
                map[(i,j)][1] = 2
            else:
                continue
            show_map(map)
            print(map)
    end()

#游戏结束
def end():
    print("游戏结束！")
    exit()

a,b,c = start()
map = create_map(a,b,c)
game(map)
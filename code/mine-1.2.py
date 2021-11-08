"""
扫雷v1.2，解决清空空白格子问题，加入游戏胜利判断
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
    elif (mine[0]) & (mine[1] == 3):
        return('*')
    else:
        return(' ')

#打印地图
def show_map(map):
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
            if (i < 0) | (i > b - 1):
                continue
            for j in range(key[1] - 1,key[1] + 2):
                if (j < 0) | (j > a - 1) | ((i,j) == key):
                    continue
                elif map[(i,j)][0]:
                    count += 1
        map[key][2] = count
    return(map)

#点中空白时清空周围
def clear_around(map,key):
    for keys in [(key[0] - 1,key[1] - 1),(key[0] - 1,key[1]),(key[0] - 1,key[1] + 1),(key[0],key[1] - 1),\
                (key[0],key[1] + 1),(key[0] + 1,key[1] - 1),(key[0] + 1,key[1]),(key[0] + 1,key[1] + 1)]:
            if (keys[0] < 0) | (keys[1] < 0) | (keys[0] >= a) | (keys[1] >= b):
                continue
            elif (map[keys][2] == 0) & (not map[keys][0]) & (map[keys][1] == 0):
                map[keys][1] = 3
                map = clear_around(map,keys)
            elif (not map[keys][0]) & (map[keys][1] == 0):
                map[keys][1] = 3
    return(map)

#点击功能
def click(i,j,map):
    global tip
    if map[(i,j)][0]:
        #失败，游戏结束
        clear()
        print("你点中了地雷")
        end(False,map)        
    elif map[(i,j)][1] == 3:
        #提醒重复点击
        tip = "请勿重复点击！"
    else:
        map[(i,j)][1] = 3
        if (map[(i,j)][2] == 0):
            map = clear_around(map,(i,j))
    return(map)

#开始程序
def start():
    while True:
        try:
            string = input("输入地图大小(形如5x5)：")
            a = string.split('x',2)[0]
            b = string.split('x',2)[1]
            a = int(a)
            b = int(b)
            c = int(input("请输入地雷个数："))
        except:
            print("输入错误！")
            continue
        if c >= a * b:
            print("地雷个数过多，请确保地雷个数小于总格数")
            continue
        else:
            break
    return(a,b,c)

#游戏程序
def game(map):
    global tip
    while True:
        clear()
        win(map)
        show_map(map)
        print(tip)
        tip = ''
        try:
            string = input("输入要操作的格子坐标(形如4,3),输入q退出游戏:")
            j = string.split(',',2)[0]
            i = string.split(',',2)[1]
            i = int(i) - 1
            j = int(j) - 1
        except:
            if string == 'q':
                clear()
                print("游戏已退出")
                end(False,map)
            else:
                tip = "输入格式错误，请重新输入:"
            continue
        if (i < 0) | (j < 0) | (i > b - 1) | (j > a - 1):
            tip = "输入错误，请重新输入:"
            continue
        else:
            act = input("请确定要进行的操作，输入1进行点击操作，输入2进行~标记，输入3进行?标记，输入4取消先前标记，输入其他重新选择:")
            if act == '1':
                map = click(i,j,map)
            #标记功能
            elif (act == '2') & (map[i,j][1] != 3):
                map[(i,j)][1] = 1
            elif (act == '3') & (map[i,j][1] != 3):
                map[(i,j)][1] = 2
            elif (act == '4') & (map[i,j][1] != 3) & (map[i,j][1] != 0):
                map[(i,j)][1] = 0
            elif (act == '4') & (map[i,j][1] == 0):
                tip = "该位置未标记！"
                continue
            elif map[i,j][1] == 3:
                tip = "请勿重复标记！"
            else:
                continue
    end()

#游戏结束
def end(i,map):
    for keys in map:
        map[keys][1] = 3
    show_map(map)
    if i:
        print("恭喜你胜利了！")
        print("感谢您的游玩！")
    else:
        print("很抱歉，你失败了！")
        print("感谢您的游玩！")
    os.system("pause")
    exit()

#判断胜利
def win(map):
    count = 0
    for keys in map:
        if (not map[keys][0]) & (map[keys][1] == 3):
            count += 1
    if count == a * b - c:
        print("你已找出所有地雷！")
        end(True,map)


tip = '********py扫雷 v1.2********\n游戏胜利条件：\n当所有非地雷的方格均被点开。\n****游戏解释权归xke所有****'
print(tip)
a,b,c = start()
map = create_map(a,b,c)
map = count_mine(map)
game(map)
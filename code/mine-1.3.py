"""
扫雷v1.3
以彩色方式输出，增加再次游戏选项,加入第二个地图模板，重新优化程序结构
"""

import random
import os

#创建a*b大小地图，c个地雷
def create_map():
    global map
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

#判断周围地雷个数
def count_mine():
    global map
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

#判断地雷图标
def mine(mine):
    if type == 1:
        if mine[1] == 0:
            return('\033[0;37;47m {} \033[0m'.format('  '))
        elif mine[1] == 1:
            return('\033[0;31;47m {} \033[0m'.format('~~'))
        elif mine[1] == 2:
            return('\033[0;30;47m {} \033[0m'.format('??'))
        elif (not mine[0]) & (mine[1] == 3):
            if (mine[2] >= 0) & (mine[2] <= 2):
                return('\033[0;32;47m {} \033[0m'.format(str(mine[2]) * 2))
            elif (mine[2] == 3) | (mine[2] == 4):
                return('\033[0;36;47m {} \033[0m'.format(str(mine[2]) * 2))
            elif (mine[2] == 5) | (mine[2] == 6):
                return('\033[0;34;47m {} \033[0m'.format(str(mine[2]) * 2))
            else:
                return('\033[0;35;47m {} \033[0m'.format(str(mine[2]) * 2))
        elif (mine[0]) & (mine[1] == 3):
            return('\033[0;30;41m {} \033[0m'.format('**'))
        else:
            return('\033[0;37;47m {} \033[0m'.format('  '))
    elif type == 2:
        if mine[1] == 0:
            return('\033[0;37;47m{}\033[0m'.format('  '))
        elif mine[1] == 1:
            return('\033[0;31;47m{}\033[0m'.format('~~'))
        elif mine[1] == 2:
            return('\033[0;30;47m{}\033[0m'.format('??'))
        elif (not mine[0]) & (mine[1] == 3):
            if (mine[2] >= 0) & (mine[2] <= 2):
                return('\033[0;32;47m{}\033[0m'.format(str(mine[2]) * 2))
            elif (mine[2] == 3) | (mine[2] == 4):
                return('\033[0;36;47m{}\033[0m'.format(str(mine[2]) * 2))
            elif (mine[2] == 5) | (mine[2] == 6):
                return('\033[0;34;47m{}\033[0m'.format(str(mine[2]) * 2))
            else:
                return('\033[0;35;47m{}\033[0m'.format(str(mine[2]) * 2))
        elif (mine[0]) & (mine[1] == 3):
            return('\033[0;30;41m{}\033[0m'.format('**'))
        else:
            return('\033[0;37;47m{}\033[0m'.format('  '))

#打印地图(添加第二布局)
def show_map():
    if type == 1:
        print('#' * 3,end='')
        for j in range(a):
            print("#  {:02d}  ".format(j + 1),end='')
        print('#')
        print('#' * (7 * a + 4))
        for i in range(b):
            print("{:02d}".format(i + 1),end=' ')
            for j in range(a):
                print("# {} ".format(mine(map[(i,j)])),end='')
            print('#')
            print("{:02d}".format(i + 1),end=' ')
            for j in range(a):
                print("# {} ".format(mine(map[(i,j)])),end='')
            print('#')
            print('#' * (7 * a + 4))
    elif type == 2:
        print('#' * 2,end='')
        for j in range(a):
            print("#{:02d}".format(j + 1),end='')
        print('#')
        print('#' * (3 * a + 3))
        for i in range(b):
            print("{:02d}".format(i + 1),end='')
            for j in range(a):
                print("#{}".format(mine(map[(i,j)])),end='')
            print('#')
            print('#' * (3 * a + 3))

#点中空白时清空周围
def clear_around(key):
    global map
    for keys in [(key[0] - 1,key[1] - 1),(key[0] - 1,key[1]),(key[0] - 1,key[1] + 1),(key[0],key[1] - 1),\
                (key[0],key[1] + 1),(key[0] + 1,key[1] - 1),(key[0] + 1,key[1]),(key[0] + 1,key[1] + 1)]:
            if (keys[0] < 0) | (keys[1] < 0) | (keys[0] >= b) | (keys[1] >= a):
                continue
            elif (map[keys][2] == 0) & (not map[keys][0]) & (map[keys][1] == 0):
                map[keys][1] = 3
                clear_around(keys)
            elif (not map[keys][0]) & (map[keys][1] == 0):
                map[keys][1] = 3

#点击功能
def click(i,j):
    global tip,map
    if map[(i,j)][0]:
        #失败，游戏结束
        tip = "你点中了地雷！"
        end(False,map)        
    elif map[(i,j)][1] == 3:
        #提醒重复点击
        tip = "请勿重复点击！"
    else:
        map[(i,j)][1] = 3
        if (map[(i,j)][2] == 0):
            clear_around((i,j))

#清空屏幕
def clear():
    if os.name == 'nt':
        i = os.system('cls')
    else:
        i = os.system('clear')

#开始程序
def start():
    global a,b,c,type
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
    map_type()
    inputting = input("请选择地图模式，输入1为模式一，输入2为模式二\n其他操作由游戏默认\n地图大于25x20时建议使用模式二：")
    if inputting == '1':
        type = 1
    elif inputting == '2':
        type = 2
    else:
        if (a <=25) & (b <= 20):
            type = 1
        else:
            type = 2

def map_type():
    print("地图模式一".center(35,' '))
    print("####  01  #  02  #  03  #  04  #  05  #")
    print("#######################################")
    print("01 #      #      #      #      #      #")
    print("01 #      #      #      #      #      #")
    print("#######################################")
    print("02 #      #      #      #      #      #")
    print("02 #      #      #      #      #      #")
    print("#######################################")
    print("03 #      #      #      #      #      #")
    print("03 #      #      #      #      #      #")
    print("#######################################")
    print("04 #      #      #      #      #      #")
    print("04 #      #      #      #      #      #")
    print("#######################################")
    print("05 #      #      #      #      #      #")
    print("05 #      #      #      #      #      #")
    print("#######################################")
    print("\n")
    print("地图模式二".center(35,' '))
    print("###01#02#03#04#05#06#07#08#09#10#11#12#")
    print("#######################################")
    print("01#  #  #  #  #  #  #  #  #  #  #  #  #")
    print("#######################################")
    print("02#  #  #  #  #  #  #  #  #  #  #  #  #")
    print("#######################################")
    print("03#  #  #  #  #  #  #  #  #  #  #  #  #")
    print("#######################################")
    print("04#  #  #  #  #  #  #  #  #  #  #  #  #")
    print("#######################################")
    print("05#  #  #  #  #  #  #  #  #  #  #  #  #")
    print("#######################################")
    print("06#  #  #  #  #  #  #  #  #  #  #  #  #")
    print("#######################################")
    print("07#  #  #  #  #  #  #  #  #  #  #  #  #")
    print("#######################################")

#游戏程序
def game():
    global tip,map
    while True:
        clear()
        win()
        show_map()
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
                tip = "游戏已退出"
                end(False)
            else:
                tip = "输入格式错误，请重新输入:"
            continue
        if (i < 0) | (j < 0) | (i > b - 1) | (j > a - 1):
            tip = "输入错误，请重新输入:"
            continue
        else:
            act = input("请确定要进行的操作，输入1进行点击操作，输入2进行~标记，输入3进行?标记，输入4取消先前标记，输入其他重新选择:")
            if act == '1':
                click(i,j)
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

#判断胜利
def win():
    global tip
    count = 0
    for keys in map:
        if (not map[keys][0]) & (map[keys][1] == 3):
            count += 1
    if count == a * b - c:
        tip = "你已找出所有地雷！"
        end(True)

#游戏结束
def end(i):
    global tip,map
    for keys in map:
        map[keys][1] = 3
    clear()
    show_map()
    print(tip)
    if i:
        print("恭喜你胜利了！")
        print("感谢您的游玩！")
    else:
        print("很抱歉，你失败了！")
        print("感谢您的游玩！")
    string = input("是否重新开始游戏？输入1或y重新开始，其他操作退出游戏：")
    if (string == '1') | (string == 'y'):
        main()
    else:
        exit()

#主程序
def main():
    clear()
    global a,b,c,map,tip
    tip = '********py扫雷 v1.3********\n游戏胜利条件：\n当所有非地雷的方格均被点开。\n****游戏解释权归xke所有****'
    print(tip)
    start()
    tip = ''
    create_map()
    count_mine()
    game()



a,b,c,map,tip,type = 0,0,0,{},'',1
main()
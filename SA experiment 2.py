import math
import random
import numpy as np
from math import e
from math import exp
import matplotlib.pyplot as plt
import xlwt

city_loc = [[6734,1453],[2233,10],[5530,1424],[401,841],[3082,1644],[7608,4458],[7573,3716],[7265,1268],[6898,1885],
                 [1112,2049],[5468,2606],[5989,2873],[4706,2674],[4612,2035],[6347,2683],[6107,669],[7611,5184],[7462,3590],
                 [7732,4723],[5900,3561],[4483,3369],[6101,1110],[5199,2182],[1633,2809],[4307,2322],[675,1006],[7555,4819],
                 [7541,3981],[3177,756],[7352,4506],[7545,2801],[3245,3305],[6426,3173],[4608,1198],[23,2216],[7248,3779],
                 [7762,4595],[7392,2244],[3484,2829],[6271,2135],[4985,140],[1916,1569],[7280,4899],[7509,3239],[10,2676],
                 [6807,2993],[5185,3258],[3023,1942]]
T0 = 50000      #初始温度
T_end = 15      #结束温度
q = 0.98        #降温系数
L = 1000        #迭代次数

#两个城市的距离
def dist(a, b):
    x1 = city_loc[a][0]
    x2 = city_loc[b][0]
    y1 = city_loc[a][1]
    y2 = city_loc[b][1]
    distance = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
    return distance
#路程总长
def totaldistance(a):
    value = 0
    for j in range(47):
        value += dist(a[j], a[j + 1])
    value += dist(a[47], a[0])
    return value

#初始化一个解 [0,1,2,3..48]
def init_ans():
    ans = []
    for i in range(48):
        ans.append(i)
    return ans
#产生新解
def creat_new(ans_before):
    ans_after = []
    for i in range(len(ans_before)):
        ans_after.append(ans_before[i])
    cuta = random.randint(0,47)
    cutb = random.randint(0,47)
    ans_after[cuta], ans_after[cutb] = ans_after[cutb], ans_after[cuta]
    return ans_after

def SA():
    ans0 =init_ans()    #产生初始路径
    T = T0              #当前温度等于初始温度
    cnt = 0             #计数器
    trend = []          #
    while T > T_end:    #如果当前温度大于终止温度
        for i in range(L):#循环L次
            newans = creat_new(ans0)    #扰动产生新路径
            old_dist = totaldistance(ans0)  #计算旧路径的长度
            new_dist = totaldistance(newans)#计算新路径的长度
            df = new_dist - old_dist        #判断大小
            if df >= 0:                     #如果新路径长度大于旧路径长度
                rand = random.uniform(0,1)  #以一定的概率接受
                if rand < math.exp(-df/T):
                    ans0 = newans
            else:
                ans0 = newans
        T = T * q       #降温
        cnt += 1        #计数器
        now_dist = totaldistance(ans0)      #当前路径长度
        trend.append(now_dist)              #把当前路径长度加入“趋势”列表
        # print(cnt,"次降温，温度为：",T," 路程长度为：", now_dist)   #报文
    distance = totaldistance(ans0)      #ans0保存最佳路径，distance保存最短长度
    print(distance, ans0)
    plt.plot(trend)
    plt.savefig("D:\demo\demo4\SA experiment2 A single run")
    return distance,ans0

if __name__ == '__main__':
    distance_list = []
    ans0_list = []
    work_book = xlwt.Workbook(encoding='utf-8')
    sheet = work_book.add_sheet('25次迭代最优值')
    sheet.write(0, 0, '迭代次数')
    sheet.write(0, 1, '最优值')
    for i in range(5):
        distance,ans0 = SA()
        distance_list.append(distance)
        ans0_list.append(ans0)
        sheet.write(i+1,0,str(i+1))
        sheet.write(i+1,1,distance)
        sheet.write(i + 1, 2,str(ans0))
    work_book.save('SA experment2.xls')
    plt.clf()
    plt.plot(distance_list)
    plt.savefig("D:\demo\demo4\SA experiment 2 optimal distance chart")
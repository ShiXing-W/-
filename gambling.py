import math
from heapq import nlargest
from scipy.optimize import linear_sum_assignment
import random
import copy
import numpy as np
import matplotlib.pyplot as plt

A_v=1 #AGV速度
class _Gambling():
    def __init__(self, Pool,F,t,T):
        self.Pool=Pool  #任务池即决策选择
        self.F=F    #局中人
        self.t = t  # 当前时间
        self.T = T  # 当前时间

    def Earning(self,agvNo):    #计算收益
        earns={}    #收益字典
        for key in self.Pool.keys():   #遍历任务池中的任务
            if self.Pool[key].expectTime-self.t<0:
                earn = 1*(abs(self.F[agvNo].position[0] - self.Pool[key].start[0]) + abs(self.F[agvNo].position[1] - self.Pool[key].start[1])) // A_v\
                       +1*(abs(self.Pool[key].expectTime - self.t - (abs(self.F[agvNo].position[0] - self.Pool[key].start[0])
                                                                     + abs(self.F[agvNo].position[1] - self.Pool[key].start[1])) // A_v))
            else:
                earn=1*(abs(self.F[agvNo].position[0]-self.Pool[key].start[0])+abs(self.F[agvNo].position[1]-self.Pool[key].start[1]))//A_v+\
                     1*(self.Pool[key].expectTime-self.t-(abs(self.F[agvNo].position[0]-self.Pool[key].start[0])
                                                          +abs(self.F[agvNo].position[1]-self.Pool[key].start[1]))//A_v)
            earns[key]=earn
        return earns
    # def Earning(self,agvNo):    #迭代贪婪
    #     earns={}    #记录最好解和当前解
    #     for key in self.Pool.keys():   #遍历任务池中的任务
    #         earn=3*(abs(self.F[agvNo].position[0]-self.Pool[key].start[0])+abs(self.F[agvNo].position[1]-self.Pool[key].start[1]))//A_v
    #         # +7*(abs(self.Pool[key].expectTime-self.t-(abs(self.F[agvNo].position[0]-self.Pool[key].start[0])+abs(self.F[agvNo].position[1]-self.Pool[key].start[1]))//A_v))
    #         earns[key]=earn
    #     return earns

    def topn_dict(d, n):    #找出字典中最大前几个的键值
        return nlargest(n, d, key=lambda k: d[k])  # 注：这里lambda k: d[k]的用法

    def Game(self):
        allEarns={}     #所有局中人的收益集合
        allEarn=[]      #所有局中人的收益矩阵
        for key in self.F.keys():
            allEarns[key]=self.Earning(key)
        for key in self.F.keys():
            earn=[]
            for i in allEarns[key].values():
                earn.append(i)
            allEarn.append(earn)
        allEarn=np.array(allEarn)
        row_ind, col_ind = linear_sum_assignment(allEarn)
        for n in range(len(row_ind)):
            no=list(allEarns.keys())[n]
            tno = list(allEarns[no].keys())[col_ind[n]]
            self.T[tno].done = 1
            self.T[tno].responTime = self.t
            self.F[no].currentTasks.append(tno)
            self.F[no].allTasks.append(tno)
            self.F[no].emptyLine += (abs(self.F[no].position[0] - self.T[tno].start[0]) + abs(self.F[no].position[1] - self.T[tno].start[1])) // A_v
            self.F[no].cost=self.F[no].cost+allEarn[n][n]
            if len(self.F[no].currentTasks)==1:
                self.T[tno].startTime=self.t+(abs(self.F[no].position[0] - self.T[tno].start[0])
                                              + abs(self.F[no].position[1] - self.T[tno].start[1]))//A_v
                self.T[tno].endTime = self.T[tno].startTime+self.T[tno].distance//A_v
                self.F[no].endTime.append(self.T[tno].endTime)
                self.F[no].position = self.T[tno].end
            else:
                self.T[tno].startTime=self.F[no].endTime[-1]+(abs(self.F[no].position[0] - self.T[tno].start[0])
                                                              + abs(self.F[no].position[1] - self.T[tno].start[1]))//A_v
                self.T[tno].endTime = self.T[tno].startTime+self.T[tno].distance//A_v
        return self.F,self.T

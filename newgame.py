import pandas as pd
from collections import Counter
from copy import deepcopy
import taskResource
from gambling import _Gambling
import matplotlib.pyplot as plt
from pylab import *
from random import sample
import requests
import openpyxl
import xlsxwriter
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
mpl.rc("font",family='YouYuan')
#region 配送单元、工位等类
class Agv:
	def __init__(self):
		# AGV编号
		self.no =0
		# AGV当前任务队列
		self.currentTasks = []
		# AGV下一任务队列
		self.nextTasks = []
		# AGV所有任务队列
		self.allTasks = []
		#任务队列中各个任务完成时间
		self.endTime=[]
		# AGV当前位置
		self.position = []
		# AGV行驶距离
		self.journey =0
		# AGV空行时间
		self.emptyLine =0
		# AGV空闲时间
		self.emptyTime =0
		# AGV收益
		self.cost =0

class Task:
	def __init__(self):
		# 任务编号
		self.no =0
		# 任务起始点位置
		self.start = []
		# 任务终点位置
		self.end = []
		# 任务开始时间
		self.startTime=0
		# 任务结束时间
		self.endTime=0
		# 任务期望结束时间
		self.expectTime = 0
		#任务距离
		self.distance=0
		# 任务状态，0是待分配，1是已分配
		self.done = 0
		# 响应时间
		self.responTime = 0
		# 响应时间
		self.generateTime = 0
#endregion
T=taskResource.taskinput()
#region 初始化参数
#AGV数量
A_num=12
#AGV速度
A_v=1
#endregion

#region 工位、任务等初始化
A={}	#AGV集合
T3={}
#创建对象加入集合并初始化属性
for n in range(1, A_num + 1):	#AGV对象
	A[n]=Agv()
	A[n].position=[20,50]
	A[n].no=n
for n in range(1, A_num + 1):	#初始给AGV分配任务
	A[n].currentTasks.append("DT"+str(n))
	A[n].allTasks.append("DT"+str(n))
	A[n].endTime.append((T["DT"+str(n)].distance//A_v)+(abs(A[n].position[0]-T["DT"+str(n)].start[0])
														+abs(A[n].position[1]-T["DT"+str(n)].start[1]))//A_v+T["DT"+str(n)].generateTime)
	A[n].emptyLine+=(abs(A[n].position[0]-T["DT"+str(n)].start[0])+abs(A[n].position[1]-T["DT"+str(n)].start[1]))//A_v
	A[n].position=T["DT"+str(n)].end
	T["DT"+str(n)].done=1
	T["DT"+str(n)].endTime=A[n].endTime[-1]
	T["DT"+str(n)].startTime=T["DT"+str(n)].endTime-T["DT"+str(n)].distance//A_v+T["DT"+str(n)].generateTime
	T["DT"+str(n)].responTime=T["DT"+str(n)].generateTime
#endregion

T1=deepcopy(T)	#方法一任务
T2=deepcopy(T)	#方法二任务
A1=deepcopy(A)	#方法一AGV
A2=deepcopy(A)	#方法二AGV
T3=deepcopy(T)	#方法三任务
A3=deepcopy(A)	#方法三AGV

#region		模拟时间
for t in range(1,45000):
	# 方法一更新任务状态
	for i in T1.keys():
		if T1[i].generateTime==t and T1[i].done==2:
			T1[i].done = 0
	# 方法二更新任务状态
	for i in T2.keys():
		if T2[i].generateTime==t and T2[i].done==2:
			T2[i].done = 0
	# # 方法三更新任务状态
	# for i in T3.keys():
	# 	if T3[i].generateTime==t and T3[i].done==2:
	# 		T3[i].done = 0
	for i in range(1, A_num + 1):	#对AGV状态进行判断
		# 方法一更新AGV
		if A1[i].endTime[-1]==t:		#对部分AGV和任务状态进行更改
			if len(A1[i].currentTasks) != 0:
				del A1[i].currentTasks[0]
			if len(A1[i].currentTasks) != 0:
				A1[i].endTime.append(T1[A1[i].currentTasks[0]].endTime)
				A1[i].position = T1[A1[i].currentTasks[0]].end
		# 方法二更新AGV
		if A2[i].endTime[-1]==t:		#对部分AGV和任务状态进行更改
			if len(A2[i].currentTasks) != 0:
				del A2[i].currentTasks[0]
		# # 方法三更新AGV
		# if A3[i].endTime[-1]==t:		#对部分AGV和任务状态进行更改
		# 	if len(A3[i].currentTasks) != 0:
		# 		del A3[i].currentTasks[0]
		# 	if len(A3[i].currentTasks) != 0:
		# 		A3[i].endTime.append(T3[A3[i].currentTasks[0]].endTime)
		# 		A3[i].position = T3[A3[i].currentTasks[0]].end

	F1={}	#实验组在t时刻响应的AGV集合
	Pool1={}	#实验组在t时刻任务池
	F2={}	#对照组在t时刻响应的AGV集合
	Pool2={}	#对照组在t时刻响应的AGV集合
	F3={}	#对照组在t时刻响应的AGV集合
	Pool3={}	#对照组在t时刻响应的AGV集合
	for k in range(1,A_num+1):	#找出t时刻响应的AGV
		if len(A1[k].currentTasks)<=1:
			F1[k]=A1[k]
		if len(A2[k].currentTasks)==0:
			F2[k]=A2[k]
		if len(A3[k].currentTasks)<=1:
			F3[k]=A3[k]
	for key in T1.keys():	#找出t时刻可响应的任务
		if T1[key].done==0:
			Pool1[key]=T1[key]
	for key in T2.keys():	#找出t时刻可响应的任务
		if T2[key].done == 0:
			Pool2[key] = T2[key]
	for key in T3.keys():	#找出t时刻可响应的任务
		if T3[key].done == 0 and (T3[key].expectTime-t)<540:
			Pool3[key] = T3[key]
	# 方法一调度
	if len(F1)!=0 and len(Pool1)!=0:
		gambling=_Gambling(Pool1,F1,t,T1,)	#迭代贪婪/博弈
		F,T=gambling.Game()
		for key in F.keys():
			A1[key]=F[key]
		for key in T.keys():
			T1[key]=T[key]
	# 方法二调度
	if len(F2)!=0 and len(Pool2)!=0:
		gambling1=_Gambling(Pool2,F2,t,T2,)
		F,T=gambling1.Game()
		for key in F.keys():
			A2[key]=F[key]
		for key in T.keys():
			T2[key]=T[key]
	# 方法三调度
	if len(F3)!=0 and len(Pool3)!=0:
		gambling=_Gambling(Pool3,F3,t,T3,)	#迭代贪婪/博弈
		F,T=gambling.Game()
		for key in F.keys():
			A3[key]=F[key]
		for key in T.keys():
			T3[key]=T[key]

# #region 	画甘特图
#
# fontdict_time = {
# 	"family": "Microsoft YaHei",
# 	"style": "oblique",
# 	"color": "black",
# 	"size": 9
# }
# c = ['Orange', 'Gold', 'y', 'DarkSalmon', 'g', 'r']
# ylabels = []  # 生成y轴标签
# for k in range(1,A_num+1):
# 	for i in range(len(A1[k].allTasks)):
# 		plt.barh(1*k,width=T1[A1[k].allTasks[i]].distance//A_v,left=T1[A1[k].allTasks[i]].startTime,edgecolor="black", color=c[i%3])
# 		plt.text(T1[A1[k].allTasks[i]].startTime+2, k, A1[k].allTasks[i],fontdict=fontdict_time)
# 	ylabels.append("AGV" + str(k))
# plt.yticks(range(1,13), ylabels,fontsize=15)
# plt.xlabel("Time /s",fontsize=15)
# plt.ylabel("AGV",fontsize=15)
# plt.show()
# ylabels = []  # 生成y轴标签
# for k in range(1, A_num + 1):
# 	for i in range(len(A2[k].allTasks)):
# 		plt.barh(k, width=T2[A2[k].allTasks[i]].distance//A_v,left=T2[A2[k].allTasks[i]].startTime, edgecolor="black",color=c[i % 3])
# 		plt.text(T2[A2[k].allTasks[i]].startTime+2, k, A2[k].allTasks[i],fontdict=fontdict_time)
# 	ylabels.append("AGV" + str(k))
# plt.yticks(range(1,13), ylabels,fontsize=15)
# plt.xlabel("Time /s",fontsize=15)
# plt.ylabel("AGV")
# plt.show()
# Cmax1=0
# Cmax2=0
# W1=0
# W2=0
# Ca1=0
# Ca2=0
# n1=0
# n2=0
# task1=[]
# task2=[]
# for k in range(1,A_num+1):
# 	task1[0:0]=A1[k].allTasks
# 	task2[0:0]=A2[k].allTasks
# 	a=T1[A1[k].allTasks[-1]].endTime
# 	Ca1+=T1[A1[k].allTasks[-1]].endTime
# 	n1+=len(A1[k].allTasks)
# 	Ca2+=T2[A2[k].allTasks[-1]].endTime
# 	n2+=len(A2[k].allTasks)
# 	if a>=Cmax1:
# 		Cmax1=a
# 	b=T2[A2[k].allTasks[-1]].endTime
# 	if b>=Cmax2:
# 		Cmax2=b
# 	W1+=A1[k].emptyLine
# 	W2+=A2[k].emptyLine
# #endregion

#region		输出文档
for k in range(1, A_num + 1):
	for i in A1[k].allTasks:
		A1[k].journey+=T1[i].distance
	for i in A2[k].allTasks:
		A2[k].journey+=T2[i].distance
	for i in A3[k].allTasks:
		A3[k].journey+=T3[i].distance
t1=0
t2=0
t3=0
d1=0
d2=0
d3=0
datatask1=[]
for i in T1.keys():
	t=[]
	t.append(T1[i].no)
	t.append(T1[i].startTime)
	t.append(T1[i].endTime)
	for k in A1.keys():
		if i in A1[k].allTasks:
			t.append(k)
	t.append(T1[i].responTime)
	t.append(T1[i].expectTime-T1[i].endTime)
	t1=t1+(T1[i].expectTime-T1[i].endTime)
	datatask1.append(t)
df1 = pd.DataFrame(datatask1,columns=['任务编号','开始时间','结束时间','搬运agv编号','响应时间','期望完成时间差'])

datatask2=[]
for i in T2.keys():
	t=[]
	t.append(T2[i].no)
	t.append(T2[i].startTime)
	t.append(T2[i].endTime)
	for k in A2.keys():
		if i in A2[k].allTasks:
			t.append(k)
	t.append(T2[i].responTime)
	t.append(T2[i].expectTime-T2[i].endTime)
	t2 = t2 + (T2[i].expectTime - T2[i].endTime)
	datatask2.append(t)
df2 = pd.DataFrame(datatask2,columns=['任务编号','开始时间','结束时间','搬运agv编号','响应时间','期望完成时间差'])

datatask5=[]
for i in T3.keys():
	t=[]
	t.append(T3[i].no)
	t.append(T3[i].startTime)
	t.append(T3[i].endTime)
	for k in A3.keys():
		if i in A3[k].allTasks:
			t.append(k)
	t.append(T3[i].responTime)
	t.append(T3[i].expectTime-T3[i].endTime)
	t3=t3+(T3[i].expectTime-T3[i].endTime)
	datatask5.append(t)
df5 = pd.DataFrame(datatask5,columns=['任务编号','开始时间','结束时间','搬运agv编号','响应时间','期望完成时间差'])

datatask3=[]
for i in A1.keys():
	t=[]
	t.append(A1[i].no)
	t.append(A1[i].allTasks)
	t.append(T1[A1[i].allTasks[-1]].endTime-A1[i].journey//A_v-A1[i].emptyLine)
	t.append(A1[i].emptyLine)
	t.append(A1[i].journey)
	t.append(len(A1[i].allTasks))
	d1=d1+(A1[i].emptyLine)
	t.append(sum(A1[i].cost))
	datatask3.append(t)
df3 = pd.DataFrame(datatask3,columns=['agv编号','任务队列','空闲时间','空行时间','行驶距离','任务数','成本'])

datatask4=[]
for i in A2.keys():
	t=[]
	t.append(A2[i].no)
	t.append(A2[i].allTasks)
	t.append(T2[A2[i].allTasks[-1]].endTime-A2[i].journey//A_v-A2[i].emptyLine)
	t.append(A2[i].emptyLine)
	t.append(A2[i].journey)
	t.append(len(A2[i].allTasks))
	t.append(sum(A2[i].cost))
	d2 = d2 + (A2[i].emptyLine)
	datatask4.append(t)
df4 = pd.DataFrame(datatask4,columns=['agv编号','任务队列','空闲时间','空行时间','行驶距离','任务数','成本'])

datatask6=[]
for i in A3.keys():
	t=[]
	t.append(A3[i].no)
	t.append(A3[i].allTasks)
	t.append(T3[A3[i].allTasks[-1]].endTime-A3[i].journey//A_v-A3[i].emptyLine)
	t.append(A3[i].emptyLine)
	t.append(A3[i].journey)
	t.append(len(A3[i].allTasks))
	t.append(sum(A3[i].cost))
	d3=d3+(A3[i].emptyLine)
	datatask6.append(t)
df6 = pd.DataFrame(datatask6,columns=['agv编号','任务队列','空闲时间','空行时间','行驶距离','任务数','成本'])
print(t1,t2,t3,d1,d2,d3)
writer = pd.ExcelWriter('D:\\桌面\\demo\\第二组.xlsx',engine='xlsxwriter')
#分别将表df_one、df_two、df_three写入Excel中的Sheet1、Sheet2、Sheet3
# 并命名为表1、表2、表3
df1.to_excel(writer,sheet_name='表1',index=False)
df2.to_excel(writer,sheet_name='表2',index=False)
df5.to_excel(writer,sheet_name='表3',index=False)
df3.to_excel(writer,sheet_name='表4',index=False)
df4.to_excel(writer,sheet_name='表5',index=False)
df6.to_excel(writer,sheet_name='表6',index=False)
writer.close()
#endregion

# region	定义函数来显示柱状上的数值 作柱状图
# def autolabel(rects):
#     for rect in rects:
#         height = rect.get_height()
#         plt.text(rect.get_x()+rect.get_width()/2.-0.2, 1.03*height, '%s' % float(height))
# l1=[Cmax1, W1,n1]
# l2=[Cmax2, W2,n2]
# plt.rcParams['font.sans-serif'] = ['SimHei']
# name=['Max completion time','Empty row time','Total late/early time']
# total_width, n = 0.8, 2
# width = total_width / n
# x=[0,1,2]
# a=plt.bar(x, l1, width=width, label='gambling',fc = 'y')
# for i in range(len(x)):
# 	x[i] = x[i] + width
# b=plt.bar(x, l2, width=width, label="greedy",tick_label = name,fc = 'r')
# autolabel(a)
# autolabel(b)
# plt.xlabel('。。。')
# plt.ylabel('time/s')
# plt.title('')
# plt.legend()
# plt.show()
#endregion
# x=[]
# y=[]
# z=[]
# for i in range(len(A1[1].allTasks)):
# 	x.append(T1[A1[1].allTasks[i]].start[0])
# 	x.append(T1[A1[1].allTasks[i]].end[0])
# 	y.append(T1[A1[1].allTasks[i]].start[1])
# 	y.append(T1[A1[1].allTasks[i]].end[1])
# for k in range(len(x)):
# 	z.append(k+1)
# X=np.array(x)
# Y=np.array(y)
# Z=np.array(z)
# # 设置图例字号
# mpl.rcParams['legend.fontsize'] = 10
# fig = plt.figure()
# # 设置三维图形模式
# ax = fig.add_subplot(projection='3d')
# # 绘制图形
# ax.plot(X, Y, Z, label='parametric curve')
# # 显示图例
# ax.legend()
# # 显示图形
# plt.show()
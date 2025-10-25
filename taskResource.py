import matplotlib.pyplot as plt  #画图用
import numpy as np
import matplotlib
import xlrd  				#读Excel数据用
import random
file_location = "D:\桌面\demo\任务1.xls"
data = xlrd.open_workbook(file_location)
sheetTask = data.sheet_by_index(0)
# sheetPick = data.sheet_by_index(2)
# sheetStation = data.sheet_by_index(1)
# sheetWarehouse = data.sheet_by_index(3)
# dataWarehouse = [[sheetWarehouse.cell_value(r,c) for c in range(1,sheetWarehouse.ncols)] for r in range(2,sheetWarehouse.nrows)]
dataTask = [[sheetTask.cell_value(r,c) for c in range(1,sheetTask.ncols)] for r in range(1,sheetTask.nrows)]
# dataPick = [[sheetPick.cell_value(r,c) for c in range(1,sheetPick.ncols)] for r in range(2,sheetPick.nrows)]
# dataStation = [[sheetStation.cell_value(r,c) for c in range(1,sheetStation.ncols)] for r in range(2,sheetStation.nrows)]
class Station:
	def __init__(self):
		# 工位编号
		self.no =0
		# 工位位置
		self.position = []

class Pick:
	def __init__(self):
		# 取料点编号
		self.no =0
		# 取料点位置
		self.position = []

class Warehouse:
	def __init__(self):
		# 编号
		self.no =0
		# 位置
		self.position = []

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
		self.done = 2
		# 响应时间
		self.responTime = 0
		# 响应时间
		self.generateTime = 0

# S={}	#工位集合
T={}	#任务集合
# P={}	#取料点集合
# W={}    #半成品库集合

# for i in dataWarehouse:
#     no=i[0]
#     W[no] = Warehouse()
#     W[no].no = no
#     x = i[1]  # 横坐标
#     y = i[2]  # 纵坐标
#     W[no].position = [x, y]
# for i in dataPick:
#     no=i[0]
#     P[no] = Pick()
#     P[no].no = no
#     x = i[1]  # 横坐标
#     y = i[2]  # 纵坐标
#     P[no].position = [x, y]
# for i in dataStation:
#     no=i[0]
#     S[no] = Station()
#     S[no].no = no
#     x = i[1]  # 横坐标
#     y = i[2]  # 纵坐标
#     S[no].position = [x, y]
for i in dataTask:
    no=i[0]
    T[no] = Task()
    T[no].no = no
    T[no].done = 2
    T[no].start =[i[1],i[2]]
    T[no].end = [i[3],i[4]]
    # start=i[1]
    # end=i[2]
    # if start[0]=='S':
    #     T[no].start=S[start].position
    # if start[0]=='W':
    #     T[no].start=W[start].position
    # if start[0]=='P':
    #     T[no].start=P[start].position
    # if end[0]=='S':
    #     T[no].end=S[end].position
    # if end[0]=='W':
    #     T[no].end=W[end].position
    # if end[0]=='P':
    #     T[no].end=P[end].position
    T[no].distance = abs(T[no].start[0] - T[no].end[0]) + abs(T[no].start[1] - T[no].end[1])
    T[no].expectTime=i[6]
    T[no].generateTime=i[5]

# class Plus:
#     def __init__(self, T):
#         self.T = T
def taskinput():
    return T

def newtask():
    list=random.sample(range(21,3000),90)
    list.sort()
    return list
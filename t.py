# from heapq import nlargest
#
# # 返回字典d前n个最大值对应的键
# '''
# topn_dict(d,n)
#
# 参数：
#     d:字典
#     n：前几个数
#
# 思路：
#     利用nlargest(n,d)函数 简单说来就是找出最大的几行 注意是 最大 不可以是最小
#     n：表示行数
#     d：排序的依据
#     在这个例子中，d是一个字典，但是加了一个key值，使得排序
# '''
# def topn_dict(d, n):
#     return nlargest(n, d, key=lambda k: d[k])#注：这里lambda k: d[k]的用法暂不明白
# # ['a', 'd', 'c']
# print(topn_dict({'a': 10, 'b': 8, 'c': 9, 'd': 10}, 2))
#
# b=[1,2]
# del b[0]
# print(b )
# import numpy as np
# from scipy.optimize import linear_sum_assignment
# cost = np.array([[4, 1, 3],[5, 7, 9],[5, 7, 9]])
#
# row_ind, col_ind = linear_sum_assignment(cost)
# # col_ind
# # array([1, 0, 2])
# print(cost)
# print(row_ind, col_ind)
# cost[row_ind, col_ind].sum()
# import random
# def newtask():
#     list=random.sample(range(21,3000),90)
#     list.sort()
#     return list

a=[1,1,1,1,1,1]
b=sum(a)
print(3//1.5)
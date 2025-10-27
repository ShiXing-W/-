# test
A Non-Cooperative Game Theory-Based Self-Organized Response Method for Production Logistics Delivery in Discrete Manufacturing Workshop
#
import random
import pandas as pd
from collections import Counter
from copy import deepcopy
import taskResource
from gambling import _Gambling
import matplotlib.pyplot as plt
from pylab import *
# from random import sample
import requests
import openpyxl
import xlsxwriter
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl

# Set Chinese font for matplotlib plots
mpl.rc("font", family='YouYuan')

#region Distribution Unit, Workstation Classes
class Agv:
    """
    Autonomous Guided Vehicle (AGV) class representing a material handling robot
    """
    def __init__(self):
        # AGV identification number
        self.no = 0
        # Current task queue being executed
        self.currentTasks = []
        # Next task queue waiting to be executed
        self.nextTasks = []
        # Complete history of all tasks assigned to this AGV
        self.allTasks = []
        # Completion times for each task in the queue
        self.endTime = []
        # Current position coordinates [x, y]
        self.position = []
        # Total distance traveled by AGV
        self.journey = 0
        # Time spent moving without carrying load (empty travel)
        self.emptyLine = 0
        # Time spent idle (no tasks assigned)
        self.emptyTime = 0
        # Revenue/cost associated with AGV operations
        self.cost = 0

class Task:
    """
    Task class representing a material transport assignment
    """
    def __init__(self):
        # Task identification number
        self.no = 0
        # Starting coordinates [x, y] for the task
        self.start = []
        # Destination coordinates [x, y] for the task
        self.end = []
        # Actual start time of task execution
        self.startTime = 0
        # Actual completion time of task
        self.endTime = 0
        # Expected/desired completion time
        self.expectTime = 0
        # Distance between start and end points
        self.distance = 0
        # Task status: 0=pending, 1=assigned, 2=completed(?)
        self.done = 0
        # Response time (time from generation to assignment)
        self.responTime = 0
        # Time when task was generated/created
        self.generateTime = 0
#endregion

# Initialize task resources from external module
T = taskResource.taskinput()

#region Parameter Initialization
# Number of AGVs in the system
A_num = 20
# AGV movement speed (units per time unit)
A_v = 1
#endregion

#region Workstation and Task Initialization
A = {}    # Dictionary to store AGV objects
T3 = {}   # Placeholder for additional task data

# Create AGV objects and initialize their properties
for n in range(1, A_num + 1):
    A[n] = Agv()
    A[n].position = [20, 50]  # Initial position for all AGVs
    A[n].no = n

# Assign initial tasks to AGVs and calculate initial parameters
for n in range(1, A_num + 1):
    # Assign initial task "DTn" to each AGV
    A[n].currentTasks.append("DT" + str(n))
    A[n].allTasks.append("DT" + str(n))
    
    # Calculate completion time: travel to task + task execution + generation time
    A[n].endTime.append(
        (T["DT" + str(n)].distance // A_v) +  # Task execution time
        (abs(A[n].position[0] - T["DT" + str(n)].start[0]) +  # Travel to start point
         abs(A[n].position[1] - T["DT" + str(n)].start[1])) // A_v +  # Manhattan distance
        T["DT" + str(n)].generateTime  # Task generation time
    )
    
    # Calculate empty travel time to reach task start point
    A[n].emptyLine += (abs(A[n].position[0] - T["DT" + str(n)].start[0]) + 
                      abs(A[n].position[1] - T["DT" + str(n)].start[1])) // A_v
    
    # Update AGV position to task destination
    A[n].position = T["DT" + str(n)].end
    
    # Mark task as assigned
    T["DT" + str(n)].done = 1
    # Set task completion time
    T["DT" + str(n)].endTime = A[n].endTime[-1]
    # Calculate task start time
    T["DT" + str(n)].startTime = T["DT" + str(n)].endTime - T["DT" + str(n)].distance // A_v + T["DT" + str(n)].generateTime
    # Set response time (immediate for initial tasks)
    T["DT" + str(n)].responTime = T["DT" + str(n)].generateTime
#endregion

# Create deep copies for experimental and control groups
T1 = deepcopy(T)  # Experimental group 1
T2 = deepcopy(T)  # Experimental group 2  
A1 = deepcopy(A)  # Control group 1
A2 = deepcopy(A)  # Control group 2

# Generate 3% variant tasks (modified tasks for experiment)
# Original: list = taskResource.newtask()
list = [42, 154, 160, 162, 189, 293, 323, 345, 349, 385, 431, 439, 474, 478, 488, 532, 579, 590, 630, 642, 696, 723, 731, 742, 746, 749, 776, 787, 807, 819, 828, 848, 851, 872, 928, 953, 974, 1078, 1129, 1143, 1220, 1239, 1245, 1250, 1295, 1362, 1389, 1467, 1476, 1491, 1599, 1684, 1702, 1757, 1758, 1774, 1779, 1825, 1848, 1932, 1935, 2006, 2023, 2065, 2067, 2073, 2082, 2141, 2162, 2176, 2199, 2280, 2461, 2506, 2590, 2613, 2632, 2660, 2676, 2696, 2762, 2794, 2839, 2848, 2857, 2914, 2941, 2971, 2973, 2997]

# Create modified tasks with delayed generation times
for n in list:
    # Create copy of original task with "DTT" prefix
    T2["DTT" + str(n)] = deepcopy(T["DT" + str(n)])
    # Delay task generation by 10 time units
    T2["DTT" + str(n)].generateTime += 10
    # Also delay expected completion time
    T2["DTT" + str(n)].expectTime += 10

#region Simulation Time Loop
# Main simulation loop running for 45000 time units
for t in range(1, 45000):
    # Update task status for experimental group 1
    for i in T1.keys():
        if T1[i].generateTime == t and T1[i].done == 2:
            T1[i].done = 0  # Reactivate tasks at generation time
    
    # Update task status for experimental group 2  
    for i in T2.keys():
        if T2[i].generateTime == t and T2[i].done == 2:
            T2[i].done = 0  # Reactivate tasks at generation time
    
    # Update AGV states for both groups
    for i in range(1, A_num + 1):
        # Experimental group 1 AGV updates
        if A1[i].endTime[-1] == t:  # Current task completed
            if len(A1[i].currentTasks) != 0:
                del A1[i].currentTasks[0]  # Remove completed task
            if len(A1[i].currentTasks) != 0:  # More tasks in queue
                A1[i].endTime.append(T1[A1[i].currentTasks[0]].endTime)
                A1[i].position = T1[A1[i].currentTasks[0]].end
        
        # Experimental group 2 AGV updates  
        if A2[i].endTime[-1] == t:  # Current task completed
            if len(A2[i].currentTasks) != 0:
                del A2[i].currentTasks[0]  # Remove completed task
            if len(A2[i].currentTasks) != 0:  # More tasks in queue
                A2[i].endTime.append(T2[A2[i].currentTasks[0]].endTime)
                A2[i].position = T2[A2[i].currentTasks[0]].end
    
    # Initialize available resources for current time step
    F1 = {}    # Available AGVs in experimental group 1 (can accept new tasks)
    Pool1 = {} # Available tasks in experimental group 1 task pool
    F2 = {}    # Available AGVs in experimental group 2
    Pool2 = {} # Available tasks in experimental group 2 task pool
    
    # Identify available AGVs (with <= 1 current task)
    for k in range(1, A_num + 1):
        if len(A1[k].currentTasks) <= 1:
            F1[k] = A1[k]
        if len(A2[k].currentTasks) <= 1:
            F2[k] = A2[k]
    
    # Identify available tasks from task pools
    for key in T1.keys():
        # Tasks that are pending and within time window (expectTime - t < 480)
        if T1[key].done == 0 and (T1[key].expectTime - t) < 480:
            Pool1[key] = T1[key]
    
    for key in T2.keys():
        # All pending tasks in group 2
        if T2[key].done == 0:
            Pool2[key] = T2[key]
    
    # Task assignment for experimental group 1 using gambling/game theory approach
    if len(F1) != 0 and len(Pool1) != 0:
        gambling = _Gambling(Pool1, F1, t, T1)  # Initialize assignment algorithm
        F, T = gambling.Game()  # Execute task assignment
        # Update AGVs with new assignments
        for key in F.keys():
            A1[key] = F[key]
        # Update tasks with new status
        for key in T.keys():
            T1[key] = T[key]
    
    # Task assignment for experimental group 2 using gambling/game theory approach  
    if len(F2) != 0 and len(Pool2) != 0:
        gambling1 = _Gambling(Pool2, F2, t, T2)  # Initialize assignment algorithm
        F, T = gambling1.Game()  # Execute task assignment
        # Update AGVs with new assignments
        for key in F.keys():
            A2[key] = F[key]
        # Update tasks with new status
        for key in T.keys():
            T2[key] = T[key]

# The following sections (commented out) contain:
# - Gantt chart visualization code
# - Performance metric calculations (Cmax, W, etc.)
# - 3D trajectory plotting
# - Additional data analysis and visualization

#region Output Data to Excel
# Calculate total journey distances for each AGV
for k in range(1, A_num + 1):
    for i in A1[k].allTasks:
        A1[k].journey += T1[i].distance
    for i in A2[k].allTasks:
        A2[k].journey += T2[i].distance

# Prepare task data for experimental group 1
datatask1 = []
t1 = 0  # Total time difference accumulator
t2 = 0  # Total time difference accumulator  
d1 = 0  # Total empty line time accumulator
d2 = 0  # Total empty line time accumulator

for i in T1.keys():
    t = []
    t.append(T1[i].no)  # Task number
    t.append(T1[i].startTime)  # Start time
    t.append(T1[i].endTime)  # End time
    # Find which AGV executed this task
    for k in A1.keys():
        if i in A1[k].allTasks:
            t.append(k)  # AGV number
    t.append(T1[i].responTime)  # Response time
    t.append(T1[i].expectTime - T1[i].endTime)  # Time difference (expected vs actual)
    t1 = t1 + (T1[i].expectTime - T1[i].endTime)  # Accumulate total time difference
    datatask1.append(t)

# Create DataFrame for group 1 tasks
df1 = pd.DataFrame(datatask1, columns=['Task Number', 'Start Time', 'End Time', 'AGV Number', 'Response Time', 'Expected Completion Time Difference'])

# Prepare task data for experimental group 2
datatask2 = []
for i in T2.keys():
    t = []
    t.append(T2[i].no)
    t.append(T2[i].startTime) 
    t.append(T2[i].endTime)
    for k in A2.keys():
        if i in A2[k].allTasks:
            t.append(k)
    t.append(T2[i].responTime)
    t.append(T2[i].expectTime - T2[i].endTime)
    t2 = t2 + (T2[i].expectTime - T2[i].endTime)
    datatask2.append(t)

df2 = pd.DataFrame(datatask2, columns=['Task Number', 'Start Time', 'End Time', 'AGV Number', 'Response Time', 'Expected Completion Time Difference'])

# Prepare AGV performance data for group 1
datatask3 = []
for i in A1.keys():
    t = []
    t.append(A1[i].no)  # AGV number
    t.append(A1[i].allTasks)  # All tasks executed
    # Calculate idle time: total time - working time - empty travel time
    t.append(T1[A1[i].allTasks[-1]].endTime - A1[i].journey // A_v - A1[i].emptyLine)
    t.append(A1[i].emptyLine)  # Empty travel time
    t.append(A1[i].journey)  # Total distance traveled
    t.append(len(A1[i].allTasks))  # Number of tasks completed
    d1 = d1 + (A1[i].emptyLine)  # Accumulate total empty travel time
    t.append(sum(A1[i].cost))  # Total cost
    datatask3.append(t)

df3 = pd.DataFrame(datatask3, columns=['AGV Number', 'Task Queue', 'Idle Time', 'Empty Travel Time', 'Travel Distance', 'Task Count', 'Cost'])

# Prepare AGV performance data for group 2
datatask4 = []
for i in A2.keys():
    t = []
    t.append(A2[i].no)
    t.append(A2[i].allTasks)
    t.append(T2[A2[i].allTasks[-1]].endTime - A2[i].journey // A_v - A2[i].emptyLine)
    t.append(A2[i].emptyLine)
    t.append(A2[i].journey)
    t.append(len(A2[i].allTasks))
    t.append(sum(A2[i].cost))
    d2 = d2 + (A2[i].emptyLine)
    datatask4.append(t)

df4 = pd.DataFrame(datatask4, columns=['AGV Number', 'Task Queue', 'Idle Time', 'Empty Travel Time', 'Travel Distance', 'Task Count', 'Cost'])

# Print summary statistics
print(t1, t2, d1, d2)

# Write all DataFrames to Excel file
writer = pd.ExcelWriter('D:\\桌面\\demo\\Group2.xlsx', engine='xlsxwriter')
df1.to_excel(writer, sheet_name='Sheet1', index=False)
df2.to_excel(writer, sheet_name='Sheet2', index=False) 
df3.to_excel(writer, sheet_name='Sheet3', index=False)
df4.to_excel(writer, sheet_name='Sheet4', index=False)
writer.close()
#endregion

# The remaining commented sections contain:
# - Bar chart visualization code for performance comparison
# - 3D trajectory plotting for AGV paths
# - Additional performance metric calculations and visualizations

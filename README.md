# test
A Non-Cooperative Game Theory-Based Self-Organized Response Method for Production Logistics Delivery in Discrete Manufacturing Workshop
A Non-Cooperative Game Theory-Based Self-Organized Response Method for Production Logistics Delivery
This repository contains the implementation code for the research project titled "A Non-Cooperative Game Theory-Based Self-Organized Response Method for Production Logistics Delivery in Discrete Manufacturing Workshop". The code focuses on dynamic task allocation for Automated Guided Vehicles (AGVs) in discrete manufacturing workshops using non-cooperative game theory, aiming to optimize production logistics efficiency.
Project Overview
The core objective of this project is to realize self-organized task response and allocation for AGVs in discrete manufacturing environments. By modeling the interaction between AGVs (as players) and tasks (as resources) as a non-cooperative game, the system dynamically calculates task earnings for each AGV and allocates tasks optimally to maximize overall logistics efficiency.
File Structure
The key files in this repository are as follows:
•gambling.py: Core implementation of the game theory-based task allocation mechanism, including earnings calculation (Earning method) and task assignment logic (Game method).
•ideagambling.py: Variant implementation of the gambling mechanism with alternative earnings calculation strategies (Earning1, Earning methods).
•taskResource.py: Defines core data structures: Task (task attributes like start/end positions, expected time), Agv (AGV properties like position, task queues), and auxiliary classes (Station, Pick, Warehouse).
•newgame.py, Game.py, idea.py: Alternative implementations of Agv and Task classes with consistent attribute definitions (position, task queues, task status, etc.).
•main.py: Entry point template (basic structure for initializing and running the system).
Key Components
1.AGV Model (Agv class in newgame.py, Game.py, idea.py):
Represents AGVs with attributes including:
◦position: Current coordinates
◦currentTasks/allTasks: Task queues
◦endTime: Completion times of assigned tasks
◦cost: Accumulated earnings from tasks
1.Task Model (Task class in taskResource.py, newgame.py, etc.):
Represents logistics tasks with attributes including:
◦start/end: Start and end positions
◦expectTime: Expected completion time
◦done: Task status (0 = unassigned, 1 = assigned)
◦startTime/endTime: Actual start and completion times
1.Game Theory Mechanism (_Gambling class in gambling.py, ideagambling.py):
◦Earning(agvNo): Calculates the "earning" of an AGV (by ID agvNo) for each task in the pool, considering distance to the task start and time constraints.
◦Game(): Implements task allocation using the Hungarian algorithm (linear_sum_assignment) based on the earnings matrix, updating AGV task queues and task statuses.
Running Flow
1.Initialization:
◦Prepare the task pool (Pool): A collection of unassigned Task objects.
◦Initialize AGVs (F): A set of Agv objects with initial positions and empty task queues.
◦Set time parameters: Current time (t) and system time (T).
1.Earnings Calculation:
For each AGV, use _Gambling.Earning(agvNo) to compute earnings for all tasks in Pool, generating an earnings matrix.
2.Task Allocation:
The Game() method applies the Hungarian algorithm to the earnings matrix to find the optimal AGV-task assignment, updating:
◦Task status (done = 1 for assigned tasks)
◦AGV task queues (currentTasks, allTasks)
◦AGV position and task completion times (endTime)
1.Iteration:
Repeat the process as new tasks enter the pool or AGVs complete existing tasks, enabling dynamic self-organized response.
Usage Guide
1.Dependencies:
Ensure the following libraries are installed:

pip install numpy
(The linear_sum_assignment from scipy.optimize is used for optimal assignment, implied in the code.)
1.Setup:
◦Define task parameters (positions, expected times) and initialize Task objects in Pool.
◦Configure AGVs with initial positions and properties, stored in F.
◦Set initial time t and system time T.
1.Run the Allocation:

# Example initialization (simplified)
from gambling import _Gambling
from taskResource import Task, Agv
# Initialize tasks and AGVs
tasks = {0: Task(), 1: Task(), ...}  # Populate task attributes
agvs = {0: Agv(), 1: Agv(), ...}     # Set AGV initial positions
current_time = 0
# Create gambling instance and run allocation
game = _Gambling(Pool=tasks, F=agvs, t=current_time, T=tasks)
updated_agvs, updated_tasks = game.Game()
1.Output:
The Game() method returns updated agvs (with assigned tasks and new positions) and tasks (with status and time updates).
Notes
•The earnings calculation logic (Earning method) can be adjusted based on specific workshop requirements (e.g., modifying distance/time weights).
•Alternative implementations in ideagambling.py provide experimental earnings strategies (e.g., Earning1 with different weight coefficients).
Extend main.py to integrate real-time task generation (refer to taskResource.newtask()) and continuous allocation loops for dynamic scenarios.

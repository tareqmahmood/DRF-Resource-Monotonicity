'''
The initial allocations in Dominant Resource Fairness (DRF) are calculated based on the concept of dominant shares. Here's a simplified example to illustrate the process:

Consider a system with two resources, CPU and memory, and two users, A and B, with different resource demands:

User A's tasks require 1 CPU and 4 GB of memory each.
User B's tasks require 3 CPUs and 1 GB of memory each.
Assume the system has a total of 9 CPUs and 18 GB of memory available.

Calculate each user's dominant share:

For User A, the dominant share is the maximum share of any resource, which is 4 GB / 18 GB = 2/9 (since memory is the dominant resource for User A).
For User B, the dominant share is 3 CPUs / 9 CPUs = 1/3 (since CPU is the dominant resource for User B).
Equalize dominant shares:

The goal of DRF is to equalize the dominant shares of all users. In this case, we want to make User A's dominant share (2/9) equal to User B's dominant share (1/3).
To achieve this, we can allocate resources to each user such that their dominant shares are equal. Let's say we allocate 'x' tasks to User A and 'y' tasks to User B.
The allocation would be:
User A: x CPUs and 4x GB of memory.
User B: 3y CPUs and y GB of memory.
Solve for 'x' and 'y':

The constraints are:
The total CPU usage should not exceed 9: x + 3y ≤ 9.
The total memory usage should not exceed 18: 4x + y ≤ 18.
The dominant shares should be equal: 2x/9 = y/3.
Solving this system of equations gives us the initial allocation: x = 3 and y = 2.
Allocate resources:

Based on the solution, we allocate the following resources:
User A gets 3 CPUs and 12 GB of memory (for 3 tasks).
User B gets 6 CPUs and 2 GB of memory (for 2 tasks).
This allocation ensures that both users have an equal dominant share of 2/3, meaning they each have two-thirds of their dominant resource (memory for User A and CPU for User B).
'''


import cvxpy as cp
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--num_cpus", required=True, help="CPU demand for User A", type=int)
ap.add_argument("-m", "--num_mems", required=True, help="Memory demand for User A", type=int)
args = ap.parse_args()


# Define the total resources
num_cpus = args.num_cpus # core
num_mems = args.num_mems # GB

# Define the users' resource demands per task
cpu_a = 1
mem_a = 4
cpu_b = 3
mem_b = 1

# tolerance
tol = 0.1

# Define the variables
x = cp.Variable(integer=True) # number of tasks for User A
y = cp.Variable(integer=True) # number of tasks for User B

# Find dominant shares
dom_share_a = max(mem_a / num_mems, cpu_a / num_cpus)
dom_share_b = max(mem_b / num_mems, cpu_b / num_cpus)
print("Dominant share for User A:", dom_share_a)
print("Dominant share for User B:", dom_share_b)

# Define the constraints
constraints = [
    cpu_a * x + cpu_b * y <= num_cpus,
    mem_a * x + mem_b * y <= num_mems,
    cp.abs(dom_share_a * x - dom_share_b * y) <= tol
]


# Define the objective
obj = cp.Maximize(x + y)

# Solve the problem
prob = cp.Problem(obj, constraints)
result = prob.solve()

# Print the results
print('-----------------------------------')
print("Number of tasks for User A:", x.value)
print("Number of tasks for User B:", y.value)
print("Total CPU usage:", cpu_a * x.value + cpu_b * y.value)
print("Total memory usage:", mem_a * x.value + mem_b * y.value)
print("Total dominant share for User A:", x.value * dom_share_a)
print("Total dominant share for User B:", y.value * dom_share_b)
print("Resource allocation:")
print("User A: {} CPUs and {} GB of memory".format(cpu_a * x.value, mem_a * x.value))
print("User B: {} CPUs and {} GB of memory".format(cpu_b * y.value, mem_b * y.value))

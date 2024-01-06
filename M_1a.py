import json
import numpy as np
from python_tsp.heuristics import solve_tsp_local_search,solve_tsp_simulated_annealing
from python_tsp.exact import solve_tsp_dynamic_programming
import tsp_solutions
import pandas as pd
import copy
'''
tsp = tsp_solutions.tsp()

'''

def openfile(fname) :
    f = open('InputData/'+fname+'.json')
 
    data = json.load(f)
    f.close()
    return data

def writefile(obj,fname) :
    f = open('MyOutput/'+fname+'.json','w')
    json.dump(obj,f)

data = openfile('level1a')

ord = {}
dis_mat = []
n = data['neighbourhoods']
for i in n :
    dis_mat.append(n[i]['distances'])
    neighbour = int(i.replace('n', "")) +1
    ord[neighbour] = n[i]['order_quantity']
rn = data['restaurants']['r0']['neighbourhood_distance']
rn.insert(0,0)
dis_mat.insert(0,rn)
for i in range(1,len(dis_mat)) :
    dis_mat[i].insert(0,rn[i])
capacity = data['vehicles']['v0']['capacity']

paths = []
while (ord!={}) :
    total_orders = 0
    path = []
    while (ord!= {} and ord[max(zip(ord.values(), ord.keys()))[1]] + total_orders <= capacity) :
        total_orders += ord[max(zip(ord.values(), ord.keys()))[1]]
        path.append(max(zip(ord.values(), ord.keys()))[1])
        del ord[max(zip(ord.values(), ord.keys()))[1]]
    paths.append(path)


def get_mat(path) :
    req = copy.deepcopy(dis_mat)
    temp = []
    temp.append(req[0])
    for i in range(1,21) :
        if i not in path :
            continue 
        temp.append(req[i])
    indices_to_delete = []
    for i in range(1,21) :
        if i not in path :
            indices_to_delete.append(i)
    for i in range(len(temp)) :
        temp[i] = [value for index, value in enumerate(temp[i]) if index not in indices_to_delete]
    return temp

def calc_path(mat) :
    mat = np.array(mat)
    pm2,t = solve_tsp_simulated_annealing(mat)
    sp,cost = solve_tsp_local_search(
    mat, x0=pm2, perturbation_scheme="ps5")
    return tuple((sp,cost)) 

def shortest_paths(paths) :
    p = {}
    costs = []
    for i in range(len(paths)) :
        res = calc_path(get_mat(paths[i]))
        res[0][0] = "r0"
        res[0].append("r0")
        for j in range(1,len(res[0])-1) :
            res[0][j] = "n"+str(paths[i][res[0][j]-1]-1)
        p["path"+str(i+1)] = res[0]
        costs.append(res[1])
    return [p,costs]
output = {"v0" : shortest_paths(paths)[0]}
writefile(output,"level1a_output")



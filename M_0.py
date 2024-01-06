import json
import numpy as np
from python_tsp.heuristics import solve_tsp_local_search,solve_tsp_simulated_annealing
from python_tsp.exact import solve_tsp_dynamic_programming
import tsp_solutions
import pandas as pd
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

data = openfile('level0')

dis_mat = []
n = data['neighbourhoods']
for i in n :
    dis_mat.append(n[i]['distances'])
rn = data['restaurants']['r0']['neighbourhood_distance']
rn.insert(0,0)
dis_mat.insert(0,rn)
for i in range(1,len(dis_mat)) :
    dis_mat[i].insert(0,rn[i])
#print (dis_mat)

dis_mat = np.array(dis_mat)
pm2,t = solve_tsp_simulated_annealing(dis_mat)
sp,cost = solve_tsp_local_search(
dis_mat, x0=pm2, perturbation_scheme="ps5")

'''
visited = [0] * 50
n = len(dis_mat)
cost = 0
sp = []
def travellingsalesman(c,tsp_g):
    global cost
    adj_vertex = 99999
    min_val = 99999
    visited[c] = 1
    sp.append(c+1)
    for k in range(n):
        if (tsp_g[c][k] != 0 and visited[k] == 0):
            if (tsp_g[c][k] < min_val):
                min_val = tsp_g[c][k]
                adj_vertex = k
    if (min_val != 99999):
        cost = cost + min_val
    if (adj_vertex == 99999):
        adj_vertex = 0
        sp.append(adj_vertex + 1)
        cost += tsp_g[c][adj_vertex]
        return
    travellingsalesman(adj_vertex,tsp_g)
travellingsalesman(0,dis_mat)
'''
#print (sp)
#print (cost)
out = {"v0": {"path": []}}
out['v0']["path"].append('r0')
for i in sp[1:len(sp)] :
    out['v0']["path"].append("n"+str(i-1))
out['v0']["path"].append('r0')


writefile(out,'level0_output')
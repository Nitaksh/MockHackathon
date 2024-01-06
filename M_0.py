import json


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

visited = [0] * 50
n = len(dis_mat)
cost = 0
sp = []
def travellingsalesman(c,tsp_g):
    global cost
    adj_vertex = 999
    min_val = 999
    visited[c] = 1
    sp.append(c+1)
    for k in range(n):
        if (tsp_g[c][k] != 0 and visited[k] == 0):
            if (tsp_g[c][k] < min_val):
                min_val = tsp_g[c][k]
                adj_vertex = k
    if (min_val != 999):
        cost = cost + min_val
    if (adj_vertex == 999):
        adj_vertex = 0
        sp.append(adj_vertex + 1)
        cost += tsp_g[c][adj_vertex]
        return
    travellingsalesman(adj_vertex,tsp_g)
travellingsalesman(0,dis_mat)

out = {"v0": {"path": []}}
out['v0']["path"].append('r0')
for i in sp :
    out['v0']["path"].append("n"+str(i))
out['v0']["path"].append('r0')

writefile(out,'level0_output')
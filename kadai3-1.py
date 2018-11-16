# 次数中心性, 近接中心性, 媒介中心性の実装

import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities

# グラフを構築
G = nx.read_edgelist('youtuber4.txt', nodetype=str)

# 次数中心性
print("Degree centrality")
deg_cen = nx.degree_centrality(G)
count = 1
# dictionary型のkeyでなくvalueの値で降順にソート
for k, v in sorted(deg_cen.items(), key=lambda x: -x[1]):
    if count > 10:
        print("")
        break
    else:
        print(str(count) +  "." + str(k) + ": " + str(v))
        count = count + 1

# 近接中心性
print("Closeness centrality")
clo_cen = nx.closeness_centrality(G)
count = 1
for k, v in sorted(clo_cen.items(), key=lambda x: -x[1]):
    if count > 10:
        print("")
        break
    else:
        print(str(count) +  "." + str(k) + ": " + str(v))
        count = count + 1

# 媒介中心性
print("Betweenness centrality")
bet_cen = nx.betweenness_centrality(G)
count = 1
for k, v in sorted(bet_cen.items(), key=lambda x: -x[1]):
    if count > 10:
        print("")
        break
    else:
        print(str(count) +  "." + str(k) + ": " + str(v))
        count = count + 1


c = greedy_modularity_communities(G)

nodes = nx.nodes(G)
color_list = []

for node in nodes:
        for i, name in enumerate(c):
            #print(i,name)
            if node in c[i]:
                color_list.append(i)   

# レイアウトの取得
pos = nx.spring_layout(G)

# 可視化
plt.figure(figsize=(6, 6))
nx.draw_networkx_edges(G, pos, edge_color="gray", width=0.5, alpha=0.6)
nx.draw_networkx_nodes(G, pos, node_color=color_list, cmap=plt.cm.hsv, node_size=[round(v*5000) for k, v in bet_cen.items()], alpha=0.6)
nx.draw_networkx_labels(G, pos, font_size=4,  font_family='Osaka')
plt.axis('off')
plt.show()



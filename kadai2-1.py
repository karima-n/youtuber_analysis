# NetworkXを用いてModularityを実行       

import networkx as nx
import matplotlib.pyplot as plt 

from networkx.algorithms.community import greedy_modularity_communities

G = nx.read_edgelist('youtuber4.txt', nodetype=str)

c = greedy_modularity_communities(G)
nodes = nx.nodes(G)
color_list = []

for node in nodes:
    for i, name in enumerate(c):
        if node in c[i]:
            color_list.append(i)    


#print(color_list[:])
#print(len(color_list))
#print(nx.number_of_nodes(G))

# レイアウトの取得
pos = nx.spring_layout(G)

# pagerank の計算
pr = nx.pagerank(G)

# 可視化
plt.figure(figsize=(6, 6))
nx.draw_networkx_edges(G, pos, edge_color="gray", width=0.5, alpha=0.6)
nx.draw_networkx_nodes(G, pos, node_color=color_list, cmap=plt.cm.hsv, node_size=[10000*v for v in pr.values()], alpha=0.6)
nx.draw_networkx_labels(G, pos, font_size=8,  font_family='Osaka')
plt.axis('off')
plt.show()
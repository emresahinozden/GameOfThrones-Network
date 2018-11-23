import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import collections
import random

""" #################################################################################
Reading in datasets/book1.csv
Merging them in one dataset
Summing the weights of 5 books in merged dataset
"""
book1 = pd.read_csv("C:/Users/MONSTER/Google Drive/ders/_EX/Graph Analytics/Project/datasets/book1.csv")
book1 = book1.drop(["Type","book"],1)
book2 = pd.read_csv("C:/Users/MONSTER/Google Drive/ders/_EX/Graph Analytics/Project/datasets/book2.csv")
book2 = book2.drop(["Type","book"],1)
book3 = pd.read_csv("C:/Users/MONSTER/Google Drive/ders/_EX/Graph Analytics/Project/datasets/book3.csv")
book3 = book3.drop(["Type","book"],1)
book4 = pd.read_csv("C:/Users/MONSTER/Google Drive/ders/_EX/Graph Analytics/Project/datasets/book4.csv")
book4 = book4.drop(["Type","book"],1)
book5 = pd.read_csv("C:/Users/MONSTER/Google Drive/ders/_EX/Graph Analytics/Project/datasets/book5.csv")
book5 = book5.drop(["Type","book"],1)

book = book1.append(book2).append(book3).append(book4).append(book5)
del book1, book2, book3, book4, book5
book = book.groupby(["Source","Target"],as_index=False).sum()

book.loc[book["Source"].str.contains("Stark"), "House"] = "Stark"
book.loc[book["Source"].str.contains("Lannister"), "House"] = "Lannister"
book.loc[book["Source"].str.contains("Baratheon"), "House"] = "Baratheon"
book.loc[book["Source"].str.contains("Targaryen"), "House"] = "Targaryen"

""" #################################################################################
Creating and feeding the graph 
""" 
G = nx.Graph()
for index, edge in book.iterrows():
    G.add_node(edge['Source'], House=edge['House'])    
for index, edge in book.iterrows():
    G.add_edge(edge['Source'], edge['Target'], weight=edge['weight'])
""" #################################################################################
Creating and feeding the subgraph 
""" 
def sub_graph(house_name):
    sub = nx.Graph()
    for index, edge in book.iterrows():
        if edge.House == house_name:
            sub.add_node(edge['Source'], House=edge['House'])
    for index, edge in book.iterrows():
        if edge.House == house_name:
            sub.add_edge(edge['Source'], edge['Target'], weight=edge['weight'])
    return sub

   
""" #################################################################################
Calculating the metrics of book in a function
""" 


def metrics_function(G):
    
    #Degree Centrality
    deg_book = nx.degree_centrality(G)
    sorted_deg_book = sorted(deg_book.items(), key=lambda x:x[1], reverse=True)[0:5]
    x, y = zip(*sorted_deg_book)
    print("The degree centralities of the graph is as follows:")
    print()
    for i in range(len(sorted_deg_book)):
        print(i+1,".",x[i],"  -  ",round(y[i],3))
    #Degree Centrality graph   
    plt.figure(figsize=(10,7))
    plt.bar(x,y)
    plt.title("Degree Centrality TOP 5")
    plt.ylabel("Centrality")
    my_list =[]
    for i in range(len(x)):
        my_list.append(x[i])
    degree_sequence = sorted([d for n, d in G.degree().items()], reverse=True)  
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())
    #Degree Distribution graph
    plt.figure(figsize=(15,7))
    plt.bar(deg, cnt, width=0.80, color='b')
    plt.title("Degree Distribution")
    plt.ylabel("Count")
    plt.xlabel("Degrees")
    #Degree Distribution log/log graph
    plt.figure(figsize=(10,7))
    plt.loglog(deg, cnt)
    plt.title("Degree Distribution Log/Log")

    #Closeness Centrality
    clo_book = nx.closeness_centrality(G)    
    sorted_clo_book = sorted(clo_book.items(), key=lambda x:x[1], reverse=True)[0:5]
    x, y = zip(*sorted_clo_book)
    print()
    print()
    print("The closeness centralities of the graph is as follows:")
    print()
    for i in range(len(sorted_deg_book)):
        print(i+1,".",x[i],"  -  ",round(y[i],3))
    #Closeness Centrality graph
    plt.figure(figsize=(10,7))
    plt.bar(x,y)
    plt.title("Closeness Centrality TOP 5")
    plt.ylabel("Centrality")
    
    #Betweenness Centrality
    bet_book = nx.betweenness_centrality(G)
    sorted_bet_book = sorted(bet_book.items(), key=lambda x:x[1], reverse=True)[0:5]
    x, y = zip(*sorted_bet_book)
    print()
    print()
    print("The betweenness centralities of the graph is as follows:")
    print()
    for i in range(len(sorted_deg_book)):
        print(i+1,".",x[i],"  -  ",round(y[i],3))
    #Closeness Centrality graph        
    plt.figure(figsize=(10,7))
    plt.bar(x,y)
    plt.title("Betweenness Centrality TOP 5")
    plt.ylabel("Centrality")    
    
    #PageRank Centrality
    page_book = nx.pagerank(G)
    sorted_page_book = sorted(page_book.items(), key=lambda x:x[1], reverse=True)[0:5]
    x, y = zip(*sorted_page_book)
    print()
    print()
    print("The PageRank centralities of the graph is as follows:")
    print()
    for i in range(len(sorted_deg_book)):
        print(i+1,".",x[i],"  -  ",round(y[i],3))
    #PageRank Centrality graph
    plt.figure(figsize=(10,7))
    plt.bar(x,y)
    plt.title("PageRank Centrality TOP 5")
    plt.ylabel("Centrality")
    
    #Correlations between centralities
    measures = [nx.degree_centrality(G), 
            nx.closeness_centrality(G),
            nx.betweenness_centrality(G), 
            nx.pagerank(G)]

    cor = pd.DataFrame.from_records(measures)
    cor = cor.T
    cor.columns = ["Degree Cent.","Closeness Cent.","Betweenness Cent.","PageRank Cent."]
    print()
    print()
    print("Correlation matrix of centralities is as follows")
    print()
    print(cor.corr())

    #some metrics
    print()
    print()
    print("The diameter of the graph is:")
    print(nx.diameter(G))
    print()
    print("The radius of the graph is:")
    print(nx.radius(G))
    print()
    print("The average shortest path of the graph is:")
    print(round(nx.average_shortest_path_length(G),3))
    print()
    print("The average clustering coefficent of the graph is:")
    print(round(nx.average_clustering(G),3))
    print("The density of the graph is:")
    print(round(nx.density(G),3))
    print("The average degree of the graph is:")
    print(round((G.number_of_edges()/G.number_of_nodes())*2,3))


""" #################################################################################
Creating a spread function for the graph, and plotting every spread step
"""    

Test = nx.Graph()
Test.add_edges_from( [(1,2),(1,3),(2,3),(2,5),(3,5),(5,6),(5,7),(7,9),(7,10),(8,10),(8,11),(8,12),(8,13)] )

K = nx.karate_club_graph()
first_inf=1
prob=0.5

def mapping(x):    
    return str(x)

KK = nx.relabel_nodes(K,mapping)
   
pos = nx.spring_layout(G) 
     
def spread_function (G, first_inf, prob):
    nx.set_node_attributes(G,"infected",0)

    node_color = []

    for node in G:
        if node in first_inf:
            node_color.append('Red')
            G.node[node]["infected"] = 1
        else: node_color.append('Blue')      
    
    
    nx.draw(G,node_color = node_color,pos=pos)
    
    while (True):  
        
        d = 0
        for i in range(len(G.node)):
            a = 0
            for j in G.neighbors(G.nodes()[i]):
                a = a + G.node[j]["infected"]
            if (a/len(G.neighbors(G.nodes()[i])) >= prob and G.node[G.nodes()[i]]["infected"] == 0):
                G.node[G.nodes()[i]]["infected"] = 1
                node_color[i] ="Red"
                d = d + 1
                
        plt.figure()
        nx.draw(G,node_color=node_color,pos=pos)
        
        if d==0:
            break
        
""" below is a good example of spread function on the Targaryen sub-graph

Targaryen = sub_graph("Targaryen")
spread_function(Targaryen,["Alleras"],0.15)
spread_function(Targaryen,["Aegon-I-Targaryen"],0.15)       
"""        
        
""" #################################################################################
Calculating the connectivity and assortivity values of book in a function
""" 

def node_connectivity_function (G):
    import networkx as nx
    
    print("Node connectivity of Graph is: ",nx.node_connectivity(G))
    print("Minimum node cut of the Graph is: ",nx.minimum_node_cut(G))
    print("Edge connectivity of Graph is: ",nx.edge_connectivity(G))
    print("Minimum edge cut of the Graph is: ",nx.minimum_edge_cut(G))        
        
    print("Degree assortivity coefficent of the Graph is: ",nx.degree_assortativity_coefficient(G))  

houses_list= ["Stark","Lannister","Baratheon","Targaryen"]

def assortivity_function(list):
    for i in list:
        print("Degree assortivity of the graph ",i," is: ",round(nx.degree_assortativity_coefficient(sub_graph(i)),3))
        if nx.degree_assortativity_coefficient(sub_graph(i)) < 0:
            print("Degree assortivity of the graph ",i," is negative.\nSo it is expected to have a low degree of node connectivity and it is ",nx.node_connectivity(G),".")
            print("The person to kill in order to disconnect the graph is: ",nx.minimum_node_cut(sub_graph(i)))
        elif nx.degree_assortativity_coefficient(sub_graph(i)) > 0.5:
            print("Degree assortivity of the graph ",i," is over 0.5.\nSo it is expected to have a high degree of node connectivity and it is ",nx.node_connectivity(G),".")
            print("The persons to kill in order to disconnect the graph is: ",nx.minimum_node_cut(sub_graph(i)))
        else:
            print("Degree assortivity of the graph ",i," is between 0 and 0.5.\nSo it is expected to have a moderate degree of node connectivity and it is ",nx.node_connectivity(G),".")
            print("The persons to kill in order to disconnect the graph is: ",nx.minimum_node_cut(sub_graph(i)))            



def attack_function(G,per,n):
    GC = G.copy()
    giant = max(nx.connected_component_subgraphs(GC),key=len)
    print("Number of the nodes of the graph is ", GC.number_of_nodes())
    print("Number of the nodes of the biggest component is", giant.number_of_nodes()) 
    
    ListOfNodes = GC.nodes()
    RandomNodes = random.sample(ListOfNodes, round(per*GC.number_of_nodes()/100))
    
    bet = nx.betweenness_centrality(GC)
    sorted_bet = sorted(bet.items(),key=lambda x:x[1],reverse = True)[0:n]
    FirstNNodes = []
    for i in sorted_bet:
        FirstNNodes.append(i[0])
        
    GC.remove_nodes_from(RandomNodes)
    giant = max(nx.connected_component_subgraphs(GC),key=len)
    print("Number of the nodes of the biggest component after removing ", per," percent(",round(per*G.number_of_nodes()/100),") of the nodes randomly is ", giant.number_of_nodes()) 
    print("Diameter of the biggest component after removing ", per," percent(",round(per*G.number_of_nodes()/100),") of the nodes randomly is ", nx.diameter(giant)) 
    
    GC = G.copy()
    GC.remove_nodes_from(FirstNNodes)
    giant = max(nx.connected_component_subgraphs(GC),key=len)
    print("Number of the nodes of the biggest component after removing ", n," nodes with the highest betweenness is ", giant.number_of_nodes()) 
    print("Diameter of the biggest component after removing ", n," nodes with the highest betweenness is ", nx.diameter(giant))

    GC = G.copy()
    ListOfNodes = GC.nodes()
    RandomNodes = random.sample(ListOfNodes, len(ListOfNodes))
    import matplotlib.pyplot as plt
    RandomPlot = []
    for i in range(0,len(RandomNodes)-1):
        GC.remove_node(RandomNodes[i])
        giant = max(nx.connected_component_subgraphs(GC),key=len)
        RandomPlot.append(giant.number_of_nodes())
    plt.plot(RandomPlot)

    GC = G.copy()
    bet = nx.betweenness_centrality(GC)
    sorted_bet = sorted(bet.items(),key=lambda x:x[1],reverse = True)[0:len(ListOfNodes)]
    TargetNodes = []
    for i in sorted_bet:
        TargetNodes.append(i[0])
    TargetingPlot = []
    for i in range(0,len(TargetNodes)-1):
        GC.remove_node(TargetNodes[i])
        giant = max(nx.connected_component_subgraphs(GC),key=len)
        TargetingPlot.append(giant.number_of_nodes())
    plt.plot(TargetingPlot)


"""
An attack function that targets the most central nodes 
""" 

def attack_function0(G):
    TestGraph = G.copy()
    if nx.is_connected(TestGraph) == True:
        print("The graph is connected")
        TestGraph = G.copy()
        ListOfNodes = TestGraph.nodes()
        RandomNode = random.sample(ListOfNodes, 1)
        TestGraph.remove_nodes_from(RandomNode)
        if nx.is_connected(TestGraph) == True:
            print("Removing a random node does not disconnect the graph")
        else:
            print("Removing a random node disconnects the graph")
        
        TestGraph = G.copy() 
        deg_book = nx.degree_centrality(TestGraph)
        DegreeNode = sorted(deg_book.items(), key=lambda x:x[1], reverse=True)[0][0]
        TestGraph.remove_nodes_from(DegreeNode)
        print()
        print("The node with the highest degree is",DegreeNode)
        if nx.is_connected(TestGraph) == True:
            print("Removing the node with the highest degree does not disconnect the graph")
        else:
            print("Removing the node with the highest degree disconnects the graph")
        
        TestGraph = G.copy()
        deg_book = nx.closeness_centrality(TestGraph)
        ClosenessNode = sorted(deg_book.items(), key=lambda x:x[1], reverse=True)[0][0]
        TestGraph.remove_nodes_from(ClosenessNode)
        print()
        print("The node with the highest closeness centrality is",ClosenessNode)
        if nx.is_connected(TestGraph) == True:
            print("Removing the node with the highest closeness centrality does not disconnect the graph")
        else:
            print("Removing the node with the highest closeness centrality disconnects the graph")        
        
        TestGraph = G.copy()
        deg_book = nx.betweenness_centrality(TestGraph)
        BetweennessNode = sorted(deg_book.items(), key=lambda x:x[1], reverse=True)[0][0]
        TestGraph.remove_nodes_from(BetweennessNode)
        print()
        print("The node with the highest betweenness centrality is",BetweennessNode)
        if nx.is_connected(TestGraph) == True:
            print("Removing the node with the highest betweenness centrality does not disconnect the graph")
        else:
            print("Removing the node with the highest betweenness centrality disconnects the graph")          
                
        TestGraph = G.copy()
        deg_book = nx.pagerank(TestGraph)
        PageNode = sorted(deg_book.items(), key=lambda x:x[1], reverse=True)[0][0]
        TestGraph.remove_nodes_from(PageNode)
        print()
        print("The node with the highest PageRank is",PageNode)
        if nx.is_connected(TestGraph) == True:
            print("Removing the node with the highest PageRank does not disconnect the graph")
        else:
            print("Removing the node with the highest PageRank disconnects the graph")
    else:
        print("The graph is not connected")
        

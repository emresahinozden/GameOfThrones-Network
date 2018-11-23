The Network of Thrones is a network analysis project that gathers characters' names from the famous book series of 
'A song of Ice and Fire' and links two characters each time their names (or nicknames) appear within 15 words of one another 
(see: https://networkofthrones.wordpress.com/from-book-to-network/)

I have taken the data for each book and extracted to python and analysed using networkx library.

The code consist of those parts:

1. Reading in datasets, creating and feeding the graph 
2. A function calculating the metrics of graph (centralities, correlation between centralities, degree distribution, log-log degree dist.)
3. A function creating a spread over graph with input parameters of (A graph, Start node of spreading, Probability of spread)
4. Functions calculating node connectivity and assortativity
5. A function attacking the graph randomly and targeting the most central nodes and draws a biggest component - # of targeting attacks plot, 
input parameters are (A graph, number of targeting attack, node percentage of random attacks)
6. A function that attacks just on the most central nodes and reports the connectivity status

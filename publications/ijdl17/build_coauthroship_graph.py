import networkx as nx
from collections import defaultdict
import csv
import numpy as np

doc_dict = defaultdict(set)
doc_year_dict = defaultdict(set)

fileIn = 'author_combinations.csv'

first_name_list = set()

def effective_size(G, nodes=None, weight=None):
    """Returns the effective size of all nodes in the graph ``G``.

    The *effective size* of a node's ego network is based on the concept
    of redundancy. A person's ego network has redundancy to the extent
    that her contacts are connected to each other as well. The
    nonredundant part of a person's relationships it's the effective
    size of her ego network [1]_.  Formally, the effective size of a
    node `u`, denoted `e(u)`, is defined by

    .. math::

       e(u) = \sum_{v \in N(u) \setminus \{u\}}
       \left(1 - \sum_{w \in N(v)} p_{uw} m_{vw}\right)

    where `N(u)` is the set of neighbors of `u` and :math:`p_{uw}` is the
    normalized mutual weight of the (directed or undirected) edges
    joining `u` and `v`, for each vertex `u` and `v` [1]_. And :math:`m_{vw}`
    is the mutual weight of `v` and `w` divided by `v` highest mutual
    weight with any of its neighbors. The *mutual weight* of `u` and `v`
    is the sum of the weights of edges joining them (edge weights are
    assumed to be one if the graph is unweighted).

    For the case of unweighted and undirected graphs, Borgatti proposed
    a simplified formula to compute effective size [2]_ 

    .. math::

       e(u) = n - \frac{2t}{n}

    where `t` is the number of ties in the ego network (not including
    ties to ego) and `n` is the number of nodes (excluding ego).

    Parameters
    ----------
    G : NetworkX graph
        The graph containing ``v``. Directed graphs are treated like
        undirected graphs when computing neighbors of ``v``.

    nodes : container, optional
        Container of nodes in the graph ``G``.

    weight : None or string, optional
      If None, all edge weights are considered equal.
      Otherwise holds the name of the edge attribute used as weight.

    Returns
    -------
    dict
        Dictionary with nodes as keys and the constraint on the node as values.

    Notes
    -----
    Burt also defined the related concept of *efficency* of a node's ego
    network, which is its effective size divided by the degree of that
    node [1]_. So you can easily compute efficencty:

    >>> G = nx.DiGraph()
    >>> G.add_edges_from([(0, 1), (0, 2), (1, 0), (2, 1)])
    >>> esize = nx.effective_size(G)
    >>> efficency = {n: v / G.degree(n) for n, v in esize.items()}

    See also
    --------
    constraint

    References
    ----------
    .. [1] Burt, Ronald S.
           *Structural Holes: The Social Structure of Competition.*
           Cambridge: Harvard University Press, 1995.

    .. [2] Borgatti, S.
           "Structural Holes: Unpacking Burt's Redundancy Measures"
           CONNECTIONS 20(1):35-38.
           http://www.analytictech.com/connections/v20(1)/holes.htm

    """
    def redundancy(G, u, v, weight=None):
        nmw = normalized_mutual_weight
        r = sum(nmw(G, u, w, weight=weight) * nmw(G, v, w, norm=max, weight=weight)
                for w in set(nx.all_neighbors(G, u)))
        return 1 - r
    effective_size = {}
    if nodes is None:
        nodes = G
    # Use Borgatti's simplified formula for unweighted and undirected graphs
    if not G.is_directed() and weight is None:
        for v in G:
            # Effective size is not defined for isolated nodes
            if len(G[v]) == 0:
                effective_size[v] = float('nan')
                continue
            E = nx.ego_graph(G, v, center=False, undirected=True)
            effective_size[v] = len(E) - (2 * E.size()) / len(E)
    else:
        for v in G:
            # Effective size is not defined for isolated nodes
            if len(G[v]) == 0:
                effective_size[v] = float('nan')
                continue
            effective_size[v] = sum(redundancy(G, v, u, weight) 
                                    for u in set(nx.all_neighbors(G, v)))
    return effective_size

total_unique_authors = set()

with open(fileIn,'rb') as csvfile:
    reader = csv.reader(csvfile,delimiter=';')
    #reader = csv.DictReader(csvfile,delimiter=';')
    for row in reader:

        doc_id = row[0]
        a1 = row[2]
        a2 = row[3]
        year = row[4]
        #if int(year)< 2006: continue
        #if int(year)> 2010: continue

        #doc_id,title,a1,a2,year = line.split(';')
        doc_dict[doc_id].add(a1)
        doc_dict[doc_id].add(a2)
        doc_year_dict[year].add(doc_id)

        total_unique_authors.add(a1)
        total_unique_authors.add(a2)

        a1_first_name = a1.split(' ')[0]
        a2_first_name = a2.split(' ')[0]

        first_name_list.add(a1_first_name)
        first_name_list.add(a2_first_name)

print total_unique_authors
print len(total_unique_authors),len(doc_dict.keys())

'''

#name_out = open('first_names.txt','w')
#for name in first_name_list:
#   with open('first_names.txt','a') as out:
#       out.write(name+'\n')

gender_dict = {}
with open('gender.csv','rb') as csvfile:
    reader = csv.reader(csvfile,delimiter=',')
    #reader = csv.DictReader(csvfile,delimiter=';')
    for row in reader:

        first_name = row[3]
        gender = row[2]
        gender_dict[first_name] = gender


G = nx.Graph()

for doc in doc_dict.keys():
    author_list = list(set(doc_dict[doc])) #make the list without duplicates
    for m in author_list:
        for n in author_list:
            if m not in G.nodes():
                m_first = m.split(' ')[0]
                try:
                    m_gender = gender_dict[m_first]
                except KeyError:
                    m_gender = 'none'
                    print m
                G.add_node(m, gender = m_gender)

            if n not in G.nodes():
                n_first = n.split(' ')[0]
                try:
                    n_gender = gender_dict[n_first]
                except KeyError:
                    n_gender = 'none'
                    print n             
                G.add_node(n, gender = n_gender)
            if m != n:
                if G.has_edge(m,n):
                    G[m][n]['weight'] += 1
                else:
                    G.add_edge(m,n, weight = 1)

#### for plotting ####
print sorted(nx.connected_components(G), key = len, reverse=True)
largest_cc = max(nx.connected_components(G), key=len)
largest_cc_G = nx.Graph()
for e in G.edges():
   n1,n2 = e
   if n1 in largest_cc:
       if n2 in largest_cc:
           largest_cc_G.add_edge(n1,n2)

nx.write_gexf(largest_cc_G,"largest_cc_NOKS_2006-10.gexf")
nx.write_gexf(G,"NOKS_full_2006-10.gexf")

'''

'''                   
print nx.attribute_assortativity_coefficient(G,'gender')

node_clustering = nx.clustering(G)
node_degree = nx.degree(G)

btw_list =  nx.betweenness_centrality(G)
closeness_list = nx.closeness_centrality(G)
core_list = nx.core_number(G) #not a googd measure
esize = effective_size(G)



with open('gender_results.txt','a') as out:
    out.write("gender,avg degree, avg clustering, avg btw_cent,avg closeness_cent,avg effective_size"+'\n')
    out.write('female'+','+str(np.mean(female_deg))+','+str(np.std(female_deg))
        +','+str(np.mean(female_cc))+','+str(np.std(female_cc))
        +','+str(np.mean(female_btw))+','+str(np.std(female_btw))
        +','+str(np.mean(female_closeness))+','+str(np.std(female_closeness))
        +','+str(np.mean(female_esize))+','+str(np.std(female_esize))+'\n')

    out.write('male'+','+str(np.mean(male_deg))+','+str(np.std(male_deg))
        +','+str(np.mean(male_cc))+','+str(np.std(male_cc))
        +','+str(np.mean(male_btw))+','+str(np.std(male_btw))
        +','+str(np.mean(male_closeness))+','+str(np.std(male_closeness))
        +','+str(np.mean(male_esize))+','+str(np.std(male_esize))+'\n')


'''

'''
nx.write_gexf(G,"complete_graph_NKOS.gexf")


#### output ####
with open('node_results.txt','a') as out:
    out.write("name,degree,btw_cent,closeness_cent,effective_size"+'\n')

print 'nr. nodes', G.number_of_nodes()
largest_cc = max(nx.connected_components(G), key=len)

cc_len = [len(c) for c in sorted(nx.connected_components(G), key=len, reverse=True)]
with open('component_size.txt','w') as component_out:
    component_out.write(str(cc_len))


#print largest_cc
btw_list =  nx.betweenness_centrality(G)
closeness_list = nx.closeness_centrality(G)
core_list = nx.core_number(G) #not a googd measure
esize = effective_size(G)
for n in btw_list.keys():
    if n in largest_cc:
        with open('node_results.txt','a') as out:
            out.write(n+','+str(G.degree(n))+','+str(btw_list[n])+','+str(closeness_list[n])+','+str(esize[n])+'\n')


#### for plotting ####
#largest_cc_G = nx.Graph()
#for e in G.edges():
#   n1,n2 = e
#   if n1 in largest_cc:
#       if n2 in largest_cc:
#           largest_cc_G.add_edge(n1,n2)

#nx.write_gexf(largest_cc_G,"largest_cc_NOK.gexf")

'''
'''
print 'number of components',nx.number_connected_components(G)

print 'largest component',len(largest_cc)
#for e in G.edges(data=True):
#   print e
'''


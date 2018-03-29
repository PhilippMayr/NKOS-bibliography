import networkx as nx
from collections import defaultdict
import csv
import numpy as np

import numpy as np 
import matplotlib as mpl 

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 16}

mpl.rc('font', **font)

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

## agg backend is used to create plot as a .png file
mpl.use('agg')

doc_dict = defaultdict(set)
doc_year_dict = defaultdict(set)

fileIn = 'author_combinations.csv'


with open(fileIn,'rb') as csvfile:
    reader = csv.reader(csvfile,delimiter=';')
    #reader = csv.DictReader(csvfile,delimiter=';')
    for row in reader:

        doc_id = row[0]
        a1 = row[2]
        a2 = row[3]
        year = row[4]
        #doc_id,title,a1,a2,year = line.split(';')
        doc_dict[doc_id].add(a1)
        doc_dict[doc_id].add(a2)
        doc_year_dict[year].add(doc_id)


        a1_first_name = a1.split(' ')[0]
        a2_first_name = a2.split(' ')[0]




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
 
#### measuring node strength ##############
weight_dict = defaultdict(int)
for e in G.edges():
    n1,n2 = e
    e_weight = G[n1][n2]['weight']
    weight_dict[n1] += e_weight
    weight_dict[n2] += e_weight

############################################                   
print nx.attribute_assortativity_coefficient(G,'gender')

node_clustering = nx.clustering(G)
node_degree = nx.degree(G)

btw_list =  nx.betweenness_centrality(G)
closeness_list = nx.closeness_centrality(G)
core_list = nx.core_number(G) #not a googd measure
esize = effective_size(G)
core_list = nx.core_number(G)
rc = nx.rich_club_coefficient(G,normalized=False)
rc[23] = 1.0
print rc
print core_list

male_cc = []
male_deg = []
male_btw = []
male_closeness = []
male_esize = []
male_core = []
male_rc = []
male_strength = []

female_cc = []
female_deg = []
female_btw = []
female_closeness = []
female_esize = []
female_core = []
female_rc = []
female_strength = []

largest_cc = max(nx.connected_components(G), key=len)

count_men = 0
count_women = 0

gender_list = nx.get_node_attributes(G,'gender')
for n in G.nodes():
    if n in largest_cc:
        print n,'yes'
        n_gender = gender_list[n]
        n_clustering = node_clustering[n]
        n_degree = node_degree[n]
        n_btw = btw_list[n]
        n_closeness = closeness_list[n]
        n_esize = esize[n]
        n_core = core_list[n]
        n_rc = rc[n_degree] #what is the rich club coefficient for that node degree
        n_strength = weight_dict[n]

        if n_gender == 'male':
            count_men += 1
            male_cc.append(n_clustering)
            male_deg.append(n_degree)
            male_btw.append(n_btw)
            male_closeness.append(n_closeness)
            male_esize.append(n_esize)
            male_core.append(n_core)
            male_rc.append(n_rc)
            male_strength.append(n_strength)

        if n_gender == 'female':
            count_women += 1
            female_cc.append(n_clustering)
            female_deg.append(n_degree)
            female_btw.append(n_btw)
            female_closeness.append(n_closeness)
            female_esize.append(n_esize)
            female_core.append(n_core)
            female_rc.append(n_rc)
            female_strength.append(n_strength)

print count_men , count_women

################ make box plots ##########
## numpy is used for creating fake data


import matplotlib.pyplot as plt 

data_deg = [female_deg,male_deg]
data_cc = [female_cc,male_cc]
data_btw = [female_btw,male_btw]
data_close= [female_closeness,male_closeness]
data_esize = [female_esize,male_esize]
data_rc = [female_rc,male_rc]
data_strength = [female_strength,male_strength]
#data_core = [female_core,male_core]

# Create a figure instance
colors = ['pink','lightblue']
labels = ['F','M']
#labels_short = ['F','M']
fs = 16
# Create an axes instance
# demonstrate how to toggle the display of different elements:
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(20,8))
bplot1 = axes[0, 0].boxplot(data_deg, labels=labels , patch_artist=True , vert=False , widths=0.5)
axes[0, 0].set_title('degree', fontsize=fs)
#axes[0, 0].set_aspect(8) # or some other float

bplot2 = axes[0, 1].boxplot(data_cc, labels=labels,patch_artist=True , vert=False, widths=0.5)
axes[0, 1].set_title('clustering', fontsize=fs)
#axes[0, 1].set_aspect(10) # or some other float

#axes[0, 1].set_yscale('log')
#axes[0, 1].set_ylim(0,1.2)

bplot3 = axes[0, 2].boxplot(data_btw, labels=labels, patch_artist=True , vert=False, widths=0.5)
axes[0, 2].set_title('betweenness', fontsize=fs)
#axes[0, 2].set_aspect(8) # or some other float

#axes[0, 2].set_yscale('log')
#axes[0, 2].set_ylim(10**(-5),10**(-1))

bplot4 = axes[1, 0].boxplot(data_close, labels=labels, patch_artist=True , vert=False, widths=0.5)
axes[1, 0].set_title('closeness', fontsize=fs)
#axes[1, 0].set_aspect(8) # or some other float

#axes[1, 0].set_yscale('log')

bplot5 = axes[1, 1].boxplot(data_esize,  labels=labels,patch_artist=True , vert=False, widths=0.5)
axes[1, 1].set_title('effective size', fontsize=fs)
#axes[1, 1].set_aspect(8) # or some other float

#axes[1, 1].set_yscale('log')
#axes[1,1].set_ylim(10**(-2),25)

bplot6 = axes[1, 2].boxplot(data_strength, labels=labels,patch_artist=True , vert=False, widths=0.5)
axes[1, 2].set_title('strength', fontsize=fs)
#axes[1, 2].set_aspect(8) # or some other float

for bplot in (bplot1, bplot2,bplot3,bplot4,bplot5,bplot6):
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)

#axes[1, 2].boxplot(data, labels=labels, showfliers=False)
#axes[1, 2].set_title('showfliers=False', fontsize=fs)


# Create the boxplot
#bp = ax.boxplot(data_to_plot)

# draw temporary red and blue lines and use them to create a legend


plt.subplots_adjust(left=0.25)

# Save the figure
fig.savefig('boxplot_horizontal.pdf', bbox_inches='tight')
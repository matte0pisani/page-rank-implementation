# -*- coding: utf-8 -*-
"""
@author: matte

This is the testing module for my PageRank implementation. To test it, we compare
the pg values obtained using the NetworkX\ PageRank implementation w.r.t. mine, using
the exact same parameters for alpha, v, x_0 and so on.

"""

#  TO DO: use doctest sintax

import networkx as nx
import numpy as np
from optparse import OptionParser
import src.PageRankCalculator as prc
from src.GraphConstructor import build_graph

def nx_pagerank(file_name, alfa, rround="yes"):
    """
    This procedure applies nx's implementation on the given graph with the
    given damping parameter.

    Parameters
    ----------
    file_name : string
        The name of the file containing the desired graph to process.
    alfa : float
        The damping parameter.
    rround (optional): string
        If "yes", rounds the pg values to the first 3 decimal digits.

    Returns
    -------
    numpy.array
        An array containing the pg values for all nodes, in the order they
        appear inside the file.

    """
    with open(file_name) as f:
        lines = f.readlines()
    
    G = nx.DiGraph()
    
    for line in lines:
        t = tuple(line.strip().split(','))
        G.add_edge(*t)
    
    pr = nx.pagerank(G, alpha=alfa) 
    # pr = dict(sorted(pr.items(), key=lambda x: x[0])) SEE OLDER COMMITS
    if rround == "yes":
        return np.round(list(pr.values()), 3)
    else:
        return np.array(list(pr.values()))



def test(file_name, alpha):
    """
    Test procedure for comparing my algorithm with nx's. The algorithm will pass the
    test over a certain graph if the error made over each nodes' pg value is less than
    a thousandth of the expected value according to nx.

    Parameters
    ----------
    file_name : string
        The graph to test on.
    alpha : float
        Damping parameter.

    Returns
    -------
    None.

    """
    nx_result = nx_pagerank(file_name, alpha, rround="no")
    my_result = prc.pageRank(build_graph(file_name), alpha, rround="no")

    mse = np.mean((my_result-nx_result)**2)
    same_order_num = np.sum(np.argsort(nx_result) == np.argsort(my_result))
    
    try: # TO DO: check if admissible sintax, or if there's a better way to do it
        assert(all(abs(my_result - nx_result) < nx_result / 1000))   # TO DO: make it a one
        error = "thousandth"
    except:
        try: 
            assert(all(abs(my_result - nx_result) < nx_result / 100))
            error = "hundredth"
        except:
            assert(all(abs(my_result - nx_result) < nx_result / 10))
            error = "tenth"
    
    print()
    print("PageRank test result for", file_name)
    print("---------------------------------------------------------------------------------------------")
    print("Each pg value differs from the expected one for less than a", error, "of the expected value")
    print("The MSE is:", mse)
    print("The nodes are ranked in the same way for", same_order_num, "over", len(my_result), "nodes")
    print()

# =============================================================================
# TO DO: understand & use (...?)
# nx.draw(G, with_labels=True, node_size=2000, edge_color='#eb4034', width=3, font_size=16, font_weight=500, arrowsize=20, alpha=0.8)
# plt.savefig("graph.png")
# =============================================================================

        
if __name__ == '__main__':
    
    op = OptionParser()
    op.add_option('-f',
                  dest='input_file',
                  help='CSV filename',
                  default='graph_1.txt, graph_2.txt,' +
                  'graph_3.txt, graph_4.txt, graph_5.txt, graph_6.txt,' +
                  'graph_7.txt, graph_8.txt, graph_9.txt, graph_10.txt, graph_11.txt')
    op.add_option('--alpha',
                   dest='alpha',
                   help='Damping factor (float)',
                   default=0.85,
                   type='float')

    (options, args) = op.parse_args()

    file_names = options.input_file
    file_names_list = file_names.split(',')
    
    alpha = options.alpha
    
    for file_name in file_names_list:
        test('dataset/' + file_name.strip(), alpha)

# -*- coding: utf-8 -*-
"""
@author: matte

This is the testing module for my PageRank implementation. To test it, we compare
the pg values obtained using the NetworkX PageRank implementation w.r.t. mine, using
the exact same parameters for alpha, v, x_0 and the same algorithm version.
This module can be invoked as:
    
    python test.py [-f <list of graphs to test on> --alpha <dumping factor> --profiling_number <profiling number>]

If no argument is given, the tests will be run on all available graphs.

"""

# TO DO: use doctest sintax
# TO DO: download bigger graphs

import networkx as nx
import numpy as np
from optparse import OptionParser
import src.PageRankCalculator as prc
from src.GraphConstructor import build_graph
import timeit

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
    if rround == "yes":
        return np.round(list(pr.values()), 3)
    else:
        return np.array(list(pr.values()))



def accuracy_test(file_name, alpha, algo):
    """
    Test procedure for comparing my algorithm with nx's. The algorithm will pass the
    test over a certain graph if the error made over each nodes' pg value is less than
    a tenth of the expected value according to nx.
    For this test case we consider the iterative version of my algorithm to be compared
    to nx's.

    Parameters
    ----------
    file_name : string
        The graph to test on.
    alpha : float
        Damping parameter.
    algo: string
        Specifies if the implementation to be used should be the iterative or the exact one;
        therefore strings "iterative" and "exact"

    Returns
    -------
    None.

    """
    print()
    print("PageRank test result for", file_name, "using", algo, "version")
    print("---------------------------------------------------------------------------------------------")
    
    nx_result = nx_pagerank(file_name, alpha, rround="no")
    my_result = prc.pageRank(build_graph(file_name), alpha, algo=algo, rround="no")

    mse = np.mean((my_result-nx_result)**2)
    same_order_num = np.sum(np.argsort(nx_result) == np.argsort(my_result))
    
    try:
        np.testing.assert_allclose(my_result, nx_result, rtol=1e-03, err_msg="The actual PR values differ from the desired one by more that 1/1000 of the desired value")
        error = "thousandth"
    except AssertionError as e:
        try: 
            print(e)
            np.testing.assert_allclose(my_result, nx_result, rtol=1e-02, err_msg="The actual PR values differ from the desired one by more that 1/100 of the desired value")
            error = "hundredth"
        except AssertionError as e:
            print(e)
            np.testing.assert_allclose(my_result, nx_result, rtol=1e-01, err_msg="The actual PR values differ from the desired one by more that 1/10 of the desired value")
            error = "tenth"
    
    print()
    print("Each pg value differs from the expected one for less than a", error, "of the expected value")
    print()
    print("The MSE is:", mse)
    print("The nodes are ranked in the same way for", same_order_num, "over", len(my_result), "nodes")
    print()
    
def time_test(file_name, alpha, algo, number=10, nx_time=None):
    """
    Compute the average execution time of PageRankCalculator.pageRank and .pageRank_exact given the parameters
    and compare it with the average time of NetworkX's implementation. 
    The result is printed on the console.

    Parameters
    ----------
    file_name : string
        The graph to test on.
    alpha : float
        Damping parameter.
    number: int (optional)
        The number of repeated executions for the two implementations to average on. By default it equals 10.
    algo: string
        Specifies if the implementation to be used should be the iterative or the exact one;
        therefore strings "iterative" and "exact"
    nx_time: float (optional)
        The average reference time the implementations should be compared to; if not given it is computed
        inside the function. The default value is None to represent that no reference time was given to the
        function.

    Returns
    -------
    float tuple
        The average values for the chosen PageRankCalculator implementation and nx's given the parameters.

    """
    print()
    print("Measuring average execution time of the", algo, "algorithm, over", number, "iterations on file", file_name)
    print("------------------------------------------------------------------------------------------------------------")
    print()
    
    globals()["file_name"] = file_name
    globals()["alpha"] = alpha
    globals()["algo"] = algo
    globals()["number"] = number
    
    if nx_time is None:
        nx_time = timeit.timeit("nx_pagerank(file_name, alpha, rround=\"no\")", globals=globals(), number=10)
    my_time = timeit.timeit("prc.pageRank(build_graph(file_name), alpha, algo=algo, rround=\"no\")", 
                            globals=globals(), number=10)
    
    comparison = "faster"
    if(my_time > nx_time):
        comparison = "slower"
    
    print("Average execution time for my algorithm is", my_time, "seconds")
    print("It is", abs(my_time - nx_time) , "seconds", comparison, "than NetworkX on average")
    
    return my_time, nx_time
    
        
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
    op.add_option('--profiling-number',
                   dest='number',
                   help='The number of iterations to use to compute average execution time (int)',
                   default=10,
                   type='int')

    (options, args) = op.parse_args()

    file_names = options.input_file
    file_names_list = file_names.split(',')
    
    alpha = options.alpha
    number = options.number
    
    for file_name in file_names_list:
        path = 'dataset/' + file_name.strip()
        accuracy_test(path, alpha, "iterative")
        accuracy_test(path, alpha, "exact")
        
        _, nx_time = time_test(path, alpha, "iterative", number)
        time_test(path, alpha, "exact", number=number, nx_time=nx_time)
        
        print()

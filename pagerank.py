# -*- coding: utf-8 -*-
"""
@author: Matteo Pisani

Main module to execute the PageRank algorithm over a graph contained in the "dataset"
folder.
This module has to be invoked using the command:
        
        python pagerank.py -f <graph_file_name> [--alpha <damping_factor>
                                                 --iterations <number of max iterations>
                                                 --round <"yes" if round result, "no" otherwise>
                                                 --algo <"exact" if use exact implementation> ]
        
"""

from optparse import OptionParser
from src.GraphConstructor import build_graph
import src.PageRankCalculator as prc

if __name__ == '__main__':

    op = OptionParser()
    op.add_option('-f',
                  dest='input_file',
                  help='CSV filename')
    op.add_option('--alpha',
                   dest='alpha',
                   help='Damping factor (float)',
                   default=0.85,
                   type='float')
    op.add_option('--iterations',
                   dest='iterations',
                   help='Number of max iterations (int)',
                   default=400,
                   type='int')
    op.add_option('--round',
                   dest='rround',
                   help='Flag for rounding the results',
                   default='yes',
                   type='string')
    op.add_option('--algo',
                   dest='algo',
                   help='Type of implementation to use',
                   default='iterative',
                   type='string')

    (options, args) = op.parse_args()

    file_path = 'dataset/' + options.input_file
    alpha = options.alpha
    max_it = options.iterations
    rround = options.rround
    algo = options.algo

    g = build_graph(file_path)

    pr = prc.pageRank(g, alpha, algo=algo, max_iterations=max_it, rround=rround)
    prc.pageRank_pretty_print(g, pr)
    
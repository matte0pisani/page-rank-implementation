# -*- coding: utf-8 -*-
"""
@author: matte

Main module to execute the PageRank algorithm over a graph contained in the "dataset"
folder.
This module has to be invoked using the command:
        
        python pagerank.py -f <graph_file_name> [--alpha <damping_factor>]
        
"""

from optparse import OptionParser
from src.GraphConstructor import build_graph
from src.PageRankCalculator import pageRank

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
    # TO DO
    # optparser.add_option('--iteration',
    #                      dest='iteration',
    #                      help='Iteration (int)',
    #                      default=500,
    #                      type='int')
    # TO DO: add more options, like initialization, v, exact, rround, ...

    (options, args) = op.parse_args()

    file_path = 'dataset/' + options.input_file
    alpha = options.alpha

    # TO DO: save results somewhere, to confront
    # result_dir = 'result'
    # fname = file_path.split('/')[-1].split('.')[0]

    g = build_graph(file_path)

    PR1 = pageRank(g, alpha, algo="iterative") # TO DO: specify more options here
    print("PageRank:")
    print(PR1)
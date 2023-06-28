import json

import networkx


def cycles(graph: str):
    with open(graph) as fh:
        g = networkx.from_dict_of_lists(json.load(fh), create_using=networkx.DiGraph)
    for i in networkx.simple_cycles(g):
        print(i)

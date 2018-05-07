#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import networkx as nx

NETGRAPH_FILE = sys.argv[1]

G = nx.DiGraph()
nx.write_yaml(G, NETGRAPH_FILE)

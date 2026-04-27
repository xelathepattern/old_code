# -*- coding: utf-8 -*-
"""
Created on Thu May 26 23:20:01 2022

@author: Xela
"""


class Node:
    def __init__(self, label='Unlabeled', outNodes=None):
        self.label = label
        self.outNodes = outNodes if outNodes != None else set()

    def __repr__(self):
        return f"Node({self.label}, {set(map(lambda outNode: outNode.label, self.outNodes))})"


class Edge:
    def __init__(self, *args, directed=True):
        self.directed = directed

        if len(args) not in {1, 2}:
            raise TypeError("Edge() takes 1 or 2 non-keyword arguments")
        elif len(args)==1:
            self.outNode, self.inNode = args[0][0], args[0][1]
        elif len(args)==2:
            self.outNode, self.inNode = args[0], args[1]

    def __repr__(self):
        return f"Edge({self.outNode.label}, {self.inNode.label})"

    def __eq__(self, other):
        if self.directed:
            return (self.outNode, self.inNode) == (self.outNode, self.inNode)
        else:
            return {self.outNode, self.inNode} == {self.outNode, self.inNode}

    def __hash__(self):
        return hash((self.outNode, self.inNode, self.directed))


class Graph:
    def __init__(self, edges, edgeParsing='label_edge_str', label_edge_str_delimiters=[' ', '\n'], directed=True):
        self.nodes = set()

        if edgeParsing == 'node': #[ [Node('a'), Node('b')], [Node('b'), Node('c')] ]
            self.edges = set()
            for edge in edges:
                self.edges.add(Edge(edge[0], edge[1], directed=directed))
                self.nodes.update({edge[0], edge[1]})

            #self.labelToNode = NotImplemented #!!!labelToNode for node mode

        elif edgeParsing == 'label_edge_list': #[ ['a', 'b'], ['b', 'c'] ]
            self.labelToNode = {}
            self.edges = set()
            for edge in edges:
                outLabel, inLabel = edge[0], edge[1]

                if inLabel not in self.labelToNode.keys(): #in must be done first so that out can connect to it
                    inNode = Node(inLabel)
                    self.labelToNode[inLabel] = inNode
                else:
                    inNode = self.labelToNode[inLabel]

                if outLabel not in self.labelToNode.keys():
                    outNode = Node(outLabel)
                    self.labelToNode[outLabel] = outNode
                else:
                    outNode = self.labelToNode[outLabel]

                self.edges.add( (outNode, inNode) )

            self.__init__(self.edges, edgeParsing='node', directed=directed)

        elif edgeParsing == "label_edge_one-delimit-str": #"a b b c" #first element of the delimiter argument is used
            edges = set(zip(*[iter(edges.split(label_edge_str_delimiters[0]))]*2)) #don't worry about performance and duplication bla bla here: stackoverflow says that it's zip on two references to the same iterable, which zip forcibly evaluates in the desired groupings due to the iter(). so if a=iter([1,2,3,4]) then zip(a, a) -> [ [a.next, a.next], [a.next, a.next] ]
            self.__init__(edges, edgeParsing='label_edge_list', directed=directed)

        elif edgeParsing == "label_edge_str": #"a b\nb c"
            self.__init__( edges.replace(label_edge_str_delimiters[1], label_edge_str_delimiters[0]), edgeParsing='label_edge_one-delimit-str', directed=directed)

    def __repr__(self):
        return f"Graph( {self.edges} )"


with open('twit/twitter_combined.txt') as f:
    data = f.read()

net = Graph(data)

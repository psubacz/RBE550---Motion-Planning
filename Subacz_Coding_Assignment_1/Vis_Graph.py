# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 22:17:58 2019

@author: Subacz

Class written with help from
-https://www.tutorialspoint.com/python/python_graphs.htm
-https://stackoverflow.com/questions/6416131/python-add-new-item-to-dictionary#6416142
-https://stackoverflow.com/questions/28934223/how-to-add-x-y-coordinate-value-of-each-node-in-a-graph-data-structure
-https://stackoverflow.com/questions/15300550/return-return-none-and-no-return-at-all#15300671
-
"""

class Graph:
    """This class creates a 'persistent' data structure akin to visibility
    graph. Graph holds is listed by the vertex and each vertex holds the X-Y
    Location as well as visible edges within the graph."""
    def __init__(self,gdict=None):
        if gdict is None:
            gdict = {0: {'coordinates': ([0,0]), 'edges': []}}
        self.gdict = gdict
        
    def GetVertices(self):
        return list(self.gdict.keys())
    
    def GetCoords(self,vrtx):
        return self.gdict[vrtx]['coordinates']
 
    def SearchForCoords(self,Coords):
        for vrtx in self.gdict:
            if (Coords == self.GetCoords(vrtx)):
                return vrtx
              
    def GetVertexEdges(self,vrtx):
      return self.gdict[vrtx]['edges']
#        edgename = []
#        for vrtx in self.gdict:
#            for nxtvrtx in self.gdict[vrtx]['edges']:
#                if {nxtvrtx, vrtx} not in edgename:
#                    edgename.append({vrtx, nxtvrtx})
#        return edgename
    
    def GetGraphEdges(self):
        edgename = []
        for vrtx in self.gdict:
            for nxtvrtx in self.gdict[vrtx]['edges']:
                if {nxtvrtx, vrtx} not in edgename:
                    edgename.append({vrtx, nxtvrtx})
        return edgename

    def AddVertex(self, vrtx):
        if vrtx not in self.gdict:
            self.gdict[vrtx] = {'coordinates':([0,0]), 'edges': []}
#        else:
          
    
    def AddCoords(self,vrtx,Coords):
        self.gdict[vrtx]['coordinates'] = ([Coords[0],Coords[1]])
        
#    Adds edges to the graph
    def AddEdge(self, edge):
        (vrtx1, vrtx2) = tuple(edge)
        if vrtx1 in self.gdict:
            self.gdict[vrtx1]['edges'].append(vrtx2)
        else:
            self.gdict[vrtx1]['edges'] = [vrtx2]
#        print(self.gdict[vrtx1]['edges'])
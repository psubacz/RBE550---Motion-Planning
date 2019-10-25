# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 12:10:56 2019

@author: Subacz - RBE550 Motion Planning Coding Homework 1A - DFS/BFS
"""
#Libraries
#-----------------------------------------------------------------------------
import numpy as np
import random as rm
import matplotlib.pyplot as plt
from Vis_Graph import Graph
from Queue import Queue
from Path import Path
import time as tm

#Assumptions
#-----------------------------------------------------------------------------
# Assume a point-robot that can move in any cardinal direction with diagonals
# Start position/configuration at the top left corner
# Goal configuration - right bottom corner
#Functions
#-----------------------------------------------------------------------------
def GenerateVisibilityGraph(WIDTH,HIEGHT,grid):
  #Index of vertices to be incremented
  vertex = 0
  #initialize the frist graph element
  visibilityGraph = Graph()
  #Generate Vertices and edges of the vibility graph
  for x in range(0,WIDTH):
    for y in range(0,HIEGHT):
      #If robot is in free configuration space, create a vertex
      if (grid[y,x] == 0):
        #add vertex to graph and set coordinates
        visibilityGraph.AddVertex(vertex)
        visibilityGraph.AddCoords(vertex,[x,y])
        #Increment the vertix index
        vertex+=1
  #Generate edges and return completed visibility graph
  return GenerateEdges(visibilityGraph)

def GenerateEdges(visibilityGraph):
  for vertex in visibilityGraph.GetVertices():
    [x,y] = visibilityGraph.GetCoords(vertex)
    try:
      #calculate connected edges
      connectedEdges = [
        #diagonal directions
        visibilityGraph.SearchForCoords([x-1,y-1]),
        visibilityGraph.SearchForCoords([x+1,y-1]),
        visibilityGraph.SearchForCoords([x-1,y+1]),
        visibilityGraph.SearchForCoords([x+1,y+1]),
        #Cardinal directions
        visibilityGraph.SearchForCoords([x,y-1]),
        visibilityGraph.SearchForCoords([x,y+1]),
        visibilityGraph.SearchForCoords([x-1,y]),
        visibilityGraph.SearchForCoords([x+1,y])]
      #For vertices connected by edges, add the edges to each vertex
      for vrtxEdge in connectedEdges:
        if vrtxEdge is not None:
          visibilityGraph.AddEdge([vertex,vrtxEdge])
    except:
      #Do nothing, This is here to stop the out of bounds calculation
      pass
  return visibilityGraph

#call

#
def BreadthWidthSearch(visibilityGraph,vrtx1,vrtx2):
  #Initialize the path
  path = Path()
  #Initialize the queue
  queue = Queue()
  #Add the starting vertex to the queue
  queue.Enqueue(vrtx1)
  #mark as visited
  visitedVrtcs = [vrtx1]
  
  #while the queue is not empty run until empty
  while (len(queue.GetQueue()) != 0):
    vrtx = queue.Dequeue()
    neighbor = visibilityGraph.GetVertexEdges(vrtx)
    for nxtVrtx in neighbor:
      #if the neighbor vertex has not been visited
      if((visitedVrtcs.count(nxtVrtx)==0)):
        #queue the next vertex
        queue.Enqueue(nxtVrtx)
        #mark as visited
        visitedVrtcs.append(nxtVrtx)
        
        path.AddToPath(vrtx,nxtVrtx)

  path.GetPaths()
  return path
#        path = GrowPath(vrtx,nxtVrtx)



#-----------------------------------------------------------------------------
#Assignment Parameters
WIDTH = 10 # grid width
HIEGHT = 10 #grid hieght
#WIDTH = 5 # grid width
#HIEGHT = 5 #grid hieght

#Starting Coords
xStart = 0
yStart = 0

#Goal Coords
xEnd = WIDTH-1
yEnd = HIEGHT-1

i =rm.randint(1,4)
file = 'map'

#Generate grid
#grid = np.load(file+str(i)+'.npy')
grid =np.zeros([HIEGHT,WIDTH])
to_be_graphed = []

#Program Start
#-----------------------------------------------------------------------------
for i in range(1,3):
#if(True):
  #Generate grid
  grid = np.load( 'map'+str(i)+'.npy')
  
  tic = tm.time()
    
  #generate the visibility graph
  visibilityGraph = GenerateVisibilityGraph(WIDTH,HIEGHT,grid)
  #Search for the vertices for of the Starting/End coords 
  vrtxStart = visibilityGraph.SearchForCoords([xStart,yStart])
  vrtxEnd = visibilityGraph.SearchForCoords([xEnd,yEnd])
  
  path = BreadthWidthSearch(visibilityGraph,vrtxStart,vrtxEnd)
  
  #find the path that reaches the end
  for branch in path.GetPaths():
#    print(path.pathing[branch])
    if (path.pathing[branch][-1]==vrtxEnd):
      solution = path.pathing[branch]
      
      
  print('This final solution is:\n',solution)
  
  for vrtx in solution:
    x,y = visibilityGraph.GetCoords(vrtx)
    print(vrtx,([x,y]))
    plt.plot(x, y, marker = 'o')
    
  to_be_graphed.append([(tm.time()-tic),len(solution)])
    
  plt.imshow(grid)
  plt.show()
  print('loop took {} seconds'.format(tm.time()-tic))
  
  
#  plt.plot(to_be_graphed[i],to_be_graphed[i], marker = 'o')
plt.show()
print('Jobs Done')

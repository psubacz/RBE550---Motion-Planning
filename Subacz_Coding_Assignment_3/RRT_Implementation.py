# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 21:29:17 2019

@author: Eastwind

Rapidly Exploring Random Trees Coding Assignment

Random Configuration Sampler
Sampled Configuration Collision-free Detection
Closet Neighbors Extractor
Collision-free Path checking


"""
##Libraries
import sys,time,random
from PIL import Image
import cv2
import warnings
import numpy as np
warnings.simplefilter('ignore', np.RankWarning)


class Node():
  """A node class for RRT Pathfinding"""

  def __init__(self, parent=None, position=None):
      self.parent = parent
      self.position = position
      self.g = 0 ##distance from start to a neighbor
      self.h = 0 ##distance from node to end
      self.f = 0 ## g+h

def CheckNodeExist(n1, n2):
  y_1,x_1 = n1
  y_2,x_2 = n2
  if (x_1==x_2) and (y_1==y_2):
      return True
  else:
      return False

def calculateDistanceGoal(n1,n2):
  """
  Calculates the Euclidean distance between 2 positions (L2-norm)
  """
  return np.sqrt(((n1[0]-n2[0])**2)+((n1[1]-n2[1])**2))

def NearestVrtx(qR,pos):
  """
  Finds the nearest nodes to a expansion node
  """
  dist_ = 10*10**100
  nP = (int,int)
  for p in pos:
#        print(pos)
      if(CheckNodeExist(p.position, qR)):
          continue
      dist = calculateDistanceGoal(p.position,qR)
      if (dist < dist_):
          dist_ = dist
          nP = p
  return nP

def CalculateLOS(qNear,qNew):
  goodLOS = True
  #Calculate a line of best fit
  y = [qNew[0],qNear.position[0]]
  x = [qNew[1],qNear.position[1]]
  coefficients = np.polyfit(x, y, 1)
  polynomial = np.poly1d(coefficients)
  #Trace the line from end to start and see if the cspace is clear
  for i in range(0,abs(x[0]-x[1])):
      xx = x[1]+i
      yy = int(polynomial(x[1]+i))
      if (yy>=HIEGHT):
          yy =HIEGHT-1
      if (xx>= WIDTH):
          xx = WIDTH-1
#        print(yy,xx)
      if (CSPACE[yy,xx][0] != 255):
          goodLOS = False
  for i in range(0,abs(x[0]-x[1])):
      xx = x[1]-i
      yy = int(polynomial(x[1]-i))
      if (yy>=HIEGHT):
          yy =HIEGHT-1
      if (xx>= WIDTH):
          xx = WIDTH-1
#        print(yy,xx)
      if (CSPACE[yy,xx][0] != 255):
          goodLOS = False
  return goodLOS

def CheckConfigSpace(c0):
  """
  Checks to see if the CSPACE is free of obsticles
  """
  y,x = c0
  if (y >= HIEGHT):
      y = HIEGHT-1

  if (x >= WIDTH):
      x = WIDTH-1
  Free = False
  if(CSPACE[y,x][0]==255):
      Free = True
  return Free

def randConfig():
  return (random.randint(0,HIEGHT- 1),random.randint(0,WIDTH-1))

def visualize_search(startTree,goalTree,solutionTree):
  """
  :param save_file: (optional) filename to save image to (no filename given means no save file)
  """    # draw start and end pixels
  #Draw the lines from node to parent
  if startTree is not None:
    for node in startTree:
        if (node.parent!=None):
            parentNode=node.parent
            # Draw a diagonal blue line with thickness of 5 px
            y_1,x_1 = parentNode.position
            y_2,x_2 = node.position
            cv2.line(IMG,(x_1,y_1),(x_2,y_2),GREEN,2)
  
    for node in startTree:
        y_1,x_1 = node.position
        cv2.circle(IMG,(x_1,y_1), 5, RED, -1)
  #      print(y_1,x_1)

  if goalTree is not None:
    for node in goalTree:
        if (node.parent!=None):
            parentNode=node.parent
            # Draw a diagonal blue line with thickness of 5 px
            y_1,x_1 = parentNode.position
            y_2,x_2 = node.position
            cv2.line(IMG,(x_1,y_1),(x_2,y_2),BLUE2,2)
  
    for node in goalTree:
        y_1,x_1 = node.position
        cv2.circle(IMG,(x_1,y_1), 5, RED, -1)
      
  if solutionTree is not None:
    for node in solutionTree:
        if (node.parent!=None):
            parentNode=node.parent
            # Draw a diagonal blue line with thickness of 5 px
            y_1,x_1 = parentNode.position
            y_2,x_2 = node.position
            cv2.line(IMG,(x_1,y_1),(x_2,y_2),TEAL,2)
            
  IMG[Start] = BLUE
  IMG[Goal] = BLUE

  cv2.imwrite('output.png',IMG)
  cv2.imshow('image',IMG)
  if cv2.waitKey(1) & 0xFF == ord('q'):
      cv2.destroyAllWindows()

def rapidlyExploringRandomTree(start, goal, Bidirection):
  # Create start and end node
  q1 = None ##Solution Nodes
  q2 = None ##Solution Nodes
  startNode = Node(None, start)
  endNode = Node(None, goal)
  startTree = [startNode,]
  goalTree = [endNode,]
  numNodes = 0
  solutionFound = False
  treeSwitch = True #Switch between trees, false = Start tree, True = end tree

  while not solutionFound:
    #Draw the current Model
    visualize_search(startTree,goalTree,None)
    
    #1 Generate random point from the configuration space.
    qRand = randConfig() #returns y-x pair
    if(treeSwitch):
      #2 Find the nearest vrtx (use the open node list)
      qNear = NearestVrtx(qRand,startTree) #Returns the nearest node by dist
      #3 Select a new configuration by moving towards qNear by a preset delta
      qNew = NewConfiguration(qNear,qRand,STEP_INCREMENT)
      #3.1 Check to make sure qNew is a possible solution, if so add to open node list
      if(CheckConfigSpace(qNew)):
        #If the line of sight to parent is in free space, add
        if CalculateLOS(qNear,qNew):
          #Append the node to the open start tree list
          startTree.append(Node(qNear,qNew))
          #increment the number of nodes in the tree
          numNodes+=1
          #Switch to the opposite tree 
          if (Bidirection):
            treeSwitch = False
          #4 Check for the solution
          q1,q2 = SearchForSolution(startTree,goalTree)
          #if we have a solution, end the program and draw the solution path
          if q1 is not None:
            solutionFound = True
#            print('a',q1.position,q2.position)
            #Make the 
            solutionPath = MakeSolution(q1,q2)
            visualize_search(startTree,goalTree,solutionPath)

    else:
      #2 Find the nearest vrtx (use the open node list)
      qNear = NearestVrtx(qRand,goalTree) #Returns the nearest node by dist
      #3 Select a new configuration by moving towards qNear by a preset delta
      qNew = NewConfiguration(qNear,qRand,STEP_INCREMENT)
      #3.1 Check to make sure qNew is a possible solution, if so add to open node list
      if(CheckConfigSpace(qNew)):
        #If the line of sight to parent is in free space, add
        if (CalculateLOS(qNear,qNew)):
          #Append the node to the open goal tree list
          goalTree.append(Node(qNear,qNew))
          #increment the number of nodes in the tree
          numNodes+=1
          #Switch to the opposite tree 
          if (Bidirection):
            treeSwitch = True
          #4 Check for the solution, Return None if no solution is found
          q1,q2 = SearchForSolution(goalTree,startTree)
          #if we have a solution, end the program 
          if q1 is not None:
            solutionFound = True
#            print('b',q1.position,q2.position)
            solutionPath = MakeSolution(q1,q2)
            visualize_search(startTree,goalTree,solutionPath)

    if (numNodes>=MAX_NODES) or solutionFound :
        input('press any key')
        cv2.destroyAllWindows()
        break
  return startTree,goalTree

def NewConfiguration(qNear,qRand,dQ):
  y_1,x_1 = qNear.position
  y_2,x_2 = qRand
  dx = x_2-x_1
  dy = y_2-y_1
  
  if (dx>dQ):
      dx = dQ
  if (dy>dQ):
      dy = dQ

  y = y_1+dy
  x = x_1+dx

  if (y>=HIEGHT):
      y =HIEGHT-1

  if (x>=WIDTH):
      x = WIDTH-1
  return (y,x)

def MakeSolution(Node1,Node2):
  """
  Makes a solution by searching the first graph to the starting node. Then the 
  list is reversed and the second tree is appended to the solution
  """
  startPath =  Node1
  endPath = Node2
  solution = []
  
  while startPath is not None:
    solution.append(startPath)
    startPath = startPath.parent
    
  solution.reverse()
  solution.append(Node(solution[-1],endPath.position))

  while endPath is not None:
    solution.append(endPath)
    endPath = endPath.parent
    
  return solution

def SearchForSolution(tree1,tree2):
  """
    Search for local solution to each using the eculidian
  """
  for node1 in tree1:
    y_1,x_1 = node1.position
    for node2 in tree2:
      y_2,x_2 = node2.position
      dist = np.sqrt(((y_1-y_2)**2)+((x_1-x_2)**2))
#      print('dist: ',dist)
      if (dist <= MIN_SOL_DIST):
        return (node1,node2)
  return None,None


###Global Parameters
TEAL = (255,255,0)
NEON_GREEN = (0, 255, 0)
GREEN = (75, 255, 50)
BLUE2 = (255, 75, 50)
DARK_GRAY = (100, 144, 255)
BLUE = [255,0,0]
RED =(0,0,255)

if __name__ == "__main__":
  ##Map File
  difficulty = input("Enter difficulty: 1 for Blank_Maze, 2 for Big_Simple_Maze, or 3 for Big_Hard_Maze\n")
  # Hard code start and end positions of search for each difficulty level
  if difficulty == "1":
    FILE = "Blank_Maze.png"
  elif difficulty == "2" :
    FILE = "Big_Simple_Maze.png"
  elif difficulty == "3":
    FILE = "Big_Hard_Maze.png"
  else:
    assert False, "Incorrect difficulty level provided"
  IMG = cv2.imread(FILE)
  CSPACE = IMG.copy()
  #size of the map
  HIEGHT,WIDTH,DIM = CSPACE.shape
  MAX_NODES = 50
  STEP_INCREMENT = 250
  MIN_SOL_DIST = int(STEP_INCREMENT*0.05)
  DEBUG = False
  INITIAL_OFFSET = 10
  Start = (int(HIEGHT/2),int(WIDTH/2))
  Goal = (HIEGHT-INITIAL_OFFSET,WIDTH-INITIAL_OFFSET)
  Bidirection = True
  # Perform search on given image  
  toc = time.time()   #Added to time operations
  t1,t2 = rapidlyExploringRandomTree(Start, Goal,Bidirection)
  tic = time.time()   #Added to time operations
  print('loop took {} seconds'.format(tic-toc))
            


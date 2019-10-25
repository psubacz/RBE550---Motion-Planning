# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 22:04:02 2019

@author: Eastwind
"""

class Path:
  def __init__(self,gdict=None):
      if gdict is None:
        index = 0
        pathing = {index:[0]}
        u = [0]
        newBranch = [0]
      self.pathing = pathing
      self.index = index
      self.u = u
      self.newBranch = newBranch

  def GetIndex(self):
    return self.index
  
  def GetPaths(self):
      return self.pathing
    
# Add the vertex as a key
  def CreatePath(self, pathBranch):
     if self.index not in self.pathing:
      if(len(pathBranch)>0):
        self.pathing[self.index] = pathBranch
      else:
        self.pathing[self.index] = []
      
  # Add the new edge

  def AddToPath(self, vrtx1, vrtx2):
    breakout = False
    self.u.sort()
#    print('\npv: ',vrtx1, vrtx2)
#    print('seen: ',self.u)
    paths = list(self.pathing.keys())
    #loop through the existing paths and try attempt to locate a path where the node
       #was last visited. then add that node to that specific path
    for path in paths:
#      if(self.u.count(vrtx2)==0):
        #look at the path last step in the path and append the path to branch
#        print('\n',self.pathing[path][-1],vrtx1,self.pathing[path][-1]==vrtx1)
        if (self.pathing[path][-1]==vrtx1):
          self.pathing[path].append(vrtx2)
#          self.u.append(vrtx2)
          break
        #else if path is used by a different pathing has been visited
        else:
#          print(self.u.count(vrtx1)==1)
          if(self.u.count(vrtx1)==1):
#            print(self.pathing[path].count(vrtx1)>=1)
            if(self.pathing[path].count(vrtx1)>=1):
#             while not empty
              self.newBranch = self.pathing[path].copy()
#              print('len; ',len(self.newBranch))
              zzzz =len(self.newBranch)
              while(zzzz != 0):
#                  print(self.newBranch)
#                  print(self.newBranch[-1])
#                  qqq = self.newBranch.copy()
#                  print("qqq",qqq)
#                  print(self.newBranch[-1] == vrtx1)
                  if(self.newBranch[-1] == vrtx1):
                      self.index+=1
                      self.CreatePath(self.newBranch.copy())
                      self.pathing[self.index].append(vrtx2)
                      self.u.append(vrtx2)
#                      print(self.pathing[self.index])
                      breakout = True
                      break
                  self.newBranch.pop()
#          if(breakout):
#            break  # only executed if the inner loop DID break
                
    self.u.append(vrtx2)
#    print('path: ',self.pathing)
#    if(vrtx2==2):
#      input('ss')
    
          
  def edges(self):
      return self.findedges()
    
  def findedges(self):
      edgename = []
      for vrtx in self.pathing:
          for nxtvrtx in self.pathing[vrtx]:
              if {nxtvrtx, vrtx} not in edgename:
                  edgename.append({vrtx, nxtvrtx})
      return edgename
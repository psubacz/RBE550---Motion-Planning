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

import sys,time
from PIL import Image
import numpy as np


class Tree:
    """
    Tree based data structure
    """
    def __init__(self, data):

        self.left = None
        self.right = None
        self.data = data


    def PrintTree(self):
        print(self.data)


def CalculateDistanceGoal(n1,n2):
    """
    Calculates the Euclidean distance between 2 positions (L2-norm)
    """
    return np.sqrt(((n1[0]-n2[0])**2)+((n1[1]-n2[1])**2))



def RRT():
    pass

root = Tree(10)

root.PrintTree()


# Maximum tree size
maxTree = 0
#Tuple of the start state
Start = (2,2)
#Tuple of the goal state
Goal = (7,5)

#size of the map
mapHieght = 10
mapWidth = 10

#Create a blank configuration space node
cSpace = np.zeros([mapHieght,mapWidth])

z = CalculateDistanceGoal(Start, Goal)
print(z)
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 18:03:31 2019

@author: Eastwind
"""

class Queue:
  """A representive data structure representing a queue"""
  def __init__(self):
    self.queue = list()
    
  # Insert method to add element
  def Enqueue(self,vertex):
    if vertex not in self.queue:
        self.queue.insert(0,vertex)
        return True
    return False
  
  # Pop method to remove element
  def Dequeue(self):
    if len(self.queue)>0:
        return self.queue.pop()
    return ("No elements in Queue!")
    
  
  def GetQueue(self):
    return self.queue

  
  
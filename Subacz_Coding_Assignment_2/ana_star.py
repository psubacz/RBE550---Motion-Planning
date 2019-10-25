import sys
from PIL import Image
import numpy as np
import time

class ANA_Star:
    '''
    Anytime A* Implementation
    '''
    def __init__(self,start,end,map):
        ## Create start, end, and solution nodes
        self.startNode = Node(None, (start[0], start[1]))
        self.startNode.g = self.startNode.h = self.startNode.f = 0
        self.endNode = Node(None, (end[0], end[1]))
        self.endNode.g = self.endNode.h = self.endNode.f = 0
        self.currentNode = self.startNode
        self.solutionNode = None
        
        ## Create open and closed node lists. 
        self.openNodes = [self.startNode]
        self.closedNodes = [] 
        
        ##
        self.isFirstRun = True        
        self.map = map
        print('Running A* Search for {} seconds'.format(time.time()))
        self.AStarSearch()

        
    def AStarSearch(self):
        if(self.isFirstRun==True):
            self.isFirstRun = False
            self.solutionNode = self.currentNode = self.startNode
            self.A_Star(self.startNode,self.endNode)
            
        elif(self.solutionNode == self.currentNode):
            self.A_Star(self.startNode,self.endNode)
            
        elif(self.solutionNode != self.currentNode):
            self.openNodes = []
            self.closedNodes = []
            self.A_Star(self.currentNode,self.endNode)
            pass
    
    def A_Star(self,Node2, Node1):
        firstRun = True
        #while openNodes list is not empty
        while(len(self.openNodes) > 0):      
            zzz =input('sopace')
            if zzz == 'z':
                break
            ##Look for the lowest f cost node in openNodes
            if (firstRun):
                    print('h')
                    indexNode = 0
                    firstRun = False
            else:
                self.currentNode.f = self.openNodes[-1]
                for index,node in enumerate(self.openNodes):
                    print('s',node.position,node.f,self.currentNode.f)
                    if (node.f <= self.currentNode.f):
                        indexNode = index
                        self.currentNode = node
            print('c',self.currentNode.position)
            
            #Remove the current node from the openNodes list 
            self.openNodes.pop(indexNode)
            
            ##Append current node to closeNodes list
            self.closedNodes.append(self.currentNode)

            #if the currentnode is equal to the end node, break the loop and return the path
            if(self.CheckNodeExist(self.currentNode,self.endNode)):
                print("Jobs done.")
                self.solutionNode = self.currentNode
                print(self.GetSolution())
                break
            else:
                ##Get nearest nodes that can be traversed
                traversalNodes = self.GenerateTraversals(self.map,self.currentNode)
                ##for each traversalNodes in the GenerateTraversals
                for newNode in traversalNodes:
                    isClosed = False
                    for closedNode in self.closedNodes:
                        ##if the node is closed, continue
                        if(self.CheckNodeExist(newNode,closedNode)):
                            isClosed =True
                            continue 
                    if not isClosed:
                        ##distance from start to a neighbor
                        newNode.g = self.currentNode.g + 1
                        ##distance from node to end
                        newNode.h = self.CalculateDistanceGoal(newNode,self.endNode)
                        ##
                        newNode.f = newNode.g + newNode.h
                        #If node is in the open list and has a 
                        for openNode in self.openNodes:
                            if (self.CheckNodeExist(newNode,openNode)) and (newNode.g > openNode.g):
                                continue 
                        self.openNodes.append(newNode)
                        print('e',newNode.position)
    
    def GetSolution(self):
        path = []
        while self.solutionNode is not None: 
            path.append(self.solutionNode.position)
            self.solutionNode = self.solutionNode.parent                
        return path.reverse()
    
    def CheckNodeExist(self,node1, node2):
        x_1,y_1 = node1.position
        x_2,y_2 = node2.position
        if (x_1==x_2) and (y_1==y_2):
            return True
        else:
            return False
    def CalculateDistanceGoal(self,node1,node2):
        """
        Calculates the Euclidean distance between 2 positions (L2-norm)
        """
        x_1,y_1 = node1.position
        x_2,y_2 = node2.position
        distance = np.sqrt(((x_1-x_2)**2)+((y_1-y_2)**2))
        return distance
    def GenerateTraversals(self,map,currentNode):
        '''
        Generates possible traversable nodes, some nodes may be invalid
        '''
        x,y =currentNode.position
        traversals =[]
        for newNode in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            ##Catch for out of bounds 
            if ((x+newNode[0])<0) or ((y+newNode[1])<0):
                continue
            elif((x+newNode[0])>=width-1) or ((y+newNode[1])>=height-1):
                continue
            else:
                if not (map[x+newNode[0],y+newNode[1]] == 1):
                    traversals.append(Node(currentNode, (x+newNode[0], y+newNode[1])))
        return traversals
    
class Node():
    """A node class for A* Pathfinding"""
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0
        self.e = 0
    

'''
These variables are determined at runtime and should not be changed or mutated by you
'''
start = (0, 0)  # a single (x,y) tuple, representing the start position of the search algorithm
end = (0, 0)    # a single (x,y) tuple, representing the end position of the search algorithm
difficulty = "" # a string reference to the original import file

'''
These variables determine display coler, and can be changed by you, I guess
'''
NEON_GREEN = (0, 255, 0)
PURPLE = (85, 26, 139)
LIGHT_GRAY = (50, 50, 50)
DARK_GRAY = (100, 100, 100)

'''
These variables are determined and filled algorithmically, and are expected (and required) be mutated by you
'''
path = []       # an ordered list of (x,y) tuples, representing the path to traverse from start-->goal
expanded = {}   # a dictionary of (x,y) tuples, representing nodes that have been expanded
frontier = {}   # a dictionary of (x,y) tuples, representing nodes to expand to in the future

    
def search(map):
    """
    This function is meant to use the global variables [start, end, path, expanded, frontier] to search through the
    provided map.
    :param map: A '1-concept' PIL PixelAccess object to be searched. (basically a 2d boolean array)
    """

    # O is unoccupied (white); 1 is occupied (black)
    print("pixel value at start point ", map[start[0], start[1]])
    print("pixel value at end point ", map[end[0], end[1]])
  
    ANA_Star(start,end,map)
    
#    for node in openNodes:
#        frontier.update({node.position:True})
#
#    for node in closedNodes:
#        expanded.update({node.position:True})
#    visualize_search("out.png") # see what your search has wrought (and maybe save your results)

def visualize_search(save_file="do_not_save.png"):
    """
    :param save_file: (optional) filename to save image to (no filename given means no save file)
    """
    im = Image.open(difficulty).convert("RGB")
    pixel_access = im.load()

    # draw start and end pixels
    pixel_access[start[0], start[1]] = NEON_GREEN
    pixel_access[end[0], end[1]] = NEON_GREEN

    # draw frontier pixels
    for pixel in frontier.keys():
        pixel_access[pixel[0], pixel[1]] = (255, 0, 0)

    # draw expanded pixels
#    for pixel in expanded.keys():
#        pixel_access[pixel[0], pixel[1]] = DARK_GRAY
        
    # draw path pixels
    for pixel in path:
        pixel_access[pixel[0], pixel[1]] = PURPLE

    # display and (maybe) save results
    im.show()
    if(save_file != "do_not_save.png"):
        im.save(save_file)
    im.close()


if __name__ == "__main__":
    # Throw Errors && Such
    # global difficulty, start, end
#    assert sys.version_info[0] == 2                                 # require python 2 (instead of python 3)
#    assert len(sys.argv) == 2, "Incorrect Number of arguments"      # require difficulty input

    # Parse input arguments
    function_name = str(sys.argv[0])
#    difficulty = str(sys.argv[1])
    difficulty = "trivial.gif"
    print("running " + function_name + " with " + difficulty + " difficulty.")

    # Hard code start and end positions of search for each difficulty level
    if difficulty == "trivial.gif":
        start = (8, 1)
        end = (20, 1)
    elif difficulty == "medium.gif":
        start = (8, 201)
        end = (110, 1)
    elif difficulty == "hard.gif":
        start = (10, 1)
        end = (401, 220)
    elif difficulty == "very_hard.gif":
        start = (1, 324)
        end = (580, 1)
    else:
        assert False, "Incorrect difficulty level provided"
    # Perform search on given image
    im = Image.open(difficulty)
    width, height = im.size
    
    toc = time.time()   #Added to time operations
    z = search(im.load())
    tic = time.time()   #Added to time operations
    print('loop took {} seconds'.format(tic-toc))
            
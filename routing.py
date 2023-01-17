
from sys import argv
import csv

rows = []
inf = 9999

# Setup
fileName = argv[1]
file = open(fileName)
csvRead = csv.reader(file)
for x in csvRead:
    rows.append(x)

#Functions
def adjustCosts(row, cost):
    for node in range(1, len(row)):
        if(row[node] != "9999"):
            row[node] = int(row[node]) + cost

def dAlg(row):
    for node in range(1, len(row)):
        # if node is not part of path dictionary added
        if(node != inf):
            if(node not in paths ):
                if(visited[rows[0][node]] != 1):
                    name = str(row[0]) + str(rows[0][node])
                    paths[name] = int(row[node])       
    
    #returns the smallest path
    smallest = min(paths, key = paths.get)
    return(smallest)

#List/dictionary initilization
nodeRow = {}
visited = {}
paths = {}
costs = {}
remove = []

#Generates visited nodes dictionary
for node in range(1, len(rows[0])):
    visited[rows[0][node]] = 0

#Generates nodeRow directory for later use
for node in range(1, len(rows[0])):
    nodeRow[rows[0][node]] = node 

start = input("Starting node: ")
visited[start] = 1
tempname = start + start
cost = 0

#setting the cost of the first node to 0
costs[tempname] = cost

#Initial function call 
recur = dAlg(rows[nodeRow[start]])

#loop to generate shortest paths
while(len(costs) < len(rows)+1):
    temp = recur[-1]
    
    #marks and removes unnecessary paths
    for node in paths:
        if(node[1] == temp):
            remove.append(node)
    if(len(remove) != 0):
        for x in remove:
            paths.pop(x, None)
    remove = []
    
    #adds new shortest path to the paths dictionary
    costs[recur] = rows[nodeRow[recur[0]]][nodeRow[temp]]
    
    #removes precious shortest path from the pool
    paths.pop(recur, None)
    
    #mark node as visited
    visited[temp] = 1
    
    #adjust costs moving forward
    adjustCosts(rows[nodeRow[temp]], int(costs[recur]))
    if(paths == {}):
        break
    recur = dAlg(rows[nodeRow[temp]])

temp = ""
for x,y in costs:
    temp += "{}: {}, ".format(y, rows[nodeRow[x]][nodeRow[y]])
print(temp)    


    
#broken path tree implementation
# def recursiveTree(path, next):
#     #print("PATH: {}, NEXT{})".format(path, next))
#     if(next == start):
#         path += start
#         path = path[::-1]
#         return path
#     keys = list(costs.keys())
#     values = list(costs.values())
#     next = paths[[keys.index(path)]]
#     path += path
#     next = paths[values.index(path)]
#     return recursiveTree(path, next) 

# for x,y in costs:
#     print("{}: {}".format(x,y))
#     temp = recursiveTree(y, x)
#     print(temp)
    

#===============================================================Distance Vector Code=================================================================

#Func gets the CSV file and converts it to a 2d list
def getMainList():
    #grab the file name
    Topology = argv[1]

    #open the file
    with open(Topology, newline='') as csvfile:
        #use csv.reader and get the file
        reader = csv.reader(csvfile)
        #use list() to convert reader into a 2d list
        largelist = list(reader)

    #return the 2d list
    return largelist

#get the cost of the current node to its neighbor
def getCost(CNode, DNode, GList):
    #find the cost of CNode to DNode
    for i in range(1,len(GList[0])):
        if(GList[0][i] == DNode[0]):
            break

    #return the cost
    return CNode[i]

#find the distance from the current node to the destination node
def getDist(CNode, DNode, GList):
    #cD = Cost Destination
    #create a list to hold the cost to be compared at the end
    cD = []

    #keep the space at the start of the list
    TotalNodes = len(GList[0])

    #start the range at 1 so it begins the first node
    #loop through the nodes to get all possible destinations
    for i in range(1,TotalNodes):
        #don't compare the current node to itself, save iterations
        if(CNode[0] != GList[0][i]):
            NNode = GList[0][i]
            #c(CurrentNode, OtherNodes)
            cost1 = getCost(CNode, GList[i], GList)

            #D_OtherNode(OtherNodes)
            cost2 = getCost(DNode, NNode, GList)

            #add the cost together and throw it into the list to compare later
            cD.append(int(cost1)+int(cost2))

    #get the min value within cD and return the shortest distance possible for the needed destination
    return min(cD)

def BFEq(GivenList):
    # D_N(N') = min(c(N,N')+D_N'(N'), c(N,x)+D_x(N'),...)

    #get total amount of nodes (-1 due to the space in the first row of the arr)
    TotalNodes = len(GivenList[0]) - 1

    #create a new list to be returned later
    NList = []

    #start with the first node
    for i in range(1,TotalNodes+1):
        #get the current node with neighbors weights
        CurrentNode = GivenList[i]

        #start B-F Alg
        #get c(N,N')+D_N'(N') and insert them into a list

        #check next node
        for j in range(1,TotalNodes+1):
            #set the destination node
            DestNode = GivenList[j]
            #make sure the current node and destination node are not the same
            if(CurrentNode[0] != DestNode[0]):
                #get the distance from these nodes
                dist = getDist(CurrentNode, DestNode, GivenList)

                #compare the current saved distance
                if(int(CurrentNode[j]) > dist):
                    #if the new found dist is smaller, change that position in the current node list
                    CurrentNode[j] = dist
        
        #add the current node list to the new list
        NList.append(CurrentNode)
    
    #return the new list
    return NList

#print with proper formatting
def getOutput(GList):
    TotalNodes = len(GList[0])

    #loop through the nodes
    for i in range(TotalNodes-1):
        #initialize or reset Weights
        Weights = ""
        #loop through the weights
        for j in range(1,TotalNodes):
            #concantinate the weights into Weights and add a space
            Weights += str(GList[i][j]) + " "
        #print the node and its weights
        print("Distance vector for node ", GList[i][0], ": ", Weights)

#Main Function
def Main():
    #get the initial list
    MainList = getMainList()

    #get the list with the shortest paths possible
    NewList = BFEq(MainList)

    #print with proper formatting
    getOutput(NewList)

#call Main
Main()
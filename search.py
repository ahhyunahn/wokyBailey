# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import searchAgents
import game

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):

        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """

        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    stack = util.Stack()
    stack.push(problem.getStartState())

    visited = set([])

    pathsDic = {} # dictionary that has key as state and value as the path to key state
    pathsDic[problem.getStartState()] = []

    while True:
        if stack.isEmpty():
            return [] # if it fails, return empty list
        else:
            currentState = stack.pop()
            if currentState in visited:
                continue

            else:
                visited.add(currentState)
                if problem.isGoalState(currentState): # if we reach the goal, return path
                    return pathsDic[currentState]
                else:
                    triples = problem.getSuccessors(currentState)
                    for triple in triples:
                        stack.push(triple[0])
                        pathsDic[triple[0]] = pathsDic[currentState] + [triple[1]]


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    # we needed to do this to get the position tuple
    # startingPosition = problem.getStartState()["startPosition"]
    startingState = problem.getStartState()
    queue = util.Queue()
    queue.push(startingState)

    visited = set([])

    pathsDic = {} # dictionary that has key as state and value as the path to key state
    pathsDic[startingState] = []

    while True:
        if queue.isEmpty():
            return [] # if it fails, return empty list
        else:
            currentState = queue.pop()
            if currentState in visited:
                continue

            else:
                visited.add(currentState)
                if problem.isGoalState(currentState): # if we reach the goal, return path
                    return pathsDic[currentState]

                else:
                    triples = problem.getSuccessors(currentState)
                    for triple in triples:
                        queue.push(triple[0])
                        if triple[0] not in pathsDic.keys():
                            pathsDic[triple[0]] = pathsDic[currentState] + [triple[1]]

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    pqueue = util.PriorityQueue()
    pqueue.push(problem.getStartState(), 0)

    visited = set([])

    pathsDic = {} # dictionary that has key as state and value as the path to key state
    pathsDic[problem.getStartState()] = []

    costDic = {} # dictionary that has key as state and value as minimum cumulated cost
    costDic[problem.getStartState()] = 0

    while True:
        if pqueue.isEmpty():
            return [] # if it fails, return empty list
        else:
            currentState = pqueue.pop()
            print pathsDic[currentState]
            if currentState in visited:
                print "visited"
                continue

            else:
                visited.add(currentState)
                if problem.isGoalState(currentState): # if we reach the goal, return path
                    print "goal"
                    return pathsDic[currentState]

                else:
                    triples = problem.getSuccessors(currentState)
                    # for each triple (successor, action, stepcost) returned from getSuccessors
                    for triple in triples:
                        newcost = costDic[currentState] + triple[2]
                        print triple[0]
                        print newcost
                        # if cost is already calculated and newcost is more optimal
                        # update the priority queue and path dictionary with more optimal
                        # path
                        if triple[0] in costDic.keys() and costDic[triple[0]] > newcost:
                            costDic[triple[0]] = newcost
                            pathsDic[triple[0]] = pathsDic[currentState] + [triple[1]]
                            pqueue.update(triple[0], newcost)

                        elif not triple[0] in costDic.keys():
                            costDic[triple[0]] = costDic[currentState] + triple[2]
                            pathsDic[triple[0]] = pathsDic[currentState] + [triple[1]]
                            pqueue.update(triple[0], costDic[triple[0]])



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    """Search the node of least total cost first."""
    pqueue = util.PriorityQueue()
    pqueue.push(problem.getStartState(), 0)

    visited = set([])

    pathsDic = {} # dictionary that has key as state and value as the path to key state
    pathsDic[problem.getStartState()] = []

    valueDic = {} # dictionary that has key as state and value as cumulative cost + manhattenHeuristic
    valueDic[problem.getStartState()] = 0

    while True:
        if pqueue.isEmpty():
            return [] # if it fails, return empty list
        else:
            currentState = pqueue.pop()
            print pathsDic[currentState]

            print "heuristic of currentState ", heuristic(currentState, problem), " current state", currentState

            if currentState in visited:
                print "visited"
                continue

            else:
                visited.add(currentState)
                # if we reach the goal, return path
                if problem.isGoalState(currentState): 
                    print "goal"
                    return pathsDic[currentState]

                else:
                    triples = problem.getSuccessors(currentState)
                    # for each triple (successor, action, stepcost) returned from getSuccessors
                    for triple in triples:
                        newValue = valueDic[currentState] + triple[2] + heuristic(triple[0], problem)
                        newCost = valueDic[currentState] + triple[2]
                        print "successor state currently considered ", triple[0]
                        print "newCost ", newValue - heuristic(triple[0], problem)
                        print "valueDic[currentState ", valueDic[currentState], "cost ", triple[2], "heuristic ",heuristic(triple[0], problem)
                        # if value (cumulative cost + manhatten heuristics) is already calculated 
                        # and newValue is more optimal update the priority queue and path dictionary 
                        # with more optimal path
                        if (triple[0] in valueDic.keys() and valueDic[triple[0]] > newCost):
                            valueDic[triple[0]] = newCost
                            pathsDic[triple[0]] = pathsDic[currentState] + [triple[1]]
                            pqueue.update(triple[0], newValue)

                        elif (triple[0] not in valueDic.keys()):
                            valueDic[triple[0]] = newCost
                            pathsDic[triple[0]] = pathsDic[currentState] + [triple[1]]
                            pqueue.update(triple[0], newValue)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util, math
from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def bfs(self, currentPacmanPos, goalPositions, currentGameState):
        """ this function returns the distance and the location of closest 'goal' which is a list of 
            tuples that represent a location """
        startingPos = currentPacmanPos
        queue = util.Queue()
        queue.push(startingPos)

        visited = set([])

        pathsDic = {} # dictionary that has key as state and value as the path to key state
        pathsDic[startingPos] = []

        while True:
            if queue.isEmpty():
                return (0,0), []  # if it fails, return empty list
            else:
                currentPos = queue.pop()
                if currentPos in visited:
                    continue

                else:
                    visited.add(currentPos)
                    if currentPos in goalPositions:
                      return currentPos, pathsDic[currentPos]

                    else:
                      wallList = currentGameState.getWalls().asList()
                      successors = self.getSuccessors(currentPos, wallList, currentGameState.getWalls())
                      for successor in successors:
                        successorPos = (successor[0], successor[1])
                        queue.push(successorPos)
                        if successorPos not in pathsDic.keys():
                            pathsDic[successorPos] = pathsDic[currentPos] + [successor[-1]]

    def gridToList(self, grid):
        """ this returns a list of positions of stuff in stuffGrid (substitute stuff to either food/wall)"""
        gridList =[]
        for i in range(grid.width):
          for j in range(grid.height):
            if grid[i][j] == True:
              # print "grid[i][j]", grid[i][j]
              gridList.append((i,j))
        return gridList

    def getSuccessors(self, currentPos, wallList, grid):
        """ this returns a list of successors from current location """
        x, y = currentPos
        fourDirections = [(x-1, y, Directions.WEST), (x+1, y, Directions.EAST), \
                         (x, y+1, Directions.NORTH), (x, y-1, Directions.SOUTH)]
        return filter(lambda successorPos: self.isValidPos(successorPos[0], successorPos[1], wallList, grid), fourDirections)

    
    def isValidPos(self, x, y, wallList, grid):
        """ returns true if the position is valid in grid, and not a wall """
        if (x, y) not in wallList:
          return x > 0 and x < grid.width and y > 0 and y < grid.height

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        newGhostPoses = [ghostState.getPosition() for ghostState in newGhostStates]

        numberOfFood = successorGameState.getNumFood()

        if numberOfFood == 0:
          return 1000

        closestFoodDistance = min([manhattanDistance(newPos, foodPos) for foodPos in self.gridToList(successorGameState.getFood())])

        stopPoint = 0
        if action == Directions.STOP:
          stopPoint = 20

        closestGhostDistance = min([manhattanDistance(newPos, ghostPosition) for ghostPosition in successorGameState.getGhostPositions()])

        if newPos in newGhostPoses:
          return -1000

        return - closestFoodDistance + 3*math.sqrt(closestGhostDistance) + 1.3*successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction


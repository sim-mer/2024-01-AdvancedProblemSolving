import math
import random
import timeit
from queue import Queue
#from pathlib import Path
from abc import ABC, abstractmethod


class Player(ABC): # extends ABC(Abstract Base Class) to become an abstract class
    '''
    Abstract parent class of all player classes 
        that declares methods that must be implemented
    '''
    @abstractmethod
    def __init__(self, numBlack, numWhite, player): pass

    @abstractmethod
    def doMyTurn(self): pass
    # return (c, n), meaning that we move n(> 1) coins of color c(0 or 1)

    @abstractmethod
    def doOthersTurn(self, color, number): pass


class PTreePlayer(Player):
    def __init__(self, numBlack, numWhite, player): 
        # [0] currentPlayer, [1] numCoins(B, W), [2] numWins(Player0, Player1), [3] childList, [4] parent
        self.root = (0, [numBlack, numWhite], [0, 0], [None, None, None, None], None)
        self.player = player
        self.maxNumSimulations = 50
        self.CONST_C = math.sqrt(2)
        self.expandTree()

# [0] currentPlayer, [1] numCoins(B, W), [2] numWins(Player0, Player1), [3] childList, [4] parent
# childlist = [B - 1, B - 2, W - 1, W - 2]
    def expandTree(self):
        def addChild(childIndex, numBlackMinus, numWhiteMinus, node):
            child = ((node[0] + 1) % 2, [node[1][0] - numBlackMinus, node[1][1] - numWhiteMinus], [0, 0], [None, None, None, None], node)
            node[3][childIndex] = child

        def findValue(node, childIndex):
            childNode = node[3][childIndex]
            chSum = sum(childNode[2])
            a = childNode[2][self.player] / chSum
            b = self.CONST_C * math.sqrt(math.log(sum(node[2])) / chSum)
            return a + b

        coin = [(1, 0), (2, 0), (0, 1), (0, 2)]

        simCount = 0
        while simCount < self.maxNumSimulations:
            node = self.root
            maxChild = None
            while True:
                if node[1][0] == 0 and node[1][1] == 0:
                    return

                flag = False
                max_tuple = (0, -1)

                for i in range(4):
                    if node[1][0] - coin[i][0] < 0 or node[1][1] - coin[i][1] < 0:
                        continue
                    if node[3][i] is None:
                        addChild(i, coin[i][0], coin[i][1], node)
                        maxChild = node[3][i]
                        flag = True
                        break
                    else:
                        value = findValue(node, i)
                        if value > max_tuple[1]:
                            max_tuple = (i, value)

                if flag:
                    break

                maxChild = node[3][max_tuple[0]]
                node = maxChild

            B = maxChild[1][0]
            W = maxChild[1][1]
            result = maxChild[0]
            if B != 0 or W != 0:
                while True:
                    if B == 0 and W == 0:
                        break
                    result = (result + 1) % 2
                    if (B == 1 and W == 0) or (B == 0 and W == 1):
                        break
                    elif B >= 2:
                        B -= random.randint(1, 2)
                    elif W >= 2:
                        W -= random.randint(1, 2)
                    elif B == 1:
                        B -= 1
                    elif W == 1:
                        W -= 1

            simCount += 1
            while maxChild is not None:
                maxChild[2][result] += 1
                maxChild = maxChild[4]

    def __str__(self): # called when this instance is printed - return nodes' info in BFS order
        result = [f"A total of {sum(self.root[2]) + 1} nodes"]
        q = Queue()
        q.put(self.root)
        currentPlayerInPreviousNode = 0
        while not q.empty():
            node = q.get()
            # [0] currentPlayer, [1] numCoins(B, W), [2] numWins(Player0, Player1), [3] childList, [4] parent
            if node[0] != currentPlayerInPreviousNode: result.append("") # break a line if depth increases
            result.append(f"({node[1][0]},{node[1][1]}), win rate {node[2][self.player]/sum(node[2]):.2f} ({node[2][self.player]}/{sum(node[2])})")            
            for child in node[3]:
                if child != None: q.put(child)
            currentPlayerInPreviousNode = node[0]
        return "\n".join(result)

    def doMyTurn(self): 
        # [0] currentPlayer, [1] numCoins(B, W), [2] numWins(Player0, Player1), [3] childList, [4] parent
        maxWinRate, childWithMaxWinRate = None, None
        for child in self.root[3]:
            if child != None:
                if maxWinRate == None: maxWinRate, childWithMaxWinRate = child[2][self.player]/sum(child[2]), child
                else:
                    winRate = child[2][self.player]/sum(child[2])
                    if winRate > maxWinRate: maxWinRate, childWithMaxWinRate = winRate, child
        
        if maxWinRate == None: assert False, f"expandTree(self) is not properly implemented"

        if self.root[1][0] > childWithMaxWinRate[1][0]: color, number = 0, self.root[1][0] - childWithMaxWinRate[1][0]
        else: color, number = 1, self.root[1][1] - childWithMaxWinRate[1][1]

        self.root = childWithMaxWinRate
        self.expandTree()

        return color, number

    def doOthersTurn(self, color, number): 
        # move to a child node
        # (color, number) = (0, 1), (0, 2), (1, 1), (1, 2) map to the child with index 0, 1, 2, and 3, respectively
        self.root = self.root[3][color * 2 + number - 1]
        self.expandTree()


class TreePlayer(Player):    
    def __init__(self, numBlack, numWhite, player):
        def addChild(childIndex, numBlackMinus, numWhiteMinus):
            nonlocal node, q
            # [0] currentPlayer, [1] numCoins(B, W), [2] numWins(Player0, Player1), [3] childList, [4] parent
            child = ((node[0] + 1) % 2, [node[1][0] - numBlackMinus, node[1][1] - numWhiteMinus], [0, 0], [None, None, None, None], node)
            node[3][childIndex] = child
            q.put(child)
            self.numNodes += 1
        
        # [0] currentPlayer, [1] numCoins(B, W), [2] numWins(Player0, Player1), [3] childList, [4] parent
        self.root = (0, [numBlack, numWhite], [0, 0], [None, None, None, None], None)
        self.player = player
        self.numNodes = 1
        q = Queue()
        q.put(self.root)
        while not q.empty():
            node = q.get()
            if node[1][0] == 0 and node[1][1] == 0: # end of game
                parent = node
                while parent != None:
                    parent[2][node[0]] += 1     # add numWins
                    parent = parent[4]          # move up to the parent
            else:                
                if node[1][0] >= 1: addChild(0, 1, 0) # add a child with one fewer black coin
                if node[1][0] >= 2: addChild(1, 2, 0) # add a child with two fewer black coins
                if node[1][1] >= 1: addChild(2, 0, 1) # add a child with one fewer white coin
                if node[1][1] >= 2: addChild(3, 0, 2) # add a child with two fewer white coins
                    
    def __str__(self): # called when this instance is printed - return nodes' info in BFS order
        result = [f"A total of {self.numNodes} nodes"]
        q = Queue()
        q.put(self.root)
        currentPlayerInPreviousNode = 0
        while not q.empty():
            node = q.get()
            # [0] currentPlayer, [1] numCoins(B, W), [2] numWins(Player0, Player1), [3] childList, [4] parent
            if node[0] != currentPlayerInPreviousNode: result.append("") # break a line if depth increases
            result.append(f"({node[1][0]},{node[1][1]}), win rate {node[2][self.player]/sum(node[2]):.2f} ({node[2][self.player]}/{sum(node[2])})")            
            for child in node[3]:
                if child != None: q.put(child)
            currentPlayerInPreviousNode = node[0]
        return "\n".join(result)

    def doMyTurn(self):
        # [0] currentPlayer, [1] numCoins(B, W), [2] numWins(Player0, Player1), [3] childList, [4] parent
        maxWinRate, childWithMaxWinRate = None, None
        for child in self.root[3]:
            if child != None:
                if maxWinRate == None: maxWinRate, childWithMaxWinRate = child[2][self.player]/sum(child[2]), child
                else:
                    winRate = child[2][self.player]/sum(child[2])
                    if winRate > maxWinRate: maxWinRate, childWithMaxWinRate = winRate, child
        if self.root[1][0] > childWithMaxWinRate[1][0]: color, number = 0, self.root[1][0] - childWithMaxWinRate[1][0]
        else: color, number = 1, self.root[1][1] - childWithMaxWinRate[1][1]
        self.root = childWithMaxWinRate
        return color, number

    def doOthersTurn(self, color, number):
        # move to a child node
        # (color, number) = (0, 1), (0, 2), (1, 1), (1, 2) map to the child with index 0, 1, 2, and 3, respectively
        self.root = self.root[3][color * 2 + number - 1] 


class RandomPlayer(Player):
    def __init__(self, numBlack, numWhite, player):
        self.numCoins = [numBlack, numWhite]

    def doMyTurn(self):
        if self.numCoins[0] >= 1 and self.numCoins[1] >= 1: color = random.randint(0,1)
        elif self.numCoins[0] >= 1: color = 0
        else: color = 1

        number = random.randint(1, min(self.numCoins[color], 2))
        self.numCoins[color] -= number

        return color, number
    
    def doOthersTurn(self, color, number):
        self.numCoins[color] -= number


def runBWGame(numBlack, numWhite, PlayerClass0, PlayerClass1, debug):
    '''
    Run black-white coin game and return the winner
        numBlack, numWhite: number of black and white coins
        PlayerClass0, PlayerClass1: two players' classes. Player 0 does the first turn.
        debug: if true, print each step of the game
    '''
    assert issubclass(PlayerClass0, Player), f"PlayerClass0({PlayerClass0.__name__}) must be a subclass of Player"
    assert issubclass(PlayerClass1, Player), f"PlayerClass1({PlayerClass1.__name__}) must be a subclass of Player"

    players = [PlayerClass0(numBlack, numWhite, 0), PlayerClass1(numBlack, numWhite, 1)]
    numCoins = [numBlack, numWhite]    
    currentPlayer, otherPlayer = 0, 1
    while numCoins[0] > 0 or numCoins[1] > 0:        
        color, number = players[currentPlayer].doMyTurn()
        players[otherPlayer].doOthersTurn(color, number)

        if debug: print(f"player {currentPlayer}: ({numCoins[0]}, {numCoins[1]}) --> ", end='')
        numCoins[color] -= number
        if debug: print(f"({numCoins[0]}, {numCoins[1]})")

        currentPlayer, otherPlayer = otherPlayer, currentPlayer

    if debug: print(f"player {currentPlayer} wins")
    return currentPlayer # taking the last coin loses the game


if __name__ == "__main__":    

    # Test for in-class problems

    # Create and print a sample tree
    # TreePlayer(# of black coins, # of white coins, 0(1st player) or 1(2nd player))
    #print(TreePlayer(2, 1, 1))    

    # Run one sample game with output into stdin
    # runBWGame(# of black coins, # of white coins, 1st player's class, 2nd player's class, True(output into stdin) or False(no output))
    #print(runBWGame(2, 1, RandomPlayer, TreePlayer, True)) # Run one sample game with output into stdin

    # Run multiple games and collect statistics on winning rates and running times
    numBlack, numWhite = 3, 3
    PlayerClass0, PlayerClass1 = TreePlayer, RandomPlayer
    numGames = 10
    numWins = [0, 0]    
    for i in range(numGames):
        numWins[runBWGame(numBlack, numWhite, PlayerClass0, PlayerClass1, False)] += 1
    print(f"out of {numGames} games, player 0 and 1 win ({numWins[0]}, {numWins[1]}) times")
    
    tGame = timeit.timeit(lambda: runBWGame(numBlack, numWhite, PlayerClass0, PlayerClass1, False), number=numGames)/numGames
    print(f"Average running time is {tGame:.10f} for inputs ({numBlack}, {numWhite}, {PlayerClass0.__name__}, {PlayerClass1.__name__})")

    # Test for after-class problems
    print()
    print("Correctness test for PTreePlayer")
    print(" if your answer does not appear within 5 seconds, consider that you failed the case")
    correct = True
    
    ws22 = True
    for i in range(10):
        t = PTreePlayer(1, 1, 0)
        if t.root[2] != [4, 0]: ws22 = False
    if ws22: print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    ws22, ws32 = False, False
    for i in range(10):
        t = PTreePlayer(2, 1, 0)
        if t.root[2] == [2, 2]: ws22 = True
        elif t.root[2] == [3, 2]: ws32 = True
    if ws22 and ws32: print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    t = PTreePlayer(100, 100, 0)
    if sum(t.root[2]) == t.maxNumSimulations: print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    t = PTreePlayer(1000, 1000, 0)
    if sum(t.root[2]) == t.maxNumSimulations: print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    numWins = [0, 0]
    for i in range(10):
        numWins[runBWGame(3, 3, PTreePlayer, RandomPlayer, False)] += 1
    if numWins == [10, 0]: print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    numWins = [0, 0]
    for i in range(20):
        numWins[runBWGame(5, 5, PTreePlayer, RandomPlayer, False)] += 1
    if numWins[0] >= 14: print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    numWins = [0, 0]
    for i in range(20):
        numWins[runBWGame(0, 30, RandomPlayer, PTreePlayer, False)] += 1
    if numWins[1] >= 14: print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    numWins = [0, 0]
    for i in range(20):
        numWins[runBWGame(20, 20, RandomPlayer, PTreePlayer, False)] += 1
    if numWins[1] >= 14: print("P ", end='')
    else:
        print("F ", end='')
        correct = False

    print()
    print()
    print("Speed test for expandTree()")
    if not correct: print("fail (since the algorithm is not correct)")
    else:
        numCoins, repeat = 4, 20
        tSpeedCompare1 = timeit.timeit(lambda: runBWGame(numCoins, numCoins, TreePlayer, RandomPlayer, False), number=repeat)/repeat
        tSubmittedCode = timeit.timeit(lambda: runBWGame(numCoins, numCoins, PTreePlayer, RandomPlayer, False), number=repeat)/repeat
        print(f"For {numCoins} coins")
        print(f"Average running times of the submitted code {tSubmittedCode:.10f} and TreePlayer {tSpeedCompare1:.10f}")
        if tSubmittedCode * 4 < tSpeedCompare1: print("pass")
        else: print("fail")
        print()


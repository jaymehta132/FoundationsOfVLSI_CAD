'''
Define the Iterative Solver Class that implements a heuristic based algorithm minimizing the Reed Muller Form of Boolean Functions
'''
from truthTable import TruthTable
from reedMuller import ReedMuller
from solver import Solver
from itertools import combinations
import heapq

setPrint = True
outputFile = open('output.txt', 'w')

# Debug Test : NOT NEEDED!!
# varList = ['x1', 'x2', 'x3']
# outputList = [0, 0, 0, 0, 1, 1, 1, 1]
# numVar = 3
# table = TruthTable(numVar, varList, outputList)
# reedMullerForm = ReedMuller(table)

class IterativeSolver:
    def __init__(self, reedMullerList, literals, parameters):
        self.reedMullerList = reedMullerList
        self.literals = literals
        self.numEqns = len(reedMullerList)
        
        self.iterator = 0
        self.priorityQueue = []
        self.finalAnswer = []
        self.bestDepth = 0

        self.alpha = parameters[0]
        self.beta = parameters[1]
        self.gamma = parameters[2]

        depth = 1
        eliminations = 0
        termCount = 0
        answer = []
        for RM in reedMullerList:
            termCount += len(RM.reedMuller)
        self.bestTermCount = termCount
        
        pushElement = [reedMullerList, depth, eliminations, termCount, answer]
        heapq.heappush(self.priorityQueue, (self.alpha*depth + self.beta*(eliminations / depth) - self.gamma*termCount, pushElement))

        self.generateOptionsReedMuller()
        self.recursiveAlgorithm()


    def generateOptionsReedMuller(self):
        self.options = []
        for i in range(self.numEqns):
            literal = self.literals[i]
            otherLiterals = [x for x in self.literals if x != literal]
            self.options.append([[[literal], ['1']], literal])
            result = []
            remLen = len(otherLiterals)
            for combSize in range(1, remLen + 1):
                result.extend(combinations(otherLiterals, combSize))
            for res in result:
                self.options.append([[[literal], res], literal])
        return self.options

    def optionsForRM(self):
        return self.options

    def reedMullerListAfterChecking(self, reedMullerList, option):
        finalReedMullerList = []
        for i in range(self.numEqns):
            if type(reedMullerList[i]) == list:
                finalReedMullerList.append(reedMullerList[i].updateFunction(reedMullerList[i], option[0], option[1]))
            else:
                finalReedMullerList.append(reedMullerList[i].updateFunction(reedMullerList[i].reedMuller, option[0], option[1]))
        return finalReedMullerList
    
    def recursiveAlgorithm(self):
        popElement = heapq.heappop(self.priorityQueue)[1]
        reedMullerList, originalDepth, _, originalTerms, originalAns = popElement

        space = '--' * originalDepth
        if setPrint:
            print(f'{space} Current Depth is {originalDepth}', file = outputFile)
            print(f'{space} Current Functions :', file=outputFile)
            for i in range(self.numEqns):
                if type(reedMullerList[i]) == list:
                    print(f'{space}  {reedMullerList[i]}', file=outputFile)
                else:
                    print(f'{space}  {reedMullerList[i].reedMuller}\n', file=outputFile)
        space += '--'

        if (originalTerms == self.numEqns):
            print('SOLVED!!!', file = outputFile)
            self.finalAnswer = originalAns
        else:
            options = self.optionsForRM()
            print(f'Options : {options}', file=outputFile)

            for option in options:
                newReedMullerList = self.reedMullerListAfterChecking(reedMullerList, option)
                if setPrint:
                    print(f'{space} Substituting {option}', file=outputFile)
                    print(f'{space} New Functions :', file=outputFile)
                    for i in range(self.numEqns):
                        print(f'{space}  {newReedMullerList[i]}', file=outputFile)
                newDepth = originalDepth + 1
                newEliminations = 0
                newTerms = 0
                newAnswer = originalAns + [option]

                for RM in newReedMullerList:
                    newTerms += len(RM)
                
                if (newTerms < self.bestTermCount):
                    self.bestTermCount = newTerms
                self.iterator += 1
                print(f'{self.iterator} \t {self.bestTermCount} \t {newTerms}', file=outputFile)
                
                newEliminations = originalTerms - newTerms
                pushElement = [newReedMullerList, newDepth, newEliminations, newTerms, newAnswer]

                if (newEliminations >= 0 and newTerms <= self.bestTermCount):
                    print(f'Pushing element with depth {newDepth} best count {self.bestTermCount}, term count {newTerms} Reed Muller List {newReedMullerList}', file=outputFile)
                    heapq.heappush(self.priorityQueue, (self.alpha*newDepth + self.beta*(newEliminations / newDepth - self.gamma*newTerms), pushElement))
            self.recursiveAlgorithm()





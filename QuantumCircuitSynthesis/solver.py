'''
Implement the Solver class that combines truth tables and creates their canonical Reed Muller Form
'''
from truthTable import TruthTable
from reedMuller import ReedMuller
from typing import List
from collections import Counter
from math import ceil, log2

outputFile = open('output.txt', 'w')

class Solver:
    def __init__(self, numVar : int, literals : List[str], listTables : List[List[int]]):
        self.numVar = numVar
        self.literals = literals
        self.listTables = listTables
        self.truthTables = []
        for table in self.listTables:
            self.truthTables.append(TruthTable(self.numVar, self.literals, table))
        
        self.newListTables, self.numVar = self.updateTruthTables()
        # print(type(self.newListTables[0]))
        self.reedMullerList = []
        for table in self.newListTables:
            tempTable = TruthTable(self.numVar, self.literals, table)
            self.reedMullerList.append(ReedMuller(tempTable))
            print(self.reedMullerList[-1].getReedMuller(), file=outputFile)
            # print(self.reedMullerList[-1].reedMuller())

    def printVariables(self):
        print(file=outputFile)
        print(f'Size of Function : {self.numVar}', file=outputFile)
        print(f'Variables : {self.literals}', file=outputFile)
        print(file=outputFile)
        print('Truth Tables :', file=outputFile)
        for table in self.truthTables:
            table.printTable()
        print(file=outputFile)
    
    def updateTruthTables(self):
        terms = []
        for i in range(len(self.listTables[0])):
            num = 0
            for j in range(len(self.listTables)):
                num = num + self.listTables[j][i] * (2 ** j)
            terms.append(num)
        print(f'Original Terms : {terms}', file=outputFile)

        # Finding the repeated terms
        counts = Counter(terms)
        print('Counts :', file=outputFile)
        print(counts, file=outputFile)
        # Print the repeated terms
        repeatedTerms = []
        for key, value in counts.items():
            if value > 1:
                repeatedTerms.append(tuple((key, value)))
        # Bit extension = log2(maxRepeatedTerms)
        if repeatedTerms == []:
            bitExtension = 0
            print('No Bit Extension', file=outputFile)
            return self.listTables, self.numVar
        
        maxRepeats = max(repeatedTerms, key = lambda x : x[1])
        bitExtension = ceil(log2(maxRepeats[1]))
        print(f'Bit Extension Needed : {bitExtension}', file=outputFile)

        newTerms = []
        # Update the terms to accomodate for the bitExtension
        for i in range(len(terms)):
            newTerms.append(terms[i] * (2 ** bitExtension) + counts[terms[i]] - 1)
            counts[terms[i]] = counts[terms[i]] - 1

        # Add values to the literals to accomodate for the extra variables
        for i in range(bitExtension):
            self.literals.append(f'x{self.numVar+i+1}')

        self.numVar = self.numVar + bitExtension
        for i in range(2 ** self.numVar):
            if i not in newTerms:
                newTerms.append(i)
        print(f'New Terms \n {newTerms}', file=outputFile)

        # Convert the new terms into appropriate Truth Tables
        newListTruthTables = []
        for i in range(self.numVar):
            newTable = []
            for j in range(len(newTerms)):
                newTable.append((newTerms[j] >> i) & 1)
            newListTruthTables.append(TruthTable(self.numVar, self.literals, newTable))
        # print(newListTruthTables)
        return newListTruthTables, self.numVar


def main():
    listTables = [[1, 1, 1, 1], [0, 0, 0, 0]]
    literals = ['x1', 'x2']
    numVar = 2

    solver = Solver(numVar, literals, listTables)


# if __name__ == '__main__':
#     main()
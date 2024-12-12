'''
Converts an input Truth Table into the equivalent Reed Muller representation
'''
from truthTable import TruthTable
from collections import Counter
from typing import List
from copy import deepcopy

outputFile = open('output.txt', 'w')

class ReedMuller:
    def __init__(self, truthTable : TruthTable):
        self.truthTable = truthTable
        # Get the parameters for the Truth Table
        self.numVar = truthTable.numVar
        self.varList = truthTable.varList
        self.outputList = truthTable.outputList
        self.reedMuller = self.getReedMuller()
        self.reedMullerLOL = self.listOfLists()

    def getReedMuller(self):
        '''
        Get the Reed-Muller representation for the truth table.
        '''
        # Base case: single variable truth table
        if self.numVar == 1:
            if self.truthTable.outputList == [0, 1]:
                return [self.truthTable.varList[0]]
            elif self.truthTable.outputList == [1, 0]:
                return ['1', self.truthTable.varList[0]]
            elif self.truthTable.outputList == [0, 0]:
                return ['0']
            elif self.truthTable.outputList == [1, 1]:
                return ['1']
        
        # Recursive case: split table based on the first variable
        # var = self.truthTable.varList[0]
        # print(self.truthTable.varList[1:])
        # print(self.truthTable.varList[0])
        subTableVar = self.truthTable.getSubTable(self.truthTable.varList[0], 0)
        subTableBarVar = self.truthTable.getSubTable(self.truthTable.varList[0], 1)

        # Get Reed-Muller forms for sub-tables
        reedMullerVar = ReedMuller(subTableVar).getReedMuller()
        reedMullerBarVar = ReedMuller(subTableBarVar).getReedMuller()
        
        xFx = []
        for term in reedMullerVar:
            if term == '0':
                continue
            elif term == '1':
                xFx.append(self.truthTable.varList[0])
            else:
                xFx.append(self.truthTable.varList[0] + term)

        xFxBar = []
        for term in reedMullerBarVar:
            if term == '0':
                continue
            elif term == '1':
                xFxBar.append(self.truthTable.varList[0])
            else:
                xFxBar.append(self.truthTable.varList[0] + term)        
        combinedReedMuller = xFx + xFxBar + reedMullerVar

        # print(combinedReedMuller)

        if '0' in combinedReedMuller:
            combinedReedMuller.remove('0')      

        combinedReedMuller = [key for key, value in Counter(combinedReedMuller).items() if value % 2 == 1]
        return combinedReedMuller
    
    def listOfLists(self) -> List[List[str]]:
        '''
        Convert the Reed-Muller representation to a list of lists
        '''
        reedMullerList = []
        for term in self.reedMuller:
            termList = []
            for var in self.truthTable.varList:
                if var in term:
                    termList.append(var)
            if termList == []:
                termList.append('1')
            reedMullerList.append(termList)
        return reedMullerList
    
    def evaluateReedMuller(self, inputs : List[int]) -> int:
        reedMullerLOL = self.listOfLists()
        output = 0
        for term in reedMullerLOL:
            termOutput = 1
            for var in term:
                if var == '1':
                    continue
                index = self.truthTable.varList.index(var)
                termOutput *= inputs[index]
            output += termOutput
        return output % 2
    
    def updateFunction(self, newLiteral, expression, alterLiteral):
        '''
        Update and Simplify the Reed Muller Representation by constructing the function based on a given literal
        '''
        newReedMuller = []
        tempReedMuller = deepcopy(newLiteral)
        for term in tempReedMuller:
            newTerm = deepcopy(term)
            if alterLiteral not in term:
                newReedMuller.append(newTerm)
                continue
            else:
                tempTerm = [literal for literal in newTerm if literal != alterLiteral]
                for element in expression:
                    newTemp = deepcopy(tempTerm)
                    for i in range(len(element)):
                        if element[i] != '1':
                            newTemp = newTemp + [element[i]]
                        if newTemp == []:
                            newTemp = ['1']
                    newReedMuller.append(newTemp)
        
        for i in range(len(newReedMuller)):
            newReedMuller[i] = [key for key, _ in Counter(newReedMuller[i]).items()]
            newReedMuller[i].sort()

        # Check for repeated terms in the new Reed Muller Representation
        for term in newReedMuller:
            if newReedMuller.count(term) % 2 == 0:
                # Can remove the term entirely
                while term in newReedMuller:
                    newReedMuller.remove(term)
            else:
                # Keep a single occurance of the term
                while newReedMuller.count(term) > 1:
                    newReedMuller.remove(term)
        print('New Reed Muller :', file=outputFile)
        print(newReedMuller, file=outputFile)
        return newReedMuller
    
    def updateClassFunction(self, newLiterals, expression, alterLiteral):
        self.reedMullerLOL = self.updateFunction(newLiterals, expression, alterLiteral)
        self.varList = newLiterals
        print(self.getReedMuller(), file=outputFile)
            
        


def main():
    variableList = ['X', 'Y']
    outputList = [0, 1, 1, 1]
    numVar = 2

    truthTable = TruthTable(numVar, variableList, outputList)
    truthTable.printTable()
    reedMuller = ReedMuller(truthTable)
    print("Reed Muller Representation")
    print(reedMuller.reedMuller)
    print(reedMuller.listOfLists())
    print(reedMuller.evaluateReedMuller([0, 1]))
    reedMuller.updateFunction([['X'], ['X', 'Y'], ['Y']],[['1'], ['Z']], 'X')

# if __name__ == '__main__':
#     main()
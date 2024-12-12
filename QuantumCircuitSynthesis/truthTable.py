'''
Create a Class for a Truth Table and implement the functions required for the Quantum Circuit Synthesis

'''
from typing import List

outputFile = open('output.txt', 'w')

class TruthTable:
    def __init__(self, numVar, varList, outputList):
        self.numVar = numVar
        self.varList = varList
        self.outputList = outputList
        self.table = []

    def getOutputs(self, inputs : List[str]) -> List[str]:
        '''
        Get the outputs for the given list of binary inputs
        Inputs: List of binary inputs
        Outputs: List of binary outputs
        '''
        # print(f'Inputs : {inputs}')
        # print(f'Output List : {self.outputList}')
        return self.outputList[int(''.join(map(str, inputs)), 2)]
    
    def getSubTable(self, X_i : str , value : int) -> 'TruthTable':
        '''
        Get the subtable for the given variable and value
        Inputs: Variable and value
        Outputs: Subtable
        '''
        # print(f'{X_i} \t  {value}')
        # print(self.varList)
        index = self.varList.index(X_i)
        # print(f'Index : {index}')
        # List excludes the variable X_i
        newVarList = self.varList[:index] + self.varList[index+1:]
        index = self.numVar - 1 - index
        subTable = []
        for row in range(2 ** len(newVarList)):
            newInputs = [int(x) for x in format(row, '0' + str(len(newVarList)) + 'b')]
            newInputs.insert(index, value)
            subTable.append(self.getOutputs(newInputs))
        return TruthTable(self.numVar - 1, newVarList, subTable)
    
    def printTable(self):
        '''
        Print the Truth Table
        '''
        print("Truth Table", file=outputFile)
        print(f'Variables : {self.varList}', file=outputFile)
        for i in range(2 ** self.numVar):
            inputs = [int(x) for x in format(i, '0' + str(len(self.varList)) + 'b')]
            print(''.join(map(str, inputs)), self.getOutputs(inputs), file=outputFile)
        print(file=outputFile)


def main():
    variableList = ['X', 'Y', 'Z']
    outputList = [0, 0, 0, 0, 1, 1, 1, 1]
    numVar = 3

    truthTable = TruthTable(numVar, variableList, outputList)
    # Print the output for input [0, 0, 1]
    print(f'Output for [0, 0, 1] : {truthTable.getOutputs([0, 0, 1])}')
    # Get the subtable for variable Y and value 1
    subTable = truthTable.getSubTable('Y', 1)
    print("Subtable for Y = 1")
    subTable.printTable()

# if __name__ == '__main__':
#     main()
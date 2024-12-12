from truthTable import TruthTable
from reedMuller import ReedMuller
from solver import Solver
from iterativeSolver import IterativeSolver

def main():
    # listTables = [[1, 1, 1, 1, 0, 0, 0, 0],
	# 		      [0, 1, 1, 0, 0, 0, 1, 1],
    #               [0, 0, 1, 1, 1, 1, 0, 1]]
    # numVar = 3
    # literals = ['x1', 'x2', 'x3']
    outputFile = open('output.txt', 'w')
    finalAns = open('finalAnswer.txt', 'w')
    numVar = 2
    literals = ['x1', 'x2']
    listTables = [[0, 1, 1, 0], [0, 0, 1, 1]]
    
    # Making the function reversible by running the Solver
    solverInstance = Solver(numVar, literals, listTables)
    # tables, size = solverInstance.updateTruthTables()
    tables, size = solverInstance.newListTables, solverInstance.numVar
    # print('Table :')
    # print(type(table[0]))
    tempLiterals = [chr(ord('a') + i) for i in range(size)]
    for table in tables:
        table = TruthTable(size, tempLiterals, table)
        table.printTable()
    print(f'Size : {size}', file = outputFile)

    literals = []
    for i in range(size):
        literals.append(chr(ord('a') + i))  

    # Getting all the Reed Muller Representations
    reedMullerList = []
    # print(type(tables[i]))
    for i in range(size):
        # truthTable = TruthTable(size, literals, tables[i].outputList)
        truthTable = TruthTable(size, tempLiterals, tables[i])
        reedMuller = ReedMuller(truthTable)
        reedMullerList.append(reedMuller)
        # print(f'Function {i+1} : {reedMuller.listOfLists()}')
    
    parameters = [0, 0, -1]
    solver = IterativeSolver(reedMullerList, literals, parameters)
    for step in solver.finalAnswer:
        print(step, file=finalAns)


if __name__ == '__main__':
    main()
"""
Define the function that will run a simulation given a set of test vectors
"""

def runSimulation(wires : dict, nodes : dict):
    testVectors = []
    with open('VerilogSimulator/Data/inputTestVectors.txt', 'r') as file:
        for line in file:
            testVectors.append(line.strip().split(' '))
    
    # Convert test vectors to boolean
    for vector in testVectors:
        for i in range(len(vector)):
            vector[i] = bool(int(vector[i]))
    
    for wire in wires.values():
        for node in wire.sink:
            node.setLevel()
    
    # List of Nodes sorted by level
    # nodes = {name : node for name, node in nodes.items()}
    # nodes = sorted(nodes.values(), key = lambda x : x.level)

    file = open('VerilogSimulator/Data/outputVectors.txt', 'w')

    while testVectors:
        # currInput = testVectors[0]
        # for wire in wires.values():
        #     if wire.wireType == 'input':
        #         wire.setInput(currInput.pop(0))
        # for _, node in nodes.items():
        #     node.evaluate()
        # # for node in nodes:
        # #     node.evaluate()

        # # Do an event driven simulation for the rest
        # for wire in wires.values():
        #     if wire.wireType == 'output':
        #         wire.getOutput()
        #         file.write(wire.name + ' : ' + str(int(wire.out)) + ' ')
        # file.write('\n')
        # testVectors.pop(0)
        currInput = testVectors[0]
        for wire in wires.values():
            if wire.wireType == 'input':
                wire.setInput(currInput.pop(0))
        
        for level in range(max(node.level for node in nodes.values()) + 1):
            for node in nodes.values():
                if node.level == level:
                    node.evaluate()
        
        for wire in wires.values():
            if wire.wireType == 'output':
                wire.getOutput()
                file.write(wire.name + ' : ' + str(int(wire.logicOutput)) + ' ')
        file.write('\n')
        testVectors.pop(0)

    file.close()


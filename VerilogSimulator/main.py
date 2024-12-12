from Net import Net, Node
import re
from objectHelpers import makeGraph, nodeDictionary, wireDictionary
from netlistProcessing import preprocess, patternRecognition
from runSimulation import runSimulation

def main():
    preprocess()
    moduleName, ports, wires, instances = patternRecognition()
    wires = wireDictionary(ports, wires)
    nodes = nodeDictionary(instances, wires)

    print("Created Node Objects:")
    for node in nodes.values():
        print(type(node))

    nodes, wires = makeGraph(nodes, wires)

    print("Created Wire Objects:")
    for wire in wires.values():
        wire.printDetails()

    print("Created Node Objects:")
    for node in nodes.values():
        print(type(node))
        node.printDetails()

    runSimulation(wires, nodes)
    print("Done")


if __name__ == "__main__":
    main()

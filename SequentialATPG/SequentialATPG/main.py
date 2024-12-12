from elementClass import Node, Wire
from instanceClass import Fault, Instance, UnrolledInstance
from netlistPreprocessing import patternRecognition, preprocess
from objectHelpers import wireDictionary, nodeDictionary, makeGraph
from unrollHelper import unrollInstances

def main():
    preprocess()
    _, ports, wires, instances = patternRecognition()
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
    
    unrollInstances(nodes, wires)
    print("Done")


if __name__ == '__main__':
    main()
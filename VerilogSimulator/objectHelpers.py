from Net import Net, Node
import re

def wireDictionary(portMatch : list[any], wireMatch :  list[any]) -> dict:
    wires = {} # Dictionary to hold the wire objects

    # Create wire objects from Port Matches
    for portDir, width, portName in portMatch:
        bitWidth = int(width.strip('[]').split(':')[0]) + 1 if width else 1
        wireType = 'input' if portDir == 'input' else 'output' if portDir == 'output' else 'internal'
        for i in range(bitWidth):
            wireName = portName + '_bitNo_' + str(i)
            wire = Net(wireName, wireType, False)
            wires[wireName] = wire
    
    # Create wire objects from Wire Matches
    for width, wireName in wireMatch:
        bitWidth = int(width.strip('[]').split(':')[0]) + 1 if width else 1
        tempWire = wireName
        for i in range(bitWidth):
            wireName = tempWire + '_bitNo_' + str(i)
            wire = Net(wireName, wireType='internal', out=False)
            wires[wireName] = wire

    return wires


def nodeDictionary(instanceMatch : list[any], wires : dict) -> dict:
    del instanceMatch[0]
    nodes = {} # Dictionary to hold the node objects
    for [moduleName, instanceName, connections] in instanceMatch:
        moduleName = moduleName.strip('()')
        nodes[instanceName] = Node(instanceName, moduleName)
        connPairs = [c.strip() for c in connections.split(',')]
        for conn in connPairs:
            wireName = conn.split('(')[1].split(')')[0]
            wireName = re.sub(r'\[\d+\]$', lambda m : f'_bitNo_{m.group(0)[1:-1]}', wireName) if wireName.endswith(']') else wireName + '_bitNo_0'
            wire = wires[wireName]
            portName = conn.split('(')[0].split('.')[1]

            if portName in {'A', 'B', 'C', 'D', 'S', 'R'}:
                nodes[instanceName].addInput(wire)
            elif portName in {'Y', 'Q'}:
                nodes[instanceName].addOutput(wire)

    return nodes
            

def makeGraph(nodeDict : dict, wireDict : dict) -> tuple[dict, dict]:
    for node in nodeDict.values():
        i = 0
        while i < node.numInputs:
            wire = node.inputs[i]
            if not isinstance(wire, Net):
                i += 1
                continue
            if wire.wireType == 'input':
                i += 1
                continue
            node.addInputNode(wire.source)
            node.removeInput(wire)
    
        i = 0
        while i < node.numOutputs:
            wire = node.outputs[i]
            if not isinstance(wire, Net):
                i += 1
                continue
            if wire.wireType == 'output':
                i += 1
                continue
            node.addOutputNodes(wire.sink)
            node.removeOutput(wire)
    
    # Delete all wire types with wire type internal
    for wire in wireDict:
        print(type(wire))
    wireDict = {name : wire for name, wire in wireDict.items() if wire.wireType != 'internal'}

    return nodeDict, wireDict
        
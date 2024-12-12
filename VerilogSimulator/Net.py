"""
This file contains the class Net, which is used to represent a net in a Verilog
"""
class Net:
    def __init__(self, name : str, wireType : str = 'interal', out : bool = False):
        self.name = name
        self.wireType = wireType
        self.logicOutput = out
        self.source = None # References to a Node
        self.sink = [] # References to a set of Nodes
        self.fanOut = 0 # Number of nodes driven by the net(wire)

    def printDetails(self):
        print(f"Wire: {self.name}")
        print(f"  Type: {self.wireType}")
        print(f"  Number of Fan-outs: {self.fanOut}")
        print("  Fan-outs:")
        for wire in self.sink:
            if isinstance(wire, Net):
                print(f"    Wire: {wire.name}")
            elif isinstance(wire, Node):
                print(f"    Node: {wire.name}")
    
    def addSink(self, node : 'Node'):
        if node not in self.sink:
            self.sink.append(node)
            self.fanOut += 1
    
    def setInput(self, value : bool):
        self.logicOutput = value
    
    def getOutput(self):
        self.logicOutput = self.source.logicOutput
        return self.logicOutput



"""
Class Definition for Node
Nodes for Combinational Circuits will be in Logic Gates

This Class will be used to define every logic gate from the netlist 
"""
from Net import Net

class Node:
    def __init__(self, name: str, nodeType: str, level: int = 0):
        self.name = name
        self.nodeType = nodeType
        self.level = level
        # Define the List of Wire Objects for the Inputs and Outputs
        self.inputs = []
        self.outputs = []
        # Define the number of inputs and outputs
        self.numInputs = 0
        self.numOutputs = 0
        # Define the Logic Output of the Node
        self.logicOutput = False
    
    def evaluate(self) -> None:
        """
        Identify the Type of the Node and evaluate the logic output accordingly
        """
        match self.nodeType:
            case 'NAND':
                self.logicOutput = not (self.inputs[0].logicOutput and self.inputs[1].logicOutput)
            case 'AND':
                self.logicOutput = self.inputs[0].logicOutput and self.inputs[1].logicOutput
            case 'OR':
                self.logicOutput = self.inputs[0].logicOutput or self.inputs[1].logicOutput
            case 'NOR':
                self.logicOutput = not (self.inputs[0].logicOutput or self.inputs[1].logicOutput)
            case 'XOR':
                self.logicOutput = self.inputs[0].logicOutput ^ self.inputs[1].logicOutput
            case 'XNOR':
                self.logicOutput = not (self.inputs[0].logicOutput ^ self.inputs[1].logicOutput)
            case 'NOT':
                self.logicOutput = not self.inputs[0].logicOutput
            case 'BUFF':
                self.logicOutput = self.inputs[0].logicOutput


    def evalForward(self) -> None:
        """
        Evaluate the Logic Output of the Node
        """
        self.evaluate()
        for output in self.outputs:
            if isinstance(output, Net):
                output.setOutput(self.logicOutput)
            elif isinstance(output, Node):
                output.evalForward()

    def eventDrivenSim(self):
        self.evaluate()
        for wire in self.outputs:
            if isinstance(wire, Net):
                wire.setInput(self.logicOutput)
            elif isinstance(wire, Node):
                wire.evalForward()

    def setLevel(self) -> None:
        """
        Set the Level of the Node
        """
        for wire in self.inputs:
            if isinstance(wire, Node):
                if wire.level >= self.level:
                    self.level = wire.level + 1
        for wire in self.outputs:
            if isinstance(wire, Node):
                wire.setLevel()
    
    def addInput(self, wire : Net) -> None:
        """
        Add an Input to the Node
        Input: Wire Object
        """
        if wire not in self.inputs:
            self.inputs.append(wire)
            self.numInputs += 1
            wire.addSink(self)
    
    def addInputNode(self, node : 'Node') -> None:
        """
        Add an Input Node to the Node
        Input: Node Object
        """
        if node not in self.inputs:
            self.inputs.append(node)
            self.numInputs += 1
    
    def removeInput(self, wire : Net) -> None:
        """
        Remove an Input from the Node
        Input: Wire Object
        """
        if wire in self.inputs:
            self.inputs.remove(wire)
            self.numInputs -= 1
    
    def addOutput(self, wire : Net) -> None:
        """
        Add an Output to the Node
        Input: Wire Object
        """
        if wire not in self.outputs:
            self.outputs.append(wire)
            self.numOutputs += 1
            wire.source = self
    
    def addOutputNodes(self, nodes : list['Node']) -> None:
        """
        Add an Output Node to the Node
        Input: Node Object
        """
        for node in nodes:
            if node not in self.outputs:
                self.outputs.append(node)
                self.numOutputs += 1
    
    def removeOutput(self, wire : Net) -> None:
        """
        Remove an Output from the Node
        Input: Wire Object
        """
        if wire in self.outputs:
            self.outputs.remove(wire)
            self.numOutputs -= 1

    def printDetails(self):
        """
        Print the Details of the Node
        """
        print(f"Name: {self.name}")
        print(f"Type: {self.nodeType}")
        print(f"Level: {self.level}")
        print(f"Inputs: {self.numInputs}")
        print(f"Outputs: {self.numOutputs}")
        print(f"Logic Output: {self.logicOutput}")
        print("Inputs:")
        for wire in self.inputs:
            print(f"  {wire.name}")
        print("Outputs:")
        for wire in self.outputs:
            print(f"  {wire.name}")
        print("\n")
    


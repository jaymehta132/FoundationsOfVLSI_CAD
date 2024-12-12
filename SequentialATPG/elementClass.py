"""
Define classes for Wires and Nodes
We modify the classes from the previous project to allow for event driven simulations
We also need to account for a 5 symbol system for each node to check for faults and test patterns
"""

class Wire:
    def __init__(self, name : str, wireType : str ='internal', prevOut : str ='X', out : str = 'X'):
        self.name = name
        self.wireType = wireType
        self.prevOut = prevOut
        self.out = out
        self.source = None
        self.sink = [] # Reference a list of nodes
        self.fanOut = 0 # Counts the number of nodes driven by this wire
    
    def printDetails(self):
        print("Wire Name: ", self.name)
        print(" Wire Type: ", self.wireType)
        print(" Previous Output: ", self.prevOut)
        print(" Output: ", self.out)
        print(" Source: ", self.source)
        print(" Sink: ", self.sink)
        print(" Number of Fan Outs: ", self.fanOut)
        for node in self.sink:
            if isinstance(node, Wire):
                print(f"    Wire : {node.name}")
            elif isinstance(node, Node):
                print(f"    Node : {node.name} Type : {node.nodeType}")

    def concatName(self, name):
        self.name = self.name + name

    def addOutput(self, node : 'Node'):
        if node not in self.sink:
            self.sink.append(node)
            self.fanOut += 1
    
    def removeOutput(self, node : 'Node'):
        if node in self.sink:
            self.sink.remove(node)
            self.fanOut -= 1

    def setInput(self, value : str):
        # Define the input for the wire as the parameter value if the source is None else define it as the source output
        self.prevOut = self.out
        self.out = value if self.source is None else self.source.out

    def getOutput(self) -> str:
        self.prevOut = self.out
        self.out = self.source.out
        return self.out
    
    def evaluate(self, value : str = 'U'):
        self.prevOut = self.out
        evalValue = self.out if value == 'U' else value
        self.out = evalValue if self.source is None else self.source.out

    def eventDrivenSim(self):
        self.evaluate()
        for node in self.sink:
            node.eventDrivenSim()
    
    def forwardEval(self, value : str = 'X'):
        self.evaluate()
        for node in self.sink:
            node.forwardEval()



class Node:
    def __init__(self, name : str, nodeType : str, level : int = 0):
        self.name = name
        self.nodeType = nodeType # Node can be of type 'Logic', 'Register' etc.
        self.inputs = [] # List of Wire Objects 
        self.outputs = [] # List of Wire Objects for the outputs
        self.numInputs = 0
        self.numOutputs = 0
        self.level = level
        self.out = 'X'
        self.prevOut = 'X'
    
    def concatName(self, name : str):
        self.name = self.name + name
    
    def evaluate(self):
        match self.nodeType:
            case 'NAND':
                self.prevOut = self.out
                if self.inputs[0].out == '0' or self.inputs[1].out == '0' or (self.inputs[0].out == 'DBar' and self.inputs[1].out == 'D') or (self.inputs[0].out == 'D' and self.inputs[1].out == 'DBar'):
                    self.out = '1'
                # If any input is unknown, the output is unknown
                elif self.inputs[0].out == 'X' or self.inputs[1].out == 'X':
                    self.out = 'X'
                # Cases where output will be D
                elif (self.inputs[0].out =='DBar' and (self.inputs[1].out == '1' or self.inputs[1].out == 'DBar')) or (self.inputs[1].out == 'DBar' and (self.inputs[0].out == '1' or self.inputs[0].out == 'DBar')):
                    self.out = 'D'
                # Cases where output will be DBar
                elif (self.inputs[0].out =='D' and (self.inputs[1].out == '1' or self.inputs[1].out == 'D')) or (self.inputs[1].out == 'D' and (self.inputs[0].out == '1' or self.inputs[0].out == 'D')):
                    self.out = 'DBar'
                else:
                    self.out = '0'
            
            case 'NOR':
                self.prevOut = self.out
                if self.inputs[0].out == '1' or self.inputs[1].out == '1' or (self.inputs[0].out == 'DBar' and self.inputs[1].out == 'D') or (self.inputs[0].out == 'D' and self.inputs[1].out == 'DBar'):
                    self.out = '0'
                # If any input is unknown, the output is unknown
                elif self.inputs[0].out == 'X' or self.inputs[1].out == 'X':
                    self.out = 'X'
                # Cases where output will be D
                elif (self.inputs[0].out =='DBar' and (self.inputs[1].out == '0' or self.inputs[1].out == 'DBar')) or (self.inputs[1].out == 'DBar' and (self.inputs[0].out == '0' or self.inputs[0].out == 'DBar')):
                    self.out = 'D'
                # Cases where output will be DBar
                elif (self.inputs[0].out =='D' and (self.inputs[1].out == '0' or self.inputs[1].out == 'D')) or (self.inputs[1].out == 'D' and (self.inputs[0].out == '0' or self.inputs[0].out == 'D')):
                    self.out = 'DBar'
                else:
                    self.out = '1'
            
            case 'NOT':
                self.prevOut = self.out
                if self.inputs[0].out == '1':
                    self.out = '0'
                elif self.inputs[0].out == '0':
                    self.out = '1'
                elif self.inputs[0].out == 'D':
                    self.out = 'DBar'
                elif self.inputs[0].out == 'DBar':
                    self.out = 'D'
                else:
                    self.out = 'X'
            
            case 'AND':
                self.prevOut = self.out
                if self.inputs[0] == '0' or self.inputs[1] == '0' or (self.inputs[0] == 'DBar' and self.inputs[1] == 'D') or (self.inputs[0] == 'D' and self.inputs[1] == 'DBar'):
                    self.out = '0'
                # If any input is unknown, the output is unknown
                elif self.inputs[0] == 'X' or self.inputs[1] == 'X':
                    self.out = 'X'
                # Cases where output will be DBar
                elif (self.inputs[0] =='DBar' and (self.inputs[1] == '1' or self.inputs[1] == 'DBar')) or (self.inputs[1] == 'DBar' and (self.inputs[0] == '1' or self.inputs[0] == 'DBar')):
                    self.out = 'DBar'
                # Cases where output will be D
                elif (self.inputs[0] =='D' and (self.inputs[1] == '1' or self.inputs[1] == 'D')) or (self.inputs[1] == 'D' and (self.inputs[0] == '1' or self.inputs[0] == 'D')):
                    self.out = 'D'
                else:
                    self.out = '1'
            
            case 'OR':
                self.prevOut = self.out
                if self.inputs[0] == '1' or self.inputs[1] == '1' or (self.inputs[0] == 'DBar' and self.inputs[1] == 'D') or (self.inputs[0] == 'D' and self.inputs[1] == 'DBar'):
                    self.out = '1'
                # If any input is unknown, the output is unknown
                elif self.inputs[0] == 'X' or self.inputs[1] == 'X':
                    self.out = 'X'
                # Cases where output will be DBar
                elif (self.inputs[0] =='DBar' and (self.inputs[1] == '0' or self.inputs[1] == 'DBar')) or (self.inputs[1] == 'DBar' and (self.inputs[0] == '0' or self.inputs[0] == 'DBar')):
                    self.out = 'DBar'
                # Cases where output will be D
                elif (self.inputs[0] =='D' and (self.inputs[1] == '0' or self.inputs[1] == 'D')) or (self.inputs[1] == 'D' and (self.inputs[0] == '0' or self.inputs[0] == 'D')):
                    self.out = 'D'
                else:
                    self.out = '0'
            
            case 'XOR':
                self.prevOut = self.out
                if self.inputs[0] == 'X' or self.inputs[1] == 'X':
                    self.out = 'X'
                # Cases where the output is D
                elif (self.inputs[0].out == 'D' and self.inputs[1].out == '0') or (self.inputs[0].out == '0' and self.inputs[1].out == 'D') or (self.inputs[0].out == 'DBar' and self.inputs[1].out == '1') or (self.inputs[0].out == '1' and self.inputs[1].out == 'DBar'):
                    self.out = 'D'
                # Cases where the output is DBar
                elif (self.inputs[0].out == 'DBar' and self.inputs[1].out == '0') or (self.inputs[0].out == '0' and self.inputs[1].out == 'DBar') or (self.inputs[0].out == 'D' and self.inputs[1].out == '1') or (self.inputs[0].out == '1' and self.inputs[1].out == 'D'):
                    self.out = 'DBar'
                elif self.inputs[0].out == self.inputs[1].out:
                    self.out = '0'
                else:
                    self.out = '1'
            
            case 'XNOR':
                self.prevOut = self.out
                if self.inputs[0] == 'X' or self.inputs[1] == 'X':
                    self.out = 'X'
                # Cases where the output is D
                elif (self.inputs[0].out == 'D' and self.inputs[1] == '1') or (self.inputs[0].out == '1' and self.inputs[1].out == 'D') or (self.inputs[0].out == 'DBar' and self.inputs[1].out == '0') or (self.inputs[0].out == '0' and self.inputs[1].out == 'DBar'):
                    self.out = 'D'
                # Cases where the output is DBar
                elif (self.inputs[0].out == 'DBar' and self.inputs[1].out == '1') or (self.inputs[0].out == '1' and self.inputs[1].out == 'DBar') or (self.inputs[0].out == 'D' and self.inputs[1].out == '0') or (self.inputs[0].out == '0' and self.inputs[1].out == 'D'):
                    self.out = 'DBar'
                elif self.inputs[0].out == self.inputs[1].out:
                    self.out = '1'
                else:
                    self.out = '0'
            
            case 'BUF':
                self.prevOut = self.out
                self.out = self.inputs[0].out
            
            # Define a fault generator node : 0 if fault free and 1 if faulty
            case 'FGEN':
                self.prevOut = self.out
                if self.inputs[0].out == '0' and self.inputs[1].out == '0':
                    self.out = '0'
                elif self.inputs[0].out == '1' and self.inputs[1].out == '1':
                    self.out = '1'
                elif self.inputs[0].out == '0' and self.inputs[1].out == '1':
                    self.out = 'DBar'
                elif self.inputs[0].out == '1' and self.inputs[1].out == '0':
                    self.out = 'D'
                else:
                    self.out = 'X'
            
            # Define a Positive Edge Triggered D Flip Flop
            case 'DFF':
                if (self.inputs[0].prevOut == '0' and self.inputs[0].out == '1'): # Positive Edge
                    self.prevOut = self.out
                    self.out = self.inputs[1].prevOut
            
            # Define a Postive Edge Triggered D Flip Flop with Asynchronous Set and Reset
            case 'DFFSR':
                if self.inputs[2].out == '1':
                    self.prevOut = self.out
                    self.out = '1'
                elif self.inputs[3].out == '1':
                    self.prevOut = self.out
                    self.out = '0'
                elif (self.inputs[0].prevOut == '0' and self.inputs[0].out == '1'): # Positive Edge
                    self.prevOut = self.out
                    self.out = self.inputs[1].prevOut
    
    def evalForward(self):
        self.evaluate()
        if self.out != self.prevOut:
            for wire in self.outputs:
                wire.evalForward()
    
    def eventDrivenSim(self):
        self.evaluate()
        if self.out != self.prevOut:
            for wire in self.outputs:
                wire.eventDrivenSim()
    
    def setLevel(self):
        for wire in self.inputs:
            if isinstance(wire, Node):
                if self.level >= self.level:
                    self.level = wire.level + 1
        for wire in self.outputs:
            if isinstance(wire, Node):
                wire.setLevel()

    def addInput(self, wire : 'Wire'):
        if wire not in self.inputs:
            self.inputs.append(wire)
            self.numInputs += 1
            wire.addOutput(self) 
    
    def addInputNode(self, node : 'Node'):
        if node not in self.inputs:
            self.inputs.append(node)
            self.numInputs += 1
    
    def removeInput(self, wire : 'Wire'):
        if wire in self.inputs:
            self.inputs.remove(wire)
            self.numInputs -= 1
    
    def replaceInput(self, oldWire : 'Wire', newWire : 'Wire'):
        index = self.inputs.index(oldWire)
        self.inputs[index] = newWire
    
    def addOutput(self, wire : 'Wire'):
        if wire not in self.outputs:
            self.outputs.append(wire)
            self.numOutputs += 1
            wire.source = self
    
    def addOutputNodes(self, nodes : list['Node']):
        for node in nodes:
            if node not in self.outputs:
                self.outputs.append(node)
                self.numOutputs += 1
    
    def removeOutput(self, wire : 'Wire'):
        if wire in self.outputs:
            self.outputs.remove(wire)
            self.numOutputs -= 1

    def delete(self):
        for wire in self.inputs:
            if isinstance(wire, Wire):
                print('Wire Details before Removing Wire')
                wire.printDetails()
                wire.sink.remove(self)
                wire.fanOut -= 1
                print('After Removing the Input Wire')
                wire.printDetails()
            elif isinstance(wire, Node):
                print('Before Removing the Input Node')
                wire.printDetails()
                wire.outputs.remove(self)
                wire.numOutputs -= 1
                print('After Removing the Input Node')
                wire.printDetails()
        
        for wire in self.outputs:
            if isinstance(wire, Wire):
                print('Wire Details before Removing Wire')
                wire.printDetails()
                wire.source = None
                print('After Removing the Input Wire')
                wire.printDetails()
            elif isinstance(wire, Node):
                print('Before Removing the Input Node')
                wire.printDetails()
                wire.inputs.remove(self)
                wire.numInputs -= 1
                print('After Removing the Input Node')
                wire.printDetails()
    
    def printDetails(self):
        print(f"Node: {self.name}")
        print(f"  Type: {self.nodeType}")
        print(f"  Number of Inputs: {self.numInputs}")
        print(f"  Number of Outputs: {self.numOutputs}")
        print(f"  Level: {self.level}")
        print("  Inputs:")
        for wire in self.inputs:
            if isinstance(wire, Wire):
                print(f"    Wire: {wire.name}")
            elif isinstance(wire, Node):
                print(f"    Node: {wire.name} [Type: {wire.nodeType}]")
        print("  Outputs:")
        for wire in self.outputs:
            if isinstance(wire, Wire):
                print(f"    Wire: {wire.name}")
            elif isinstance(wire, Node):
                print(f"    Node: {wire.name} [Type: {wire.nodeType}]")


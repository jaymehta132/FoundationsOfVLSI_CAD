"""
Define class to handle Faults in the Sequential Circuit
"""
from elementClass import Wire, Node
import copy

class Fault:
    def __init__(self, fault : str):
        self.faultType = fault.split('.')[0]

        if self.faultType == 'NODE':
            self.faultNode = fault.split('.')[1]
            self.faultWire = fault.split('.')[2]
            self.faultLoc = 'Output' if self.faultWire == 'Y' else 'Input'
            self.faultIndex = 0 if (self.faultLoc == 'Output' or self.faultWire == 'A') else 1
        elif self.faultType == 'WIRE':
            self.faultNode = fault.split('.')[2]
            self.faultLoc = fault.split('.')[1]
            self.faultIndex = 0
        
        self.SA = fault.split('.')[4] # Value of the stuck-at fault
        self.power = Wire(name='VDD' if self.SA == '1' else 'GND', wireType='POWER', prevOut='X', out=self.SA)
        self.fault = Wire(name='DBar' if self.SA == '1' else 'D', wireType='FAULT', prevOut='X', out='DBar' if self.SA == '1' else 'D')
        self.FGEN = Node(name='FGEN', nodeType='FGEN')
    
    def getPower(self):
        return self.power

    def getFault(self):
        return self.fault

    def printDetails(self):
        print('Fault Type:', self.faultType)
        print('Fault Node:', self.faultNode)
        print('Fault Location:', self.faultLoc)
        print('Fault Index:', self.faultIndex)
    

"""
Define a class for an Instance : A Circuit at an instance in time with all the Pseudo-Primary Inputs and Outputs
"""
class Instance:
    def __init__(self, time : str, PI : dict, PPI : dict, PO : dict, PPO : dict, nodes : dict):
        self.time = time
        self.PI = PI
        self.PPI = PPI
        self.PO = PO
        self.PPO = PPO
        self.nodes = nodes
    
    def setNodeFeedingFault(self, fault : Fault):
        # Defining a faulty node at a particular instance in time
        faultNode = fault.faultNode + '_' + str(self.time)

        if fault.faultType == 'NODE':
            faultNode = self.nodes[faultNode]
            if fault.faultLoc == 'INPUT':
                nodeFeedingFault = faultNode.inputs[fault.faultIndex]
            else:
                nodeFeedingFault = faultNode
        elif fault.faultType == 'WIRE':
            match fault.faultLoc:
                case 'PI':
                    nodeFeedingFault = self.PI[faultNode]
                case 'PPI':
                    nodeFeedingFault = self.PPI[faultNode]
                case 'PO':
                    nodeFeedingFault = self.PO[faultNode].source
                case 'PPO':
                    nodeFeedingFault = self.PPO[faultNode].source
        self.nodeFeedingFault = nodeFeedingFault
    
    def getNodeFeedingFault(self) -> Node:
        return self.nodeFeedingFault
    
    def setFault(self, fault : Fault):
        faultNode = fault.faultNode + '_' + self.time
        if fault.faultType == 'NODE':
            faultNode = self.nodes[faultNode]
            if fault.faultLoc == 'INPUT':
                faultNode.inputs[fault.faultIndex].removeOutput(faultNode)
                faultNode.replaceInput(faultNode.inputs[fault.faultIndex], fault.power)
                fault.power.addOutput(faultNode)
            else:
                for nodeWire in faultNode.outputs[:]:
                    faultNode.removeOutput(nodeWire)
                    if isinstance(nodeWire, Wire):
                        nodeWire.source = fault.power
                        fault.power.addOutput(nodeWire)
                    else:
                        nodeWire.replaceInput(faultNode, fault.power)
                        fault.power.addOutput(nodeWire)
        elif fault.faultType == 'WIRE':
            if fault.faultLoc == 'PI':
                faultWire = self.PI[faultNode]
            elif fault.faultLoc == 'PPI':
                faultWire = self.PPI[faultNode]
            elif fault.faultLoc == 'PO':
                faultWire = self.PO[faultNode]
            elif fault.faultLoc == 'PPO':
                faultWire = self.PPO[faultNode]
            
            if fault.faultLoc == 'PI' or fault.faultLoc == 'PPI':
                for sink in faultWire.sink[:]:
                    if isinstance(sink, Node):
                        faultWire.removeOutput(sink)
                        sink.replaceInput(faultWire, fault.power)
                        fault.power.addOutput(sink)
                    else:
                        sink.source = fault.power
                        fault.power.addOutput(sink)
                    faultWire.sink = []
                    faultWire.fanOut = 0
            else:
                faultWire.source.removeOutput(faultWire)
                faultWire.source = fault.power
                fault.power.addOutput(faultWire)
        fault.power.eventDrivenSim()
    
    def setD(self, fault : Fault):
        faultNode = fault.faultNode + '_' + str(self.time)
        self.setNodeFeedingFault(fault)
        if fault.faultType == 'NODE':
            faultNode = self.nodes[faultNode]
            if fault.faultLoc == 'INPUT':
                faultNode.inputs[fault.faultIndex].removeOutput(faultNode)
                faultNode.replaceInput(faultNode.inputs[fault.faultIndex], fault.FGEN)
                fault.FGEN.addOutput(faultNode)
            else:
                for nodeWire in faultNode.outputs[:]:
                    faultNode.removeOutput(nodeWire)
                    if isinstance(nodeWire, Wire):
                        nodeWire.source = fault.FGEN
                        fault.FGEN.addOutput(nodeWire)
                    else:
                        nodeWire.replaceInput(faultNode, fault.FGEN)
                        fault.FGEN.addOutput(nodeWire)
        elif fault.faultType == 'WIRE':
            if fault.faultLoc == 'PI':
                faultWire = self.PI[faultNode]
            elif fault.faultLoc == 'PPI':
                faultWire = self.PPI[faultNode]
            elif fault.faultLoc == 'PO':
                faultWire = self.PO[faultNode]
            elif fault.faultLoc == 'PPO':
                faultWire = self.PPO[faultNode]
            
            if fault.faultLoc == 'PI' or fault.faultLoc == 'PPI':
                for sink in faultWire.sink[:]:
                    if isinstance(sink, Node):
                        faultWire.removeOutput(sink)
                        sink.replaceInput(faultWire, fault.FGEN)
                        fault.FGEN.addOutput(sink)
                    else:
                        sink.source = fault.FGEN
                        fault.FGEN.addOutput(sink)
                faultWire.sink = [fault.FGEN]
                faultWire.fanOut = 1
            else:
                faultWire.source.removeOutput(faultWire)
                faultWire.source = fault.FGEN
                fault.FGEN.addOutput(faultWire)
        fault.FGEN.addInput(self.getNodeFeedingFault())
        fault.FGEN.addInput(fault.getPower())
        fault.FGEN.eventDrivenSim()

    def setTime(self, time : str):
        self.time = time
        self.PI = {f'{key}_{time}': wire for key, wire in self.PI.items()}
        for wire in self.PI.values():
            wire.concatName(f'_{time}')
        self.PPI = {f'{key}_{time}': wire for key, wire in self.PPI.items()}
        for wire in self.PPI.values():
            wire.concatName(f'_{time}')
        self.PO = {f'{key}_{time}': wire for key, wire in self.PO.items()}
        for wire in self.PO.values():
            wire.concatName(f'_{time}')
        self.PPO = {f'{key}_{time}': wire for key, wire in self.PPO.items()}
        for wire in self.PPO.values():
            wire.concatName(f'_{time}')
        self.nodes = {f'{key}_{time}': node for key, node in self.nodes.items()}
        for node in self.nodes.values():
            node.concatName(f'_{time}')
    
    def printDetails(self):
        print(f'Time : {self.time}')
        print('Primary Inputs:')
        for wire in self.PI.values():
            print(f'    {wire.name} : {wire.out}')
            wire.printDetails()
        print('Primary Pseudo Inputs:')
        for wire in self.PPI.values():
            print(f'    {wire.name} : {wire.out}')
            wire.printDetails()
        print('Primary Outputs:')
        for wire in self.PO.values():
            print(f'    {wire.name} : {wire.out}')
            wire.printDetails()
        print('Primary Pseudo Outputs:')
        for wire in self.PPO.values():
            print(f'    {wire.name} : {wire.out}')
            wire.printDetails()
        print('Nodes:')
        for node in self.nodes.values():
            print(f'    {node.name} : {node.out}')
            node.printDetails()
    
    def joinForward(self, instance : 'Instance'):
        for wire in self.PPO.values():
            for newWire in instance.PPI.values():
                # Wire Name is of the form 'Y_PPO_{time}'
                if wire.name.split('_')[0] == newWire.name.split('_')[0]:
                    wire.sink.append(newWire)
                    wire.fanOut += 1
        
    def removeForward(self):
        for wire in self.PPO.values():
            wire.sink = []
            wire.fanOut = 0
    
    def joinBackward(self, instance : 'Instance'):
        for wire in self.PPI.values():
            for newWire in instance.PPO.values():
                # Wire Name is of the form 'Y_PPI_{time}'
                if wire.name.split('_')[0] == newWire.name.split('_')[0]:
                    wire.source = newWire
    
    def removeBackward(self):
        for wire in self.PPI.values():
            wire.source = None
    


"""
Define a class Unrolled Instance to store the unrolled instances it has a list of instances
"""
class UnrolledInstance:
    def __init__(self):
        self.instances = []
        self.maxUnroll = 0
        self.forwardUnroll = 0
        self.backwardUnroll = 0
        self.fault = None
    
    def getNodeFeedingFault(self):
        for instance in self.instances:
            if instance.time == 0:
                return instance.getNodeFeedingFault()
    
    def initialize(self, instance : Instance, fault = None):
        self.baseInstance = copy.deepcopy(instance)
        DFFCount = len(instance.PPI)
        self.theoryMaxUnroll = 9 ** DFFCount
        instance.setTime(0)
        if fault is not None:
            instance.setD(fault)
        self.instances.append(instance)
        self.maxUnroll = 1
        self.fault = fault
    
    def unrollForward(self, instance : Instance):
        if instance is None:
            instance = copy.deepcopy(self.baseInstance)
        instance.setTime(self.forwardUnroll + 1)
        if self.fault is not None:
            instance.setFault(self.fault)
        self.instances.insert(0, instance)
        self.maxUnroll += 1
        self.forwardUnroll += 1
        self.instances[-2].joinForward(self.instances[-1])
        self.instances[-1].joinForward(self.instances[-2])
    
    def removeForward(self):
        self.instances.pop()
        self.instances[-1].removeForward()
        self.maxUnroll -= 1

        # Remove all sinks of self.fault that end with _{forwardUnroll}
        if self.fault is not None:
            for wire in self.fault.power.sink[:]:
                if wire.name.endswith(f'_{self.forwardUnroll}'):
                    self.fault.power.removeOutput(wire)
        self.forwardUnroll -= 1

    def unrollBackward(self, instance : Instance):
        if instance is None:
            instance = copy.deepcopy(self.baseInstance)
        instance.setTime(-self.backwardUnroll - 1)
        if self.fault is not None:
            instance.setFault(self.fault)
        self.instances.insert(0, instance)
        self.maxUnroll += 1
        self.backwardUnroll += 1
        self.instances[0].joinForward(self.instances[1])
        self.instances[1].joinBackward(self.instances[0])
    
    def removeBackward(self):
        self.instances.pop(0)
        self.instances[0].removeBackward()
        self.maxUnroll -= 1
        if self.fault is not None:
            for wire in self.fault.power.sink[:]:
                if wire.name.endswith(f'_{self.backwardUnroll}'):
                    self.fault.power.removeOutput(wire)
        self.backwardUnroll -= 1

    def ATPG(self, time = 0, PI = None):
        for instance in self.instances:
            if instance.time == time:
                tempInstance = instance
        
        newPI = {**(PI if PI is not None else {}), **(tempInstance.PI if tempInstance.PI is not None else {})}

        for PO in tempInstance.PO.values():
            while self.instances[0].time != 0:
                self.removeBackward()
            self.setAllX(newPI)
            self.setAllX(self.instances[0].PPI)

            if self.PODEM(PO, ['D', 'DBar'], newPI, self.instances[0].PPI):
                return True
        
        flag = False
        for PPO in tempInstance.PPO.values():
            while self.instances[0].time != 0:
                self.removeBackward()
            self.setAllX(newPI)
            self.setAllX(self.instances[0].PPI)
            if self.PODEM(PPO, ['D', 'DBar'], newPI, self.instances[0].PPI):
                flag = True
                break
        
        if not flag: 
            return False
        
        if self.maxUnroll == self.theoryMaxUnroll:
            return False
        
        self.unrollBackward()
        self.fault.power.eventDrivenSim()

        if self.ATPG(time + 1, newPI):
            return True
        
        self.removeForward()
        return False
   
    # Define a function to execute PODEM on the Instance
    def PODEM(self, wireNode : Node, desiredValues) -> bool:
        if wireNode is None:
            return False
        
        if isinstance(wireNode, Wire):
            if wireNode.wireType == 'INPUT' or wireNode.wireType == 'PSUEDO_INPUT':
                if desiredValues[0] not in ['0', '1']:
                    return False
                wireNode.setInput(desiredValues[0])
                return True
            return self.PODEM(wireNode.source, desiredValues)

        # Define a dictionary to track the inverting gates encountered during PODEM
        PINoInv = {}
        PPINoInv = {}
        for wire in self.PI.values():
            PINoInv[wire] = -1
        for wire in self.PPI.values():
            PPINoInv[wire] = -1
        
        # Perform a BFS on wireNode to find th number of Inverting Gates to reach PI and PPI
        queue = [[wireNode, 0]]
        visited = set()
        visited.add(wireNode)

        while queue:
            curr = queue.pop(0)
            node = curr[0]
            inputs = node.inputs if isinstance(node, Node) else [node.source]
            for wire in inputs:
                if isinstance(wire, Wire):
                    if wire not in visited:
                        queue.append([wire, curr[1]])
                        visited.add(wire)
                    
                    if wire in self.PI.values():
                        PINoInv[wire] = curr[1]
                    elif wire in self.PPI.values():
                        PPINoInv[wire] = curr[1]
                elif isinstance(wire, Node):
                    if wire not in visited:
                        if wire.nodeType in ['NOT', 'NAND', 'NOR']:
                            queue.append([wire, curr[1] + 1])
                        else:
                            queue.append([wire, curr[1]])
                        visited.add(wire)
        
        return self.backtrack(PINoInv, PPINoInv, wireNode, desiredValues, 0)

    def checkAllX(self, PPI):
        for wire in PPI.values():
            if wire.out != 'X':
                return False
        return True


    def setAllX(self, L):
        for wire in L.values():
            wire.setInput('X')
            wire.eventDrivenSim()
    
        # Define the backtrack function : try PI or PPI 
    def backtrack(self, PINoInv : dict, PPINoInv : dict, wireNode : Node, desiredValues, i : int, PI, PPI) -> bool:
        # Extract wires from PI or PPI
        if i < len(self.PI):
            wire = list(self.PI.values())[i]
            noInv = PINoInv[wire]
        elif i < len(self.PPI) + len(self.PI):
            wire = list(self.PPI.values)[i - len(self.PI)]
            noInv = PPINoInv[wire]
        else:
            return False

        # Not found in path to PI
        if noInv == -1:
            return self.backtrack(PINoInv, PPINoInv, wireNode, desiredValues, i + 1)
        
        # Get the input value based on the node type and desired value
        wire.setInput(self.getInputValue(wireNode.nodeType, desiredValues, noInv % 2))
        wire.eventDrivenSim() 
        # If the desired value is achieved, return True
        if wireNode.out in desiredValues:
            if self.checkAllX(PPI):
                return True
            if self.maxUnroll == self.theoryMaxUnroll:
                return False
            self.unrollBackward()
            self.setAllX(PPI)
            self.setAllX(PI)
            self.fault.power.eventDrivenSim()
            return self.PODEM(wireNode, desiredValues, {**PI, **self.instances[0].PI}, self.instances[0].PPI)
        # Here it is possible to achieve the desired value
        if wireNode.out == 'X':
            if self.backtrack(PINoInv, PPINoInv, wireNode, desiredValues, i + 1):
                return True
        
        # Try other values if desired value is not possible to achieve
        wire.setInput('0' if wire.out == '1' else '1')
        wire.eventDrivenSim()

        if wireNode.out in desiredValues:
            if self.checkAllX(PPI):
                return True
            if self.maxUnroll == self.theoryMaxUnroll:
                return False
            self.unrollBackward()
            self.setAllX(PPI)
            self.setAllX(PI)
            self.fault.power.eventDrivenSim()
            return self.PODEM(wireNode, desiredValues, {**PI, **self.instances[0].PI}, self.instances[0].PPI)
        
        if wireNode.out == 'X':
            if self.backtrack(PINoInv, PPINoInv, wireNode, desiredValues, i + 1):
                return True
        
        wire.setInput('X')
        wire.eventDrivenSim()
        # If the desired value is not achieved then retur False
        return False
  
    def printDetails(self):
        print(f"Max Unroll: {self.maxUnroll}")
        print(f"Forward Unroll: {self.forwardUnroll}")
        print(f"Backward Unroll: {self.backwardUnroll}")
        print(f"Number of Instances: {len(self.instances)}")
        for instance in self.instances:
            instance.printDetails()
    
    def delete(self):
        for instance in self.instances:
            del instance
        self.instances = []
        self.maxUnroll = 0
        self.forwardUnroll = 0
        self.backwardUnroll = 0

    # Define a function to obtain the input value based on the node type and the desired output
    def getInputValue(self, nodeType : Node, desiredValue, parity : int):
        desiredValue = desiredValue[0] if desiredValue[0] not in ['D', 'DBar'] else 'NONCONTROL'
        inputMap = {
            'OR' : '1' if desiredValue == '1' else '0',
            'NOR': '1' if desiredValue == '0' else '0',
            'AND': '0' if desiredValue == '0' else '1',
            'NAND': '0' if desiredValue == '1' else '1',
            'NOT': '0' if desiredValue == '1' else '1',
        }
        negateMap = {'0' : '1', '1' : '0'}

        return inputMap.get(nodeType, '0') if parity == 0 else negateMap.get(inputMap.get(nodeType, '0'))
            

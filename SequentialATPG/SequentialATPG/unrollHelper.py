from elementClass import Wire, Node
from instanceClass import Fault, Instance, UnrolledInstance
import copy


def unrollInstances(nodeDict : dict, wireDict : dict):
    # Split the wires into dictionaries depending upon their type
    PI = {name : wire for name, wire in wireDict.items() if wire.wireType == 'INPUT'}
    PPI = {name : wire for name, wire in wireDict.items() if wire.wireType == 'PSEUDOINPUT'}
    PO = {name : wire for name, wire in wireDict.items() if wire.wireType == 'OUTPUT'}
    PPO = {name : wire for name, wire in wireDict.items() if wire.wireType == 'PSEUDOOUTPUT'}

    # Define the default instance
    defaultInstance = Instance(0, PI, PPI, PO, PPO, nodeDict)

    baseInstance = copy.deepcopy(defaultInstance)

    # Generate faults for all the nodes and wires
    faults = []
    for node in nodeDict:
        for wire in ['A', 'B']:
            if nodeDict[node].nodeType == 'NOT' and wire == 'B':
                continue
            faults.append(Fault(f'NODE.{node}.{wire}.SA.0'))
            faults.append(Fault(f'NODE.{node}.{wire}.SA.1'))
        for wire in ['Y']:
            faults.append(Fault(f'NODE.{node}.{wire}.SA.0'))
            faults.append(Fault(f'NODE.{node}.{wire}.SA.1'))
    for wire in PI:
        faults.append(Fault(f'WIRE.PI.{wire}.SA.0'))
        faults.append(Fault(f'WIRE.PI.{wire}.SA.1'))
    for wire in PPI:
        faults.append(Fault(f'WIRE.PPI.{wire}.SA.0'))
        faults.append(Fault(f'WIRE.PPI.{wire}.SA.1'))
    for wire in PO:
        faults.append(Fault(f'WIRE.PO.{wire}.SA.0'))
        faults.append(Fault(f'WIRE.PO.{wire}.SA.1'))
    for wire in PPO:
        faults.append(Fault(f'WIRE.PPO.{wire}.SA.0'))
        faults.append(Fault(f'WIRE.PPO.{wire}.SA.1'))
    
    unrolledInstance = UnrolledInstance()
    unrolledInstance.initialize(copy.deepcopy(baseInstance))

    # Open file for writing in the outputs
    file = open('SequentialATPG/Data/Output.txt', 'w')
    file.write("Primary Inputs: \n")
    for wire in PI.values():
        file.write(f'\t\t{wire.name}')
    file.write("Primary Outputs: \n")
    for wire in PO.values():
        file.write(f'\t\t{wire.name}')
    file.write('\n\n\n')

    for fault in faults:
        unrolledInstance = UnrolledInstance()
        unrolledInstance.initialize(copy.deepcopy(baseInstance), fault)
        fault.getPower().eventDrivenSim()
        flag = unrolledInstance.ATPG()
        if not flag:
            file.write(f'Fault {fault.faultNode}.{fault.faultLoc}.{fault.faultIndex}.{fault.SA} : Undetectable')
        else:
            file.write(f"Fault at {fault.fault_loc} number {fault.fault_index} of {fault.fault_node} stuck at {fault.sa} is detectable\n")
            file.write(f"Test Vectors are: \n")
            for instance in unrolledInstance.instances:
                file.write(f"\t\t")
                for PI in instance.PI.values():
                    file.write(f"{PI.out}\t\t")
                file.write(f"\n")
            file.write(f"Final Output Vectors are: ")
            for PO in unrolledInstance.instances[-1].PO.values():
                file.write(f"{PO.out}\t\t")
            file.write("\n\n")
    file.close()

import re

def preprocess() -> None:
    """
    Preprocesses the netlist file to remove comments, empty lines and tabs
    """
    with open("VerilogSimulator/Data/netlist.v", "r") as file:
        lines = file.read()
    # Remove the comments
    lines = re.sub(r'\(\*.*?\*\)','', lines, flags=re.DOTALL)
    lines = re.sub(r'/\*.*?\*/','', lines, flags=re.DOTALL)
    # Remove tabs and newlines
    lines = lines.replace('\t', '')
    lines = lines.replace('\n', '')
    lines = re.sub(r'\s+', ' ', lines)

    with open("VerilogSimulator/Data/processed.txt", "w") as file:
        file.write(lines)



def patternRecognition() -> list[list[tuple]]:
    """
    Recognizes patterns in the processed netlist file
    """
    with open("VerilogSimulator/Data/processed.txt", "r") as file:
        data = file.read()
    
    # Example pattern to find module definitions
    modulePattern = r"module\s+(\w+)\s*\((.*?)\);"
    portPattern = r"(input|output|inout)\s+(?:wire|reg)?\s*(\[\d+:\d+\])?\s*(\w+);"
    wirePattern = r"wire\s+(\[.*?\])?\s*(\w+);"
    instancePattern = r"(\w+)\s+(\w+)\s*\((.*?)\);"
    # Extract the module name and ports
    module = re.search(modulePattern, data, re.DOTALL)
    moduleName = module.group(1)
    ports = re.findall(portPattern, data, re.DOTALL)
    wires = re.findall(wirePattern, data, re.DOTALL)
    instances = re.findall(instancePattern, data, re.DOTALL)
    # Return the module name, ports, wires and instances
    return [moduleName, ports, wires, instances]


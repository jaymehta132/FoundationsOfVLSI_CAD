# Verilog Simulator

This project is a Python-based Verilog simulator that utilizes Yosys to convert Verilog files into netlists and simulates the required test vectors.

## Features
- Converts Verilog source files into netlists using Yosys.
- Simulates test vectors based on the provided Verilog file.
- Supports automation through the `main.py` script.

## Prerequisites

- Python 3.x
- [Yosys](https://yosyshq.net/yosys/) (to convert Verilog files to netlists)

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/verilog-simulator.git
   cd verilog-simulator
   ```

2. **Install required Python packages**:

   ```bash
   pip install -r requirements.txt
   ```

   (Ensure you include a `requirements.txt` file with the necessary Python dependencies, if any.)

3. **Install Yosys**:

   You can install Yosys following the instructions on its [official website](https://yosyshq.net/yosys/).

## Usage

1. **Convert Verilog file to netlist**:

   The first step is to provide a Verilog file, which will be converted into a netlist using Yosys.

   ```bash
   yosys 
   read -vlog2k Data/verilogFile.v
   hierarchy -top <top_entity_name>
   flatten
   proc; opt -full
   fsm; opt -full
   memory; opt -full
   techmap; opt
   dfflib -liberty cmos_cells.lib
   abc -liberty cmos_cells.lib
   clean
   write_verilog Data/netlist.v
   ```

2. **Run Simulation**:

   After generating the netlist, run the `main.py` file to simulate the test vectors.

   ```bash
   python3 main.py
   ```

   This will simulate the provided Verilog design and output the results of the test vectors.

## Directory Structure

```
verilog-simulator/
│
├── main.py              # Main script to run simulations
├── README.md            # Project documentation
├── Data                 # Contains the data files
     ├── inputTestVectors.txt               
     ├── netlist.v
     ├── outputVectors.txt
     ├── processed.txt
     └── verilogFile.v
├── runSimulation.py     # Function to run the simulation
├── objectHelpers.py     # Functions to make the simulation graph
├── netlistProcessing.py # Convert the netlist into a processable format for ease
├── cmos_cells.lib       # File important for running yosys command
└── Net.py               # Contains Class definitions

```

## Contributing

Feel free to contribute by submitting pull requests or reporting issues!


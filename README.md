# Foundations of VLSI-CAD

This repository contains the assignments as well as project submissions for the **EE677: Foundations of VLSI CAD** course by Prof. Virendra Singh. The first assignment is the Verilog Simulator wherein we simulate the working of a Combinational Logic Circuit for given Inputs. The second assignment is the Sequential ATPG wherein we automatically generate Test Vectors for specific faults in a Sequential Logic Circuit. The project involved making a Quantum Circuit Synthesiser based on given required output functions.

## Team Members

- **Jay Mehta**
- **Kshitij Vaidya**
- **Kushal Jain**
- **Jainam Ravani**

## Overview

### Verilog Simulator 

The Verilog Simulator takes a verilog file as its input and processes it to produces a graph with a topological order of the circuit. It then simulates the circuit for given input vectors and produces the corresponding output vectors. The `README.md` file in the folder `VerilogSimulator` contains further information about this.

### Sequential ATPG

The Sequential ATPG takes a verilog file as its input and converts it into a graph and also stores the fault. It then runs the ATPG algorithm to produce test vectors for the given fault. 

### Quantum Circuit Synthesis

The Quantum Circuit Synthesiser converts input truth tables to a quantum circuit with as low quantum wires as possible using a greedy approach similar to BFS. Further information on it is given in the file `finalReport.pdf` under the `QuantumCircuitSynthesis` folder.

## Repository Structure

```plaintext                
├── QuantumCircuitSynthesis/                   
│   ├── compileNotebook.ipynb     
│   ├── finalAnswer.txt
│   ├── finalReport.pdf
│   ├── iterativeSolver.py
│   ├── main.py
│   ├── output.txt
│   ├── reedMuller.py
│   ├── solver.py
│   ├── truthTable.py    
├── SequentialATPG/
│   ├── cmos_cells.lib
│   ├── elementClass.py
│   ├── instanceClass.py
│   ├── main.py
│   ├── netlistProcessing.py
│   ├── objectHelpers.py
│   ├── unrollHelper.py                   
│   ├── Data/
│   │   ├── inputTestVectors.txt
│   │   ├── netlist.v
│   │   ├── Output.txt
│   │   ├── outputVectors.txt
│   │   ├── processed.txt
│   │   ├── verilogFile.v
├── VerilogSimulator/
│   ├── cmos_cells.lib
│   ├── main.py
│   ├── Net.py
│   ├── netlistProcessing.py
│   ├── objectHelpers.py
│   ├── README.md
│   ├── runSimulation.py             
│   ├── Data/
│   │   ├── inputTestVectors.txt
│   │   ├── netlist.v
│   │   ├── outputVectors.txt
│   │   ├── processed.txt
│   │   ├── verilogFile.v    
└── README.md             
```

## How to Use

1. **Clone the Repository**
   ```bash
   git clone https://github.com/jaymehta132/FoundationsOfVLSI_CAD/foundations_of_vlsi_cad.git
   cd foundations_of_vlsi_cad
   ```
2. **Simulate**
      - Run the `main.py` file for each assignment/project.
3. **Analyze Results**
     - Check the outputs and analyse.
4. **Modify**
     - Use the modular Python code for further enhancements or experiments.

## Acknowledgements
We would like to thank Prof. Virendra Singh for his guidance throughout the course.
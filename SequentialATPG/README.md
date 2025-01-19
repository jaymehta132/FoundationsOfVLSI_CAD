# Sequential ATPG (Automatic Test Pattern Generation)

This project implements a Python-based Sequential ATPG (Automatic Test Pattern Generation), which is extensively used for generating test vectors to detect faults in sequential circuits. The tool leverages PODEM (Path-Oriented Decision Making) to efficiently generate test patterns, which is a commonly used algorithm in ATPG for combinational and sequential circuit testing.

## What is ATPG?

ATPG is a process used in digital circuit testing to automatically generate a set of test vectors (input patterns) that can be used to detect faults in the circuit. ATPG tools typically focus on two types of faults: **stuck-at faults** and **transition faults**, where the circuit elements may behave incorrectly due to defects.

### PODEM Algorithm

PODEM is a key algorithm used in ATPG, designed to minimize the backtracking required in path sensitization. It works by attempting to justify the input values required to activate and propagate a fault to an output, ensuring that the fault can be detected by observing the output behavior. In this project, PODEM is heavily used to tackle both combinational and sequential circuit fault detection, making it more efficient compared to brute-force methods.

## Features
- **PODEM-based ATPG**: Efficient fault detection using the PODEM algorithm.
- Generates test vectors for sequential circuits to identify various fault types.
- Supports automation through Python scripts and easy integration with simulation environments.

## Prerequisites

- Python 3.x
- [Yosys](https://yosyshq.net/yosys/) (For generation of the Verilog Netlist)

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/sequential-atpg.git
   cd sequential-atpg
   ```

2. **Install Yosys**:

   You can install Yosys following the instructions on its [official website](https://yosyshq.net/yosys/).

## Usage

1. **Generate Test Patterns**:

   The tool utilizes the PODEM algorithm to generate test vectors for detecting faults in sequential circuits. Run the `main.py` file to start the test generation process.

   ```bash
   python3 main.py
   ```

   The generated test vectors will be saved and can be used in the simulation to verify the circuit's behavior under various fault conditions.

2. **Simulation**:

   After generating the test vectors, you can use them with your preferred simulation tool to validate the fault coverage and correctness of the circuit design.

## Directory Structure

```
sequential-atpg/
│
├── main.py               # Main script to generate test patterns using PODEM
├── README.md             # Project documentation
├── Data                  # Contains input/output data files
│    ├── verilogFile.v    # Verilog file for the sequential circuit
│    ├── netlist.v        # Contains the generated Netlist
│    ├── processed.txt    # Intermediate file containing cleaned up Netlist
│    ├── testVectors.txt  # Generated test vectors
│    └── Output.txt       # Fault description file
├── instanceClass.py
├── netlistPreprocessing.py
├── objectHelpers.py
├── unrollHelper.py
└── elementClass.py
```

## Contributing

Contributions are welcome! If you have improvements or suggestions, feel free to submit pull requests or report issues.

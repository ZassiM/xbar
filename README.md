# Xbar netlist generator for SPICE simulator

This python script generates a netlist on a SCS file which can be used by the Cadence Virtuoso Spectre to simulate it behavior. The netlist describes a memristor crossbar whose parameteres are user-defined through a separated config file (CSV format). The memristor model used by the simulator is written with Verilog-A (JART VCM V1b var, see description here http://www.emrl.de/JART.html#Artikel_4). It considers device-to-device and cycle-to-cycle variability.
At the moment, you can define the xbar size (rows, columns), the variability parameters, the simulation parameters and the input pulses for each row and column.

How to generate netlist:
Open the config file;
Input the preferred parameters values, a comment indicates the parameter name;
Save the config file;
Run the main.py script and read the textual feedback for success/error messages.
The netlist is written on a SCS file.

How to run the spectre simulator via terminal:
Open a terminal on a ICE machine;
Type 'module load cadence-flow/mixed-signal/2020-21';
Enter to the directory which contains the SCS file;
Run 'spectre <file-name>.scs';
You'll get the simulation results via textual information, and a .raw file is generated which can be used to visualize the waveforms.

How to visualize the output waveforms:
Open a terminal on a ICE machine;
Type 'module load spectre/18.10' and 'module load ic/6.1.8'
Type 'virtuoso'
After Virtuoso is opened, click on Tools->VIVA XL->Waveforms
After VIVA is opened, click on File->Open results, and select the RAW file generated before to view the waveforms.




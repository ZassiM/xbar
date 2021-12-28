from ckt_gen import netlist_design
from gauss_var import gauss_dist
from parameters import parameters
import numpy as np
import csv

"""
This is the main function which defined the flow of code by calling different classes in it.
"""
print()

out_file_name = "computing.scs" # file name of netlist
ckt = netlist_design()  # object of the netlist class
#gauss = gauss_dist()    # gauss distribution object

# mean and sigma of each variablity parameter
mean_sigma = { "Ndiscmin": (8e-03, 2e-3), "Ndiscmax": (20, 1), "lnew": (0.4, 0.04), "rnew": (45e-09, 5e-09)}

# static parameters which are required for internal calculation
static_param_sim = " eps = 17 epsphib = 5.5 Ndiscmin=0.008" 


# static parameters value. 
static_param = {"eps": 17,"epsphib":5.5,"phibn0":0.18, "phin":0.1,"un":4e-06,
		 "Ndiscmax":20,"Ndiscmin": 0.008,"Ninit": "Ndiscmin","Nplug": 20,
		 "a": 2.5e-10,"nyo": 2e+13, "dWa": 1.35, "Rth0": 1.572e+07,
		 "rdet": 4.5e-08, "rnew": 4.5e-08, 'lcell': 3, 'ldet': 0.4,
		 'lnew': 0.4, "Rtheff_scaling": 0.27, "RTiOx": 650, "R0": 719.244,
	     'Rthline': 90471.5, 'alphaline': 0.00392, "eps_eff": "(eps)*(8.85419e-12)",
	        'epsphib_eff': "(epsphib)*(8.85419e-12)"}

# parameter real eps	= 17 from [10:25]; 						// static hafnium oxide permittivity 
# parameter real epsphib	  =  5.5;							// hafnium oxide permittivity related to image force barrier lowering
# parameter real phibn0 	= 0.18 from [0.1:0.5];				// nominal schottky barrier height [eV]
# parameter real phin  	= 0.1	from [0.1:0.3];					// energy level difference between the Fermi level in the oxide and the oxide conduction band edge [eV]
# parameter real un	= 4e-6	from [1e-6:1e-5];				// electron mobility [m^2/Vs]
# parameter real Ndiscmax	= 20	 from [0.001:1100];				// maximum oxygen vacancy concentration in the disc[10^26/m^3]
# parameter real Ndiscmin	= 0.008	 from [0.0001:100];			// minimum oxygen vacancy concentration in the disc [10^26/m^3]
# parameter real Ninit = 0.008	from [0.0001:1000];				// initial oxygen vacancy concentration in the disc [10^26/m^3]
# parameter real Nplug = 20 from [0.001:100];					// oxygen vacancy concentration in the plug [10^26/m^3]
# parameter real a	= 0.25e-9 from [0.1e-9:1e-9];					// ion hopping distance [m]
# parameter real nyo	= 2e13 from [1e10:1e14];					// attemp frequenzy [Hz]
# parameter real dWa	= 1.35 from [0.8:1.5];					// activation energy [eV]
# parameter real Rth0  = 15.72e6 from [1e6:20e6];				// thermal resistance of the Hafnium Oxide [K/W]
# parameter real rdet = 45e-9 	from [5e-9:100e-9];				// radius of the filament [m]
# parameter real rnew = 45e-9 from [5e-9:100e-9];				// radius of the filament [m]
# parameter real lcell	= 3	from [2:5];							// length of disc and plug region [nm]
# parameter real ldet 	= 0.4 	from [0.1:5]; 					// length of the disc region [nm]
# parameter real lnew 	= 0.4 	from [0.1:5]; 					// length of the disc region [nm]
# parameter real Rtheff_scaling = 0.27 from [0.1:1];				// scaling factor for RESET 
# parameter real RTiOx = 650 from [0:5000]; 						// series resistance of the TiOx layer[Ohm]
# parameter real R0 = 719.2437;									//  Resistance at T0 [Ohm}
# parameter real Rthline = 90471.47;							// thermal conductivity of the Platinum and Titanium [W/mK]
# parameter real alphaline = 3.92e-3;							// temperature coefficient [1/K]
# parameter real eps_eff=eps*`P_EPS0; 							// static hafnium oxide permittivity 
# parameter real epsphib_eff=epsphib*`P_EPS0; 					// hafnium oxide permittivity related to image force barrier lowering

read = 0
volt_r = []
volt_c = []

with open('config.txt', 'r') as csv_file:
    config = csv.reader(csv_file)
    
    for c in config:
        if(not c or c[0][0]=='#'):  #skip empty line or comment
            if read == 4 or read == 5:
                read += 1
            continue

        elif read != 4 and read != 5:
            read += 1

        if read == 1:
            rows, columns = (int(c[0]), int(c[1]))

        if read == 2:
            nmin_b, nmax_b, ldet_b, rdet_b = (int(c[0]), int(c[1]), int(c[2]), int(c[3]))

        if read == 3:
            sim_type, stop_time, max_step = (c[0]), c[1], (c[2])
        
        if read == 4:
            volt_r.append(c)        

        if read == 5:
            volt_c.append(c)


#set the size of crossbar rows and columns 
cross_bar = ckt.set_cross_bar_params(rows, columns) #set the size of crossbar 


#Tune the simulation parameters  - duration of simulation and step you want to take
ckt.set_simulation_params(sim_type, stop_time, max_step) # set simulation type and stoptime

# print("Set variability for each of 4 parameters: (0->False, 1->True)")
# variab = str(input())

# # set variabltiy - we can check the effect of variation using single or multiple parameter variation
# bools_var = ckt.set_variablity(Nmin=(variab[0]=='1'), Nmax=(variab[1]=='1'), ldet=(variab[2]=='1'), rdet=(variab[3]=='1'))
#bools_var = ckt.set_variablity(Nmin=False, Nmax=False, ldet=False, rdet=False) 
# Creates dictionary of the form {"Ndiscmin": Nmin, "Ndiscmax": Nmax, "rnew": rdet,"lnew": ldet
# It is used by the update_param function to generate var_param to put on the top of the netlist, and also to 
bools_var = ckt.set_variablity(Nmin = nmin_b, Nmax = nmax_b, ldet = ldet_b, rdet = rdet_b) 


# set type of input to crossbar and control the other variables
#ckt.set_input_voltages(type_="pulse", vol0=-2, vol1=1.2, time_period="200n", pulse_width="50n", rise_time = "25n", fall_time="25n")
ckt.set_input_voltages(volt_r, volt_c)
#ckt.set_input_voltages(type_="pulse", vol0, vol1, time_period, pulse_width, rise_time, fall_time)

# check for variation and create a string for the first part of the netlist: if there are variations,
# it will contain the variation parameters for each memristor in the xbar to be used then to 
# define the instances of each memristor, plus the static parameters used by the simulator (eps epsphib and Ndiscmin)
var_param = ckt.update_param(static_param_sim, mean_sigma, bools_var)

# create spectre netlist using the parameters set before and the static and variab parameters
netlist = ckt.design_ckt(variables = var_param,static_param = static_param) 

# write into file, name of file can be given as argument - (file_name = "auto_generated.scs")
ckt.write_into_file(file_name = out_file_name, to_be_written= netlist)  


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

params_read = 0 # number of parameters read on the csv format file
volt_r, volt_c = [], [] # 


csv_file = open('config.txt', 'r')  
config = csv.reader(csv_file)

for c in config: # read line per line from the csv file
	if(not c or c[0][0]=='#'):  # skip empty line or comment
		if params_read == 4 or params_read == 5:  # used to correctly pass from row to columns voltage read
			params_read += 1
		continue

	elif params_read != 4 and params_read != 5:	
		params_read += 1

	if params_read == 1:	# rows and columns params
		try:
			rows, columns = (int(c[0]), int(c[1]))
			#set the size of crossbar rows and columns 
			cross_bar = ckt.set_cross_bar_params(rows, columns) # set xbar size
		except:
			print("Rows and columns are set to default!\n")
			cross_bar = ckt.set_cross_bar_params()
		
	if params_read == 2:	# variability bools
		try:
			nmin_b, nmax_b, ldet_b, rdet_b = (int(c[0]), int(c[1]), int(c[2]), int(c[3]))
			bools_var = ckt.set_variablity(Nmin = nmin_b, Nmax = nmax_b, ldet = ldet_b, rdet = rdet_b)	# create dict with variability params bools

		except:
			print("Variability parameters are disabled by default!\n")
			bools_var = ckt.set_variablity()
		
		# use the dict created before to generate a string containing the (eventual) updated parameters used for the memristor instances
		var_param = ckt.update_param(static_param_sim, mean_sigma, bools_var)

	if params_read == 3:	# simulation parameters
		try:
			sim_type, stop_time, max_step = (c[0]), c[1], (c[2])
			# tune the simulation parameters  - duration of simulation and step you want to take
			ckt.set_simulation_params(sim_type, stop_time, max_step) # set simulation type, stoptime and max step
		except:
			print("Simulation parameters are set to default!\n")

	if params_read == 4:	# row voltage pulses
		volt_r.append(c)     

	if params_read == 5:	# columns voltage pulses
		volt_c.append(c)

	
csv_file.close()

# set input voltages using the list read by the file
ckt.set_input_voltages(volt_r, volt_c)

# create spectre netlist using the parameters set before and the static and variab parameters
netlist = ckt.design_ckt(var_param, static_param) 

# write into file, name of file can be given as argument - (file_name = "auto_generated.scs")
ckt.write_into_file(out_file_name, netlist)  


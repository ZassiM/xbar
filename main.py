from ckt_gen import netlist_design
import json
import pandas as pd
import os

"""
This is the main function which defined the flow of code by calling different classes in it.
"""
print()

out_file_name = "netlist.scs" # file name of netlist
model_path =os.getcwd() + '\\' # change this path according to local path
ckt = netlist_design()  # object of the netlist class

mean_sigma = { "Ndiscmin": (8e-03, 2e-3), "Ndiscmax": (20, 1), "lnew": (0.4, 0.04), "rnew": (45e-09, 5e-09)}	# mean and sigma of each variablity parameter

static_param_sim = " eps = 17 epsphib = 5.5 Ndiscmin=0.008"	# static parameters which are required for internal calculation

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

with open('config.json', 'r') as f:
	config = json.load(f)

	rows, columns = config['xbar_sizes']['rows'], config['xbar_sizes']['columns']	# read rows and columns

	nmin_b, nmax_b, ldet_b, rdet_b = config['var_bools']['ndiscmin'], config['var_bools']['ndiscmax'], config['var_bools']['ldet'], config['var_bools']['rdet']	# create dict with variability params bools

	sim_type, stop_time, max_step = config['sim_params']['type'], config['sim_params']['stop_time'], config['sim_params']['max_step']	# tune the simulation parameters  - duration of simulation and step you want to take

	model_path += config['sim_params']['model_file']

pulses = pd.read_csv('pulses.csv',skip_blank_lines=False)

pulses_list = pulses.values.tolist()
to_col = 0
for r in pulses_list:
	if str(r[0]) == 'nan':
		to_col = 1
		continue
	if to_col == 0:
		volt_r.append(r)
	else:
		volt_c.append(r)


cross_bar = ckt.set_cross_bar_params(rows, columns)	# set xbar size

ckt.set_input_voltages(volt_r, volt_c)	# set input voltages using the list read by the file

var_bools = ckt.set_variablity(Nmin = nmin_b, Nmax = nmax_b, ldet = ldet_b, rdet = rdet_b)	# creates a dict for checking if the variabilities for each parameters are set

var_param = ckt.update_param(static_param_sim, mean_sigma, var_bools)	# update the parameters of the memristors in case the var_bools are set

netlist = ckt.design_ckt(var_param, static_param)	# create spectre netlist using the parameters set before and the static and variab parameters

ckt.set_simulation_params(sim_type, stop_time, max_step) # tune the simulator

ckt.write_into_file(out_file_name, model_path, netlist)	# write the netlist and the sim configutation into the scs file 
 


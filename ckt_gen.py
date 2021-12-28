from parameters import parameters
from gauss_var import gauss_dist
import numpy as np
import copy

class netlist_design(parameters):
	"""docstring for netlist_design"""
	def __init__(self):
		parameters.__init__(self)
		if self.device_model == "JART_VCM_1b_det":  #only deterministic model - no code for cycle to variation - just simualtion with variation
			self.static_parameters = " T0=T0 eps=esp epsphib=epsphib phiBn0=phiBn0 phin=phin un=un Nplug=Nplug \ \n a=a ny0=ny0 dWa=dWa Rth0=Rth0 Ninit=Ndiscmin rdet=rdet lcell=lcell \ \n ldet=ldet Rtheff_scaling=Rtheff_scaling RseriesTiOx=RseriesTiOx R0=R0 \ \n"
			self.variablity = "Ndiscmax={} Ndiscmin={} rdet={} ldet={}" # in case want to change parameter there are 4 variablity params
		else:   # use variablity model 
			self.static_parameters = " eps=eps epsphib=epsphib phibn0=phibn0 phin=phin \ \n un=un Ninit=Ndiscmin Nplug=Nplug a=a \ \n nyo=nyo dWa=dWa Rth0=Rth0 rdet=rdet  \ \n lcell=lcell ldet=ldet Rtheff_scaling=Rtheff_scaling RTiOx=RTiOx R0=R0 \ \n Rthline=90471.5 alphaline=0.00392 eps_eff=(eps)*(8.85419e-12) \ \n epsphib_eff=(epsphib)*(8.85419e-12)"
			self.variablity = " Ndiscmax={} Ndiscmin={} lnew = {} rnew= {} " 

	def design_voltage_sources(self):
		"""
			This function creates the voltages signal that needs to be applied on the rows and cols of the crossbar

			input : Nothing - > Takes data from global variables those are set using set_input_voltages() function

			output : retunrs name of votlage instance along with voltage values

		"""
		num_volt_source = 0
		voltages_name = ""
		vpulse = "V{} ({} {}) vsource type={} val0={} val1={} period={} width={} rise={} fall={} \n" #adding voltagesource on each row of the crossbar
		voltage_source = ""
		for i in range(self.rows):
			voltages_name += "r{} ".format(i)
			voltage_source += vpulse.format(str(num_volt_source),"r{} ".format(i),0, self.input_type_r[i], self.volt_0_r[i],self.volt_1_r[i], self.time_period_r[i], self.pulse_width_r[i], self.rise_time_r[i],self.fall_time_r[i])
			num_volt_source += 1
		for j in range(self.columns):
			voltages_name += "c{} ".format(j)
			#no voltages applied to colums
			voltage_source += vpulse.format(str(num_volt_source),"c{} ".format(j),0, self.input_type_c[j], self.volt_0_c[j],self.volt_1_c[j], self.time_period_c[j], self.pulse_width_c[j], self.rise_time_c[j],self.fall_time_c[j])
			num_volt_source += 1
		return voltages_name,voltage_source


	def update_param(self, static_param = "", mean_sigma_param = {}, bools_var = {}):
		var_param = "parameters "
		d_to_d_vardict = {}
		gauss = gauss_dist((self.rows,self.columns))

		# check for variation and create gaussin dist of each parameters according to d_to_d dict parameters
		for variation in bools_var:
			if bools_var[variation]:
				d_to_d_vardict[variation] = gauss_dist(mean_sigma_param[variation]).create_distribution((self.rows,self.columns))

		
		if(len(d_to_d_vardict) == 0):
			print("No random variations.\n")
		else:
			var_param += gauss.make_paramset(d_to_d_vardict) 
			print("{} parameters are updated due to variation.\n".format(len(d_to_d_vardict)))
	
		var_param += static_param 
		return var_param


	

	def design_ckt (self, variables = "", static_param= {}, ckt_name= "my_ckt"):
		""" 
			design the ckt based on the given parameter

			input : variables   -> all the d_to_d variable string
					with_paramt -> All the static parameters
					ckt_name    -> Name of subcircuit  ->

			output:  -> creates a complete spectre netlist and return 

		"""
		print("Generating netlist...\n")
		device_parameter_including_variablity = {}
		instance = ""
		all_current = ""
		# iterate for each device
		for rows in range(self.rows):
			for cols in range(self.columns):
				iteration = str(cols+(rows*self.columns)) # total number of iteration - required for creating number of devices

				varing_dict_ = self.variablity_param(iteration) #update dict for variation in each device 

				# the static_param dict is modified only on the parameters which have the bool var set, and the others remain the same
				for value in varing_dict_: # update the parameters for each variation
					static_param[value] = varing_dict_[value]
					

				# generate string for each instance with list of parameters from static_param
				device_parameter_including_variablity = self.set_device_parameters(param=static_param)
				
				# create instance of device
				instance += "I"+iteration +" (r{} c{}) ".format(rows,cols) + self.device_model + " " + device_parameter_including_variablity + "\n"

				# save all the current fro debugging
				all_current += "XBAR.I{}:OE ".format(iteration) 

		voltages_name, voltage_source  = self.design_voltage_sources()
		end_ckt = "ends " + ckt_name + "\n"
		subckt_instance = "XBAR (" + voltages_name + ") " + ckt_name + "\n"  # subckt instance according to spectre simulation
		output_data = variables + "\n" + "subckt " + ckt_name + " " # create subckt

		# all combined into single string
		print("Netlist generated with {} instances.\n".format(self.rows * self.columns))
		all_current += "XBAR.I2:AE"
		return output_data + voltages_name +"\n" +instance + end_ckt + subckt_instance + voltage_source + "\n save " +all_current + "\n" 


	def write_into_file(self,file_name = "auto_generated.scs", to_be_written = " "):

		"""
		write the content into spectre netlist file.

		input : Name of file in which data needs to be stored -> file_name   (by default data will be written into auto_generated.scs)
				content that needs to be written into the dile -> to_be_written
		output: create a file by the given name and store the data into that
		"""
		file_ = open(file_name,"w")
		file_.write(to_be_written)

		#ahdl include file
		path_ = "ahdl_include " + "\"" + self.model_path + "\"" + "\n"  #include the path of model in text file
		file_.write(path_)

		# type of anaylsis - only trans analysis
		ana_sis = "trans {} stop={} errpreset=conservative maxstep ={} write=\"spectre.ic\" \
		writefinal=\"spectre.fc\" annotate=status maxiters=5".format(self.simulation_type,self.simulation_stop_time, self.simulation_maxstep)
		ana_sis = ana_sis + "\nsaveOptions options save=allpub"  # type of analysis + saving the input and output current 
		file_.write(ana_sis)

		print("Netlist, model path and simulation parameters written to \"{}\"\n".format(file_name))
		
	

import copy

# this file include all the parameter those can be tuned - some of them are already set to default.

class parameters(object):  # base class for parameters
	"""docstring for parameters"""
	def __init__(self, device="var", simulation = "spectre"): #two type of device we have var (variablity) and det (deterministic)
		# gauss_dist.__init__(self)

		if simulation !="spectre":
			print("simulation needs to be set = spectre")
			exit()
		if device =="var":
			self.device_model= "JART_VCM_1b_VAR"
			self.model_path = "/net/home/zahr/Downloads/counterfeit/JART_VCM_1b_verilog-var.va" # change this path according to local path
		else:
			self.device_model= "JART_VCM_1b_det"
			# TO-DO
			print ("please slelect the device = var")
		#self.set_default_params()

	def set_device_parameters(self, param= {}, model_name="var"):
		"""
			Setting all the device parameters, this include all the static parameters and varibales.

			Input: Model name - Model could be deterministic or variablity model (det or var)
					param - type dict -> requires parameters that need to set
			Output: Set the path of devide model in local directory and link it.
					return string after combining all the parameters into one.

		"""

		self.device_parameters = ""
		if model_name=="var":
			for i in param:
				self.device_parameters+= i + " = " + str(param[i]) + " "   #concatinate the string according to each parameter

		else:
			self.device_model= "JART_VCM_1b_det"
			self.model_path = "/home/users/simranjeet/JART_variablity_test/JART_VCM_1b_veriloga-det.va"
		return self.device_parameters

	def variablity_param(self, iteration):
		"""
			Create name of each variable and append into device instance
			input: number of iteration that need to added -> added based on the global variablity parameter
					iterate for each variablity if true then append
			output: dict contaning all the variables names.

		"""

		variablity_dict = {}
		variablity_dict["Ninit"] = "Ndiscmin"
		# check for each parameter and if set perform the varition and push into dict 
		if self.vary_nmin:
			ndisc_min_var = "Ndiscmin{} ".format(iteration)
			variablity_dict["Ndiscmin"] = variablity_dict["Ninit"] = ndisc_min_var
		if self.vary_nmax:
			ndisc_max_var = "Ndiscmax{} ".format(iteration)
			variablity_dict["Ndiscmax"] = ndisc_max_var
		if self.vary_ldet:
			lnew_var = "lnew{} ".format(iteration)
			variablity_dict["lnew"] = lnew_var
		if self.vary_rdet:
			rnew_var = "rnew{}".format(iteration)
			variablity_dict["rnew"] = rnew_var

		#ex with iteration=0-> variability_dict = {"Ndiscmin" : "Ndiscmin0", "Ndiscmax" : "Ndiscmax0", "lnew" : "lnew0", "rnew0" : "rnew0"}
		#if no variations -> variability_dict = {"Ninit" : , "Ndiscmin" }
		return variablity_dict

	def set_default_params(self):
		"""
		Set all the parameters to default

		"""
		self.set_device_parameters()
		self.set_input_voltages()
		self.set_simulation_params()
		#self.set_cross_bar_params()

	def set_input_voltages(self, type_="pulse", vol0=0, vol1=2, time_period="2u", pulse_width="1u", rise_time = "25n", fall_time="25n"):
		"""
		set the input voltages to the cross bar

		input: type - (Vpulse, Vsource)  -Pulse input or sin input
			   vol0, vol1 - voltage levels
			   time_period
			   Pulse_width
			   rise_time
			   fall_time
		output: Initialize all the variables for voltage sequence 

		"""
		self.input_type = type_
		self.volt_0 = vol0
		self.volt_1 = vol1
		self.time_period = time_period
		self.pulse_width = pulse_width
		self.rise_time = rise_time
		self.fall_time = fall_time

		#print("Voltage pulses generated.\n")

	def set_simulation_params(self, type_, stop_time, maxstep):

		"""
			intilize all the parameters required for spectre simulation
			input: type_ -> type of analysis (DC, tran)
					stop_time -> simulation run time
					maxstep -> maximum step size.

					--- min step can also be set but that will create problem in evalution 
					the solution may not converge at minimum defined time. ---

		"""
		self.simulation_stop_time = stop_time
		self.simulation_type = type_
		self.simulation_maxstep = maxstep

		print("Stop time: {}, Max step: {} are set for the simulation.\n".format(self.simulation_stop_time,self.simulation_maxstep))

	def set_cross_bar_params(self, rows, columns):

		"""
		initilize the cross bar based on the number of input
		"""

		self.rows = rows
		self.columns = columns

		print("{}x{} crossbar generated.\n".format(self.rows,self.columns))
		return (self.rows,self.columns)

	def set_variablity(self, Nmin=False, Nmax=False, rdet=False, ldet=False):
		"""
		check the variablity parameters and set paraticular varilble and append it to dict
		

		"""

		self.vary_nmin = Nmin
		self.vary_nmax = Nmax
		self.vary_rdet = rdet
		self.vary_ldet = ldet

		return {"Ndiscmin": Nmin, "Ndiscmax": Nmax, "rnew": rdet,"lnew": ldet}

	def copy_param(self):
		"""
		returns a deep copy of itself
		:return params:
		:rtype: Parameters

		"""
		params = copy.deepcopy(self)
		return params
	def print_parameters(self):

		"""
		for debussing, print the device parameters
		"""

		print ("---- device parameter values ----- \n", self.device_parameters)



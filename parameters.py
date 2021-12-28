import copy

# this file include all the parameter those can be tuned - some of them are already set to default.

class parameters(object):  # base class for parameters
	"""docstring for parameters"""
	def __init__(self, device="var", simulation = "spectre"): #two type of device we have var (variablity) and det (deterministic)

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

		return variablity_dict

	def set_default_params(self):
		"""
		Set all the parameters to default

		"""
		self.set_device_parameters()
		self.set_cross_bar_params()
		self.set_input_voltages()
		self.set_simulation_params()

	def set_input_voltages(self, volt_r = [], volt_c = []):
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
		self.input_type_r, self.input_type_c = [], []
		self.volt_0_r, self.volt_0_c = [], []
		self.volt_1_r, self.volt_1_c = [], []
		self.time_period_r, self.time_period_c = [], []
		self.pulse_width_r, self.pulse_width_c = [], []
		self.rise_time_r, self.rise_time_c = [], []
		self.fall_time_r, self.fall_time_c = [], []

		def_vol = ["pulse", 0, 0, "0", "0", "0", "0"]

		if self.rows < len(volt_r):
			print("There are {} voltage pulses but only {} rows -> {} voltage pulses are ignored\n".format(len(volt_r), self.rows, len(volt_r)-self.rows))
			while self.rows != len(volt_r):
				volt_r.pop()
		
		if self.columns < len(volt_c):
			print("There are {} voltage pulses but only {} columns -> {} voltage pulses are ignored\n".format(len(volt_c), self.columns, len(volt_c)-self.columns))
			while self.columns != len(volt_c):
				volt_c.pop()
		
		if self.rows > len(volt_r):
			print("There are {} rows, but only {} voltage pulses are defined -> {} null voltages are added\n".format(self.rows, len(volt_r), self.rows - len(volt_r)))
			while self.rows != len(volt_r):
				volt_r.append(def_vol)
		
		if self.columns > len(volt_c):
			print("There are {} columns, but only {} voltage pulses are defined -> {} null voltages are added\n".format(self.columns, len(volt_c), self.columns - len(volt_c)))
			while self.columns != len(volt_c):
				volt_c.append(def_vol)

		for v in volt_r:
			self.input_type_r.append(v[0])
			self.volt_0_r.append(v[1])
			self.volt_1_r.append(v[2])
			self.time_period_r.append(v[3])
			self.pulse_width_r.append(v[4])
			self.rise_time_r.append(v[5])
			self.fall_time_r.append(v[6])

		for v in volt_c:
			self.input_type_c.append(v[0])
			self.volt_0_c.append(v[1])
			self.volt_1_c.append(v[2])
			self.time_period_c.append(v[3])
			self.pulse_width_c.append(v[4])
			self.rise_time_c.append(v[5])
			self.fall_time_c.append(v[6])
		
		print("Voltage pulses correctly added.\n")

	def set_simulation_params(self, type_ = "tran", stop_time = "5u", maxstep = "1u"):

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


		print("Stop time: {}s, Max step: {}s.\n".format(self.simulation_stop_time,self.simulation_maxstep))

	def set_cross_bar_params(self, rows = 5, columns = 5):

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



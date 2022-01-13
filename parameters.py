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

		#self.set_default_params()

	def set_device_parameters(self, param= {}, model_name="var"):
		"""
			Generates a string containing all the parameters for each memristor. It is used during the generation of the netlist
			(design_ckt function) in appending the string for each instance

		"""

		self.device_parameters = ""
		if model_name=="var":
			for i in param:
				self.device_parameters+= i + " = " + str(param[i]) + " "   #concatinate the string according to each parameter
		
		return self.device_parameters

	def variablity_param(self, iteration):
		"""
			Returns a dictionary in case the variability bools are set for each memristor of the xbar (iteration passed as argument).
			It is used during the generation of the netlist (design_ckt function) for updating the parameters accordingly.

		"""

		variablity_dict = {}
		variablity_dict["Ninit"] = "Ndiscmin"

		if self.vary_nmin:
			ndisc_min_var = f"Ndiscmin{iteration} "
			variablity_dict["Ndiscmin"] = variablity_dict["Ninit"] = ndisc_min_var
		if self.vary_nmax:
			ndisc_max_var = f"Ndiscmax{iteration} "
			variablity_dict["Ndiscmax"] = ndisc_max_var
		if self.vary_ldet:
			lnew_var = f"lnew{iteration} "
			variablity_dict["lnew"] = lnew_var
		if self.vary_rdet:
			rnew_var = f"rnew{iteration}"
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

		It takes as input the voltage pulses description for each row and columns (which are takes as input via a csv file) and appends
		them to the circuit parameters, in order to be used later with the design_voltage_sources function to generate a string for the netlist.
		It checks for an eventual difference between the xbar size and the input pulses, and manages such cases.

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
			print(f"There are {len(volt_r)} voltage pulses but only {self.rows} rows -> {len(volt_r)-self.rows} voltage pulses are ignored.\n")
			while self.rows != len(volt_r):
				volt_r.pop()
		
		if self.columns < len(volt_c):
			print(f"There are {len(volt_c)} voltage pulses but only {self.columns} columns -> {len(volt_c)-self.columns} voltage pulses are ignored.\n")
			while self.columns != len(volt_c):
				volt_c.pop()
		
		if self.rows > len(volt_r):
			print(f"There are {self.rows} rows, but only {len(volt_r)} voltage pulses are defined -> {self.rows - len(volt_r)} null voltages are added.\n")
			while self.rows != len(volt_r):
				volt_r.append(def_vol)
		
		if self.columns > len(volt_c):
			print(f"There are {self.columns} columns, but only {len(volt_c)} voltage pulses are defined -> {self.columns - len(volt_c)} null voltages are added.\n")
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
			Intilize all the parameters required for spectre simulation
			input: type_ -> type of analysis (DC, tran)
					stop_time -> simulation run time
					maxstep -> maximum step size.

					--- min step can also be set but that will create problem in evalution 
					the solution may not converge at minimum defined time. ---

		"""
		self.simulation_stop_time = stop_time
		self.simulation_type = type_
		self.simulation_maxstep = maxstep


		print(f"Stop time: {self.simulation_stop_time}s, Max step: {self.simulation_maxstep}s.\n")

	def set_cross_bar_params(self, rows = 5, columns = 5):
		"""
			initilize the cross bar based on the number of input
		"""

		self.rows = rows
		self.columns = columns

		print(f"{self.rows}x{self.columns} crossbar generated.\n")
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
		Returns a deep copy of itself
		"""
		params = copy.deepcopy(self)
		return params
	def print_parameters(self):

		"""
		For debugging, print the device parameters
		"""

		print ("---- device parameter values ----- \n", self.device_parameters)



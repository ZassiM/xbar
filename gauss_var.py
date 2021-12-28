# import parameters
import numpy as np
import matplotlib.pyplot as plt
import random
from parameters import parameters


#this class manages the variation parameters of the single memristors
class gauss_dist(parameters):
	"""docstring for gauss_dist"""
	def __init__(self, var = (None,None)):   # class will be initilized for each variable withe different mu and sigma
		parameters.__init__(self) # child class 

		if var[0]==None or var[1]==None:
			self.mu = float
			self.sigma =float
		else:
			self.mu = var[0]
			self.sigma = var[1]

	def set_mu_sigma(self, mu=None, sigma=None):
		if mu==None or sigma==None:
			print ("value of mu and sigma is not defined")
			self.mu = float
			self.sigma =float
		else:
			self.mu = mu
			self.sigma = sigma

	def create_distribution(self, cross_bar=()):
		''' this fucntion helpd to create the ramdom gauss distributin
			requirement, 
			1. mu
			2. sigma

			input : size of crossbar in tuple  -(rows and columns)
		'''
		variation = np.random.normal(self.mu, self.sigma, cross_bar[0]*cross_bar[1])
		return variation

	def make_paramset(self, in_dict = {}):
		"""
		set all the variable parameters including static

		input: in_dict -> dictionary containing all the variablity variables 

		"""
		variable_name = ""
		if (len(in_dict)==0):  # checkpoint
			pass
		else:
			for var_param in in_dict:
				for i in range(len(in_dict[var_param])): 
					variable_name += var_param + "{}".format(i) + " = " + str(in_dict[var_param][i]) + " " #append each variable in list
		return variable_name


	def plot_variation(self, variation, bin_=300, line=False):
		"""	
			plot the created distribution using matplotlib

			input: variation -> These will be ploted on histogram
					bin_ -> bins for histt
					line -> bool for gauss line 
			out : Plot the variation and show the hist

		"""

		_, bins, _ = plt.hist(variation, bin_, density=True)
		if line:
			plt.plot(bins, 1/(self.sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - self.mu)**2 / (2 * self.sigma**2) ), linewidth=2, color='r')
		title = "result for mu={}, sigma={}".format(self.mu, self.sigma)
		plt.title(title)
		plt.show()

	def __repr__(self):
		return 'mu = {}, sigma ={}'.format(self.mu, self.sigma)
	def __str__(self):
		return 'mu = {}, sigma ={}'.format(self.mu, self.sigma)


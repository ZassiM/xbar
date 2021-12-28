import csv

read = 0
volt_r = []
volt_c = []
row = 0
columns = 0

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
            row, column = (int(c[0]), int(c[1]))
            print(row,column)

        if read == 2:
            nmin_b, nmax_b, ldet_b, rdet_b = (int(c[0]), int(c[1]), int(c[2]), int(c[3]))

        if read == 3:
            sim_type, stop_time, max_step = (c[0]), c[1], (c[2])
        
        if read == 4:
            volt_r.append(c)        

        if read == 5:
            volt_c.append(c)

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
        voltage_source += vpulse.format(str(num_volt_source),"r{} ".format(i),0, self.input_type, self.volt_0,self.volt_1, self.time_period, self.pulse_width, self.rise_time,self.fall_time)
        num_volt_source += 1
    for j in range(self.columns):
        voltages_name += "c{} ".format(j)
        #no voltages applied to colums
        voltage_source += vpulse.format(str(num_volt_source),"c{} ".format(j),0, self.input_type, 0 ,0, self.time_period, self.pulse_width, self.rise_time,self.fall_time)
        num_volt_source += 1
    return voltages_name,voltage_source


        
    
            
        

        

        



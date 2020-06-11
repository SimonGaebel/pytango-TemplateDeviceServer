#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Copyright (C) 2020  MBI-Division-B / Author: Luca Barbera / Email: barbera@mbi-berlin.de
# MIT License, refer to LICENSE file
    
    
'''
This is a template for a Tango Device Server, to be cloned and used as a start for your own TangoDS.
'''

from tango import AttrWriteType, DevState, DebugIt
from tango.server import Device, attribute, command, device_property

#import the driver you will use

class TemplateDeviceServer(Device):

	#------ Attributes ------#

	humidity = attribute(name='Humidity',dtype=float, access = AttrWriteType.READ, doc='Example for an attribute that can only be read.')
	
	#optionally use fget/fset to point to read and write functions. Default is "read_temperature"/"write_temperature"
    temperature = attribute(name='Temperature',fget='get_temp',dtype=float, access = AttrWriteType.READ_WRITE, doc='Example for an attribute that can be read/written.')




    #------ Device Properties ------#
    #device_properties will be set once per family-member and usually contain
    #serial numbers or a certain port-ID that needs to be set once and not changed
    #while the server is running

    port = device_property(dtype=int, default_value=10000)



    #------ default functions that are inherited from parent "Device" ------#

    def init_device(self):
        Device.init_device(self)
        self.info_stream('Connection established') #prints this line in logging mode "info" or lower
        self.set_state(DevState.ON) #    
        
        #here you could initiate first contact to the hardware (driver)
        
        self.__temp = 0 #declaring values for the attributes and properties
    	self.__humid = 0
		self.__port = port
	
	def delete_device(self):
		self.set_state(DevState.OFF)
		self.error_stream('A device was deleted!') #prints this line in logging mode "error" or lower
	

	# define what is executed when Tango checks for the state. Here you could inquire the state of the hardware and not just (as it is in default) of the TDS.
	def get_state(self):
		#possible pseudo code:
		# if hardware-state and TDS-state is ON:
		#	return DevState.ON
	

	def always_executed_hook(self):
	#this is a method that is executed continuously but by default does nothing
	#if you want something polled or done continuously, put it in this method
		#check connection to hardware or whether status is acceptable etc.
		pass
	
	
	#------ Read/Write functions ------#

	def read_humidity(self): #this is default to read humidity
		return self.__humid #returns the current value of the attribute "humidity"
    
    def get_temp(self): #this was set by fget in attribute declaration
        return self.__temp
    
    def write_temp(self,value):
        #possibly execute some function here to talk to the hardware (e.g. set temperature with a thermostat)
        self.__temp = value # update the declared server value of the attribute
    


	#------ Internal Methods ------#
    #method that works with multiple input parameters only "inside" this code

    def internal_method(self,param1, param2):
        #do something with param1, param2
        pass
    



    #------ COMMANDS ------#

    @DebugIt() #let the execution of this command be logged in debugging mode
    @command() #make method executable through the client (as opposed to just callable inside this code)
    def External_Method(self,param):
        #this kind of method only allows one input parameter
        pass
    
    #another example of an externally executable method
    @command()
    def Turn_Off(self):
        self.set_state(DevState.OFF)
        
    @command()
    def Turn_On(self):
        self.set_state(DevState.ON)
    
#start the server
if __name__== "__main__":
    TemplateDeviceServer.run_server()        
        
    
    
        

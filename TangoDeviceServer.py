#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This is a template Tango Device Server, to be cloned and used as a start for your own TangoDS.


    Copyright (C) 2020  MBI-Division-B, Author: Luca Barbera, Email: barbera@mbi-berlin.de

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
    
    
'''

from tango import AttrWriteType, DevState, DebugIt
from tango.server import Device, attribute, command, device_property

#import the driver you will use

class MyTangoDS(Device):
    #declare your desired attributes
    temperature = attribute(name='Temperature',fget='get_temp',fset='set_temp',dtype=float, access = AttrWriteType.READ_WRITE,
                      doc='this is an example attribute that can be read and written')
    
    #device_properties will be set once per family-member and usually contain
    #serial numbers or a certain port-ID that needs to be set once and not changed
    #while the server is running
    port = device_property(dtype=int, default_value=10000)

    
    def init_device(self):
        Device.init_device(self)
        self.info_stream('Connection established') #prints this line in logging mode "info" or lower
        self.set_state(DevState.ON) #    
        
        #here you could initiate first contact to the hardware (driver)
        
        self.__temp = 0 #declaring a value for the temperature
        
    def get_temp(self):
        return self.__temp #returns the current value of the attribute "temperature"
    
    def set_temp(self,value):
        #possibly execute some function here to talk to the hardware (e.g. set temperature with a thermostat)
        self.__temp = value # update the declared server value of the attribute
    
    #method that works with multiple input parameters only "inside" this code
    def internal_method(self,param1, param2):
        #do something with param1, param2
        pass
    
    
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
    MyTangoDS.run_server()        
        
    
    
        

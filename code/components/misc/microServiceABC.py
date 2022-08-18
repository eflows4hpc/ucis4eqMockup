#!/usr/bin/env python3
#
# RESTful server for event treatment
# This module is part of the Automatic Alert System (AAS) solution
#
# Author:  Juan Esteban Rodríguez, Josep de la Puente
# Contact: juan.rodriguez@bsc.es, josep.delapuente@bsc.es
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

################################################################################
# Module imports
import sys
from abc import ABC, abstractmethod
from bson.objectid import ObjectId
from flask import jsonify
import datetime
import ucis4eq.misc.config as config

################################################################################
# Methods and classes
class MicroServiceABC(ABC):
    
    # Method for defining the entry point to the service implementation
    @abstractmethod    
    def entryPoint(self, body):
        raise NotImplementedError("Error: 'entryPoint' method should be implemented")
        
    # Static method for decorating microservices
    @classmethod
    def runRegistration(cls, func):
        def func_wrapper(*args, **kwargs):
               # Initialize
               runInfo = {}
               status = "RUNNING"               
               serviceRun = None
               className = args[0].__class__.__bases__[0].__name__               
               if className == cls.__name__:
                  className = args[0].__class__.__name__
               
               # Check if the request provides a Dict 
               if isinstance(args[1], dict) and 'id' in args[1].keys():
                    runInfo['serviceName'] = className
                    runInfo['requestId'] = args[1]['id'] 
                    runInfo['status'] = status
                    runInfo['initTime'] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
                    runInfo['inputs'] = args[1]
                    if "resources" in args[1].keys():
                        runInfo['machine'] = args[1]['resources']
                    else:
                        runInfo['machine'] = "N/A"
                    
               else:
                    raise Exception("The 'entrypoint' method for the service '" +\
                    className + "' must define a dictionary with a 'id' key")

               # Protect a service execution
               try:
                   results = func(*args, **kwargs)
                   status = "SUCCESS"
               except Exception as e:
                   
                   config.printException()
                   
                   status = "FAILED"
                        
                   # Return error code and message
                   results = jsonify(result = str(e), response = 501)                                               
                                                 
               return results
        return func_wrapper

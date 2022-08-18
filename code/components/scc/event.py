#!/usr/bin/env python3
#
# Events dispatcher
# This module is part of the Smart Center Control (SSC) solution
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
# along with this program. If not, see <https://www.gnu.org/licenses/>.

################################################################################
# Module imports
# System
import sys
import os
import traceback
import json
import requests
import math

from shapely.geometry import mapping, shape
from shapely.prepared import prep
from shapely.geometry import Point

from bson.json_util import dumps
from bson import ObjectId
from urllib.request import urlopen

# Third parties
from flask import jsonify

# Internal
from ucis4eq.misc import config, microServiceABC
import ucis4eq as ucis4eq

################################################################################
# Methods and classes
class EventRegistration(microServiceABC.MicroServiceABC):

    # Initialization method
    def __init__(self):
        """
        Initialize the eventDispatcher component implementation    
        """

    # Service's entry point definition
    @config.safeRun
    def entryPoint(self, body):
        """
        Deal with a new earthquake event
        """
        
        ""
        
        event = str(body['uuid'])
        
        print("Request Id. [" + str(event) + "] registered for event [" + \
             body['uuid'] + "]", flush=True)

        # Return list of Id of the newly created item
        return jsonify(result = str(event), response = 201)
        
        
################################################################################
# Methods and classes
class EventSetState(microServiceABC.MicroServiceABC):

    # Initialization method
    def __init__(self):
        """
        Initialize the eventDispatcher component implementation    
        """
        

    # Service's entry point definition
    @config.safeRun
    def entryPoint(self, body):
        """
        Update the status of an earthquake event
        """
        
        print("Request Id. [" + str(body['id']) + "] state [" + str(body['state']) + "]")
             
        # Return list of Id of the newly created item
        return jsonify(result = str(body['id']), response = 201)
        
class EventGetRegion(microServiceABC.MicroServiceABC):

    # Initialization method
    def __init__(self):
        """
        Initialize the eventDispatcher component implementation    
        """

    # Service's entry point definition
    @config.safeRun
    def entryPoint(self, body):
        """
        Obtain region information
        """
        region = "EQ's Region"
        
        # Return list of Id of the newly created item
        return jsonify(result = region, response = 201)

class EventDomains(microServiceABC.MicroServiceABC):

    # Initialization method
    def __init__(self):
        """
        Initialize the eventDispatcher component implementation    
        """
        
        # Initialize output results
        self.domains = {}

    # Service's entry point definition
    @microServiceABC.MicroServiceABC.runRegistration
    def entryPoint(self, body):
        """
        Figure out the set of domains which the incoming EQ event belong
        """                    
        # Retrieve the event's complete information 
        rid = body['id']

        domain = { 'region': str(rid) + '_region1', 'id': "region1"}
                
        self.domains = [domain]
                    
        # Return list of Id of the newly created item
        return jsonify(result = self.domains, response = 201)

class EventCountry(microServiceABC.MicroServiceABC):

    # Initialization method
    def __init__(self):
        """
        Initialize the eventDispatcher component implementation    
        """
         
    # Service's entry point definition
    @microServiceABC.MicroServiceABC.runRegistration
    def entryPoint(self, body):
        """
        Figure out the country which the incoming EQ event belong 
        """

        # Return list of Id of the newly created item
        return jsonify(result = "COUNTRY", response = 201)
      
      
      
      
      

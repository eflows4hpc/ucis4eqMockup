#!/usr/bin/env python3
#
# Simulator (Wave propagation simulator)
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
import uuid
import yaml
from bson.json_util import dumps

# Third parties
from flask import jsonify

# Internal
from ucis4eq.misc import config, microServiceABC
import ucis4eq as ucis4eq

################################################################################
# Methods and classes

class SimulatorPrepare(microServiceABC.MicroServiceABC):

    # Initialization method
    def __init__(self):
        """
        Initialize SimulatorRun instance
        """

    # Service's entry point definition
    @microServiceABC.MicroServiceABC.runRegistration                
    def entryPoint(self, body):
        """
        Call the Simulator-Flow Marta's wrapper
        """

        # Get the path to the Simulator input parameters
        result = "/get/the/path/to/the/generated/simulator_input_file.params"
        
        # Return list of Id of the newly created item
        return jsonify(result = result, response = 201)

class SimulatorRun(microServiceABC.MicroServiceABC):

    # Initialization method
    def __init__(self):
        """
        Initialize SimulatorRun instance
        """

    # Service's entry point definition
    @microServiceABC.MicroServiceABC.runRegistration    
    def entryPoint(self, body):
        """
        Call the Simulator-Compute on the remote machine
        """
            
        result = "/get/the/path/to/the/generated/simulation/outputs/"        

        # Return list of Id of the newly created item
        return jsonify(result = result, response = 201)
    
class SimulatorPost(microServiceABC.MicroServiceABC):

    # Initialization method
    def __init__(self):
        """
        Initialize the CMT statistical component implementation
        """

    # Service's entry point definition
    @config.safeRun
    @microServiceABC.MicroServiceABC.runRegistration    
    def entryPoint(self, body):
        """
        Call the Simulator-Flow Marta's wrapper (Postprocessing scripts)
        """
        
        result = "Simulation's postprocessing stage"        
        
        # Return list of Id of the newly created item
        return jsonify(result = result, response = 201)

class SimulatorPostSwarm(microServiceABC.MicroServiceABC):

    # Initialization method
    def __init__(self):
        """
        Initialize the CMT statistical component implementation
        """

    # Service's entry point definition
    @config.safeRun
    @microServiceABC.MicroServiceABC.runRegistration    
    def entryPoint(self, body):
        """
        Call the Simulator-Flow Marta's wrapper (Postprocessing scripts)
        """

        result = "Simulation's postprocessing stage"    
        
        # Return list of Id of the newly created item
        return jsonify(result = result, response = 201)

class SimulatorPlots(microServiceABC.MicroServiceABC):

    # Initialization method
    def __init__(self):
        """
        Initialize the CMT statistical component implementation
        """

    # Service's entry point definition
    @config.safeRun
    @microServiceABC.MicroServiceABC.runRegistration    
    def entryPoint(self, body):
        """
        Call the Simulator-Flow Marta's wrapper (Postprocessing scripts)
        """
        
        result = "Simulation's plots result"
        
        # Return list of Id of the newly created item
        # TODO: Return the SRF in plain text 
        return jsonify(result = result, response = 201)        
                
class SimulatorPing(microServiceABC.MicroServiceABC):

    # Initialization method
    def __init__(self):
        """
        Initialize SimulatorRun instance
        """

    # Service's entry point definition
    @config.safeRun
    def entryPoint(self, body):
        """
        Call the Simulator-Compute on the remote machine
        """
        
        # Return list of Id of the newly created item
        return jsonify(result = {}, response = 201)

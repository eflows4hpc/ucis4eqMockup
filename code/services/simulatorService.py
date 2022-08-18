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

# System imports
import sys
import json
import ast
import traceback
from functools import wraps

# Flask (WSGI) utils
from flask import Flask, request, jsonify

# Load Simulator service implemented components
from ucis4eq.scc.simulator import SimulatorPrepare, SimulatorRun, SimulatorPost, SimulatorPlots, SimulatorPing, SimulatorPostSwarm

################################################################################
# Dispatcher App creation
################################################################################
simulatorServiceApp = Flask(__name__)

# POST request decorator
def postRequest(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        
        """
        Function to dispatch new events.
        """
        # Create new events
        try:
            body = ast.literal_eval(json.dumps(request.get_json()))
        except:
            # Bad request as request body is not available
            # Add message for debugging purpose
            return "", 400

        # Call the decorated method passing it the input JSON
        return fn(body)
        
    return wrapped

# Base root of the micro-services Hub
@simulatorServiceApp.route("/")
def get_initial_response():
    """Welcome message for the API."""
    # Message to the user
    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'Welcome to the UCIS4EQ Simulator service'
    }
    # Making the message looks good
    resp = jsonify(message)
    # Returning the object
    return resp
    
################################################################################
# Services definition
################################################################################

# Generate input parameters for Simulator
@simulatorServiceApp.route("/SimulatorPrepare", methods=['POST'])
@postRequest
def SimulatorPrepareService(body):
    """
    Call component implementing this service
    """
    
    return SimulatorPrepare().entryPoint(body)    

# Call Simulator for a trial
@simulatorServiceApp.route("/SimulatorRun", methods=['POST'])
@postRequest
def SimulatorRunService(body):
    """
    Call component implementing this service
    """
    
    return SimulatorRun().entryPoint(body)
    
# Call Simulator post-processing
@simulatorServiceApp.route("/SimulatorPost", methods=['POST'])
@postRequest
def SimulatorPostService(body):
    """
    Call component implementing this service
    """
    return SimulatorPost().entryPoint(body)    
    
# Call Simulator post-processing
@simulatorServiceApp.route("/SimulatorPostSwarm", methods=['POST'])
@postRequest
def SimulatorPostSwarmService(body):
    """
    Call component implementing this service
    """
    return SimulatorPostSwarm().entryPoint(body)      

# Call Simulator post-processing
@simulatorServiceApp.route("/SimulatorPlots", methods=['POST'])
@postRequest
def SimulatorPlotsService(body):
    """
    Call component implementing this service
    """
    return SimulatorPlots().entryPoint(body)
    
# Call Simulator post-processing
@simulatorServiceApp.route("/SimulatorPing", methods=['POST'])
@postRequest
def SimulatorPingService(body):
    """
    Call component implementing this service
    """
    return SimulatorPing().entryPoint(body)
    

################################################################################
# Start the micro-services aplication
################################################################################

if __name__ == '__main__':
    # Running app in debug mode
    simulatorServiceApp.run(host="0.0.0.0", debug=True, port=5003)

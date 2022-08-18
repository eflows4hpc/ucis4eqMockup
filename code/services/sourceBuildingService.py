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

# Load slip-gen service implemented components
from ucis4eq.scc.sourceBuilding import SourceBuilding

################################################################################
# Dispatcher App creation
################################################################################
sourceBuildingServiceApp = Flask(__name__)

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
@sourceBuildingServiceApp.route("/")
def get_initial_response():
    """Welcome message for the API."""
    # Message to the user
    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'Welcome to the UCIS4EQ Source building service for PD1'
    }
    # Making the message looks good
    resp = jsonify(message)
    # Returning the object
    return resp
    
################################################################################
# Services definition
################################################################################
    
# Determine the kind of source for the simulation
@sourceBuildingServiceApp.route("/SourceBuilding", methods=['POST'])
@postRequest
def sourceBuildingService(body):
    """
    Call component implementing this service
    """
    return SourceBuilding().entryPoint(body)

################################################################################
# Start the micro-services aplication
################################################################################

if __name__ == '__main__':
    # Running app in debug mode
    sourceBuildingServiceApp.run(host="0.0.0.0", debug=True, port=5002)

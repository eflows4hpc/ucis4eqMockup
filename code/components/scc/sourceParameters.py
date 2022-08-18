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
import traceback
import json
from bson import ObjectId

# Third parties
from flask import jsonify

# Internal
import ucis4eq
from ucis4eq.misc import config, microServiceABC

################################################################################
# Methods and classes

class SourceParametersInputs(microServiceABC.MicroServiceABC):

    # Attibutes
    setup = {}             # Setup for the CMT calculation
    event = None           # Input event

    # Initialization method
    def __init__(self):
        """
        Initialize the SourceParameters component implementation
        """

    # Service's entry point definition
    @microServiceABC.MicroServiceABC.runRegistration
    def entryPoint(self, body):
        """
        Generate a source parameters inputs
        """

        # Retrieve the event's complete information
        event = {}
        event['alerts'] = {}

        # Add the current event
        inputParameters = {
                            "event": {
                                "_id": body['id'],
                                "alerts": event['alerts'],
                                }
                           }

        return jsonify(result = inputParameters, response = 201)

class SourceParametersCalculation(microServiceABC.MicroServiceABC):

    # Attibutes
    setup = {}             # Setup for the CMT calculation
    event = None           # Input event

    # Initialization method
    def __init__(self):
        """
        Initialize the SourceParameters component implementation
        """

    # Service's entry point definition
    @microServiceABC.MicroServiceABC.runRegistration
    def entryPoint(self, body):
        """
        Source Parameters Calculation
        """

        sources = {}
        for sid in range(1, 6):
            sources['source'+str(sid)] = {}

        return jsonify(result = sources, response = 201)

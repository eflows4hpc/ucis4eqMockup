#!/usr/bin/env python3
#
# Slip generation
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
import random
from bson.json_util import dumps

# Third parties
from flask import jsonify

# Internal
import ucis4eq
from ucis4eq.misc import config, microServiceABC

################################################################################
# Methods and classes

class SourceBuilding(microServiceABC.MicroServiceABC):

    # Service's entry point definition
    @microServiceABC.MicroServiceABC.runRegistration                
    def entryPoint(self, body):
        """
        Call the source building
        """

        # Get the path to the generated rupture
        result = "/get/the/path/to/the/generated/source"
        return jsonify(result = result, response = 201)

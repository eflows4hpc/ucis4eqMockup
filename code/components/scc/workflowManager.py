#!/usr/bin/env python3
#
# Workflow Manager
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
import requests
import json
import uuid
import concurrent.futures
import time
import os

# Third parties
from flask import jsonify

from pycompss.api.parameter import *
from pycompss.api.http import http
from pycompss.api.api import compss_wait_on, compss_barrier
from pycompss.api.task import task
#from pycompss.api.on_failure import on_failure

# Internal
import ucis4eq
from ucis4eq.misc import config, microServiceABC

################################################################################
# Methods and classes

class PyCommsWorkflowManager(microServiceABC.MicroServiceABC):

    # Initialization method
    def __init__(self):
        """
        Initialize -the workflow manager
        """

    # Service's entry point definition
    @config.safeRun
    def entryPoint(self, body):
        """
        PyCOMPSs workflow manager
        """

        print("__ Running PyCOMPSs workflow __")
        event = body
        
        # Set event's name
        basename = "event_" + event['uuid']
        
        # Obtain the Event Id. (useful during all the workflow livecycle)    
        eid = register_event(event)
        
        # Obtain the region where the event occured        
        domains = get_domains(eid)
        
        # Wait for future to check if continue or abort
        domains = compss_wait_on(domains)
                
        if not domains: 
            eid = set_event_state(eid, "REJECTED")

            raise Exception("There is not enough information for simulating the EQ in region")  
        
        else:
            # For each found domain
            for domain in domains:
                
                # Calculate the CMT input parameters
                presource = pre_source(eid, domain['region'])
            
                # Obtain region information
                region = get_event_region(domain['region'])
                
                # Calculate computational resources for the given domain
                resources = compute_resources(eid, domain)
                
                # Wait for region setup
                region = compss_wait_on(region)
                
                # Compute alerts
                all_results = []
                for alert in event['alerts']:
                    
                    # Calculating CMTs
                    sources = source_calculation(alert, eid, domain, presource)

                    # Wait for calculated CMTs
                    sources = compss_wait_on(sources)            
                    
                    # For each calculated or provided CMT
                    for source in sources.keys():
                        
                        # For each GP defined trial
                        for slip in range(1, 4):
                            
                            # Set the trial path
                            path = basename + "/trial_" + ".".join([domain['id'], source, 
                                             "slip"+str(slip)])
                                                                     
                            # Call source building service
                            builtSource = compute_source_building(eid, alert, path,
                                           sources[source], domain, resources)
                                                
                            # Call input parameters builder
                            inputs = build_input_parameters( eid, alert, sources[source], 
                                    builtSource, domain, resources)                                                     

                            # Build the Simulator input parameter file (remotely)
                            simulator_inputs = build_simulator_parameters( eid, path, 
                                    inputs, resources)
                                                                

                            # Build the Simulator input parameter file (remotely)
                            result = run_simulator( eid, path, simulator_inputs,
                                    resources)
                                                    
                            # Call Simulator post 
                            all_results.append(run_simulator_post(eid, result, path, 
                                            resources))

                #TODO: Be sure this continue being necessary
                compss_wait_on(all_results)
                
                # Call postprocessing swarm
                output_swarm = run_simulator_post_swarm(eid, basename, domain, resources)

                # General post-processing for generating plots
                result = run_simulator_plots(eid, output_swarm, basename, domain, resources)

                # Set the event with SUCCESS state    
                compss_wait_on(result)   
                eid = set_event_state(eid, "SUCCESS")

        # Wait for the workflow to finish
        compss_barrier(no_more_tasks=True)
                
        # Return list of Id of the newly created item
        return jsonify(result = "Event with UUID " + str(body['uuid']), response = 201)

#@on_failure(management='IGNORE', returns=0)
@http(request="POST", resource="eventRegistration", service_name="microservices",
      payload="{{event}}", produces='{"result" : "{{return_0}}" }')
@task(returns=1)
def register_event(event):
    """
    """
    pass
    
#@on_failure(management='IGNORE', returns=0)    
@http(request="POST", resource="eventDomains", service_name="microservices",
      payload='{ "id" : {{event_id}} }', 
      produces='{"result" : "{{return_0}}" }')
@task(returns=1)
def get_domains(event_id):
    """
    """
    pass
    
#@on_failure(management='IGNORE', returns=0)    
@http(request="POST", resource="eventSetState", service_name="microservices",
      payload='{ "id" : {{event_id}}, "state": "{{state}}" }', 
      produces='{"result" : "{{return_0}}" }')
@task(returns=1)
def set_event_state(event_id, state):
    """
    """
    pass  

#@on_failure(management='IGNORE', returns=0)    
@http(request="POST", resource="eventGetRegion", service_name="microservices",
      payload='{ "id" : "{{region_id}}" }', 
      produces='{"result" : "{{return_0}}" }')
@task(returns=1)
def get_event_region(region_id):
    """
    """
    pass      
    
#@on_failure(management='IGNORE', returns=0)    
@http(request="POST", resource="presource", service_name="microservices",
      payload='{ "id" : {{event_id}}, "region": "{{region_id}}" }', 
      produces='{"result" : "{{return_0}}" }')
@task(returns=1)
def pre_source(event_id, region_id):
    """
    """
    pass     
    
#@on_failure(management='IGNORE', returns=0)    
#, "base" : {{base_name}}, "resources" : {{resources}} 
@http(request="POST", resource="source", service_name="microservices",
      payload='{ "event" : {{alert}}, "id" : {{event_id}}, \
                 "domain" : {{domain}}, "setup" : {{precmt}} }',
      produces='{"result" : "{{return_0}}"}')
@task(returns=1)
def source_calculation(alert, event_id, domain, precmt):
    """
    """
    pass  
    
#@on_failure(management='IGNORE', returns=0)    
@http(request="POST", resource="computeResources", service_name="microservices",
      payload='{ "id" : {{event_id}}, "domain": {{domain}} }', 
      produces='{"result" : "{{return_0}}" }')
@task(returns=1)
def compute_resources(event_id, domain):
    """
    """
    pass    
    
#@on_failure(management='IGNORE', returns=0)
@http(request="POST", resource="SourceBuilding", service_name="sourcebuilding",
      payload='{ "event" : {{alert}}, "id" : {{event_id}}, "CMT" : {{cmt}}, \
                 "trial" : "{{trial}}", "domain" : {{domain}}, \
                 "resources" : {{resources}} }',
      produces='{"result" : "{{return_0}}"}')
@task(returns=1)
def compute_source_building(event_id, alert, trial, cmt, domain, resources):
    """
    """
    pass
    
#@on_failure(management='IGNORE', returns=0)
@http(request="POST", resource="inputParametersBuilder", service_name="microservices",
      payload='{ "id" : {{event_id}}, "event" : {{alert}}, "CMT" : {{cmt}}, \
                 "builtSource" : {{builtSource}}, "domain" : {{domain}}, \
                 "resources" : {{resources}} }',
      produces='{"result" : "{{return_0}}"}')
@task(returns=1)
def build_input_parameters(event_id, alert, cmt, builtSource, domain, resources):
    """
    """
    pass
    
#@on_failure(management='IGNORE', returns=0)
@http(request="POST", resource="SimulatorPrepare", service_name="simulator",
      payload='{ "id" : {{event_id}}, "trial" : "{{trial}}", \
                 "input" : {{input}}, "resources" : {{resources}} }',
      produces='{"result" : "{{return_0}}"}')
@task(returns=1)
def build_simulator_parameters(event_id, trial, input, resources):
    """
    """
    pass
    
#@on_failure(management='IGNORE', returns=0)
@http(request="POST", resource="SimulatorRun", service_name="simulator",
      payload='{ "id" : {{event_id}}, "trial" : "{{trial}}", \
                 "input" : {{input}}, "resources" : {{resources}} }',
      produces='{"result" : "{{return_0}}"}')
@task(returns=1)
def run_simulator(event_id, trial, input, resources):
    """
    """
    pass
    
#@on_failure(management='IGNORE', returns=0)
@http(request="POST", resource="SimulatorPost", service_name="simulator",
      payload='{ "id" : {{event_id}}, "trial" : "{{trial}}", \
                 "resources" : {{resources}} }',
      produces='{"result" : "{{return_0}}"}')
@task(returns=1)
def run_simulator_post(event_id, simulator_result, trial, resources):
    """
    """
    pass    
    
#@on_failure(management='IGNORE', returns=0)
@http(request="POST", resource="SimulatorPostSwarm", service_name="simulator",
      payload='{ "id" : {{event_id}}, "base" : "{{base}}", \
                 "domain" : {{domain}}, "resources" : {{resources}} }',
      produces='{"result" : "{{return_0}}"}')
@task(returns=1)
def run_simulator_post_swarm(event_id, base, domain, resources):
    """
    """
    pass       
    
#@on_failure(management='IGNORE', returns=0)
@http(request="POST", resource="SimulatorPlots", service_name="simulator",
      payload='{ "id" : {{event_id}}, "base" : "{{base}}", \
                 "domain" : {{domain}}, "resources" : {{resources}} }',
      produces='{"result" : "{{return_0}}"}')
#@task(returns=1, results=COLLECTION_IN)
@task(returns=1)
def run_simulator_plots(event_id, simulator_post_results, base, domain, resources):
    """
    """
    pass    
    

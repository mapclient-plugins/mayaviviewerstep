'''
MAP Client, a program to generate detailed musculoskeletal models for OpenSim.
    Copyright (C) 2012  University of Auckland
    
This file is part of MAP Client. (http://launchpad.net/mapclient)

    MAP Client is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MAP Client is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MAP Client.  If not, see <http://www.gnu.org/licenses/>..
'''
import os
import json
os.environ['ETS_TOOLKIT'] = 'qt4'
import random
import string

from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint

import numpy as np
from mapclientplugins.mayaviviewerstep.mayaviviewerdata import StepState
from mapclientplugins.mayaviviewerstep.widgets.configuredialog import ConfigureDialog
from mapclientplugins.mayaviviewerstep.widgets.mayaviviewerwidget import MayaviViewerWidget

# from mappluginutils.mayaviviewer
from gias2.mappluginutils.mayaviviewer.mayaviviewerobjects import MayaviViewerObjectsContainer
from gias2.mappluginutils.mayaviviewer.mayaviviewerfieldworkmodel import MayaviViewerFieldworkModel
from gias2.mappluginutils.mayaviviewer.mayaviviewergiasscan import MayaviViewerGiasScan
from gias2.mappluginutils.mayaviviewer.mayaviviewerdatapoints import MayaviViewerDataPoints
from gias2.mappluginutils.mayaviviewer import mayaviviewerfieldworkmeasurements as MVFM

class MayaviViewerStep(WorkflowStepMountPoint):
    '''
    Step for displaying 3D objects using mayavi.
    '''
    
    def __init__(self, location):
        super(MayaviViewerStep, self).__init__('Mayavi 3D Model Viewer', location)
        self._category = 'Visualisation'
        self._state = StepState()
        # self._icon = QtGui.QImage(':/zincmodelsource/images/zinc_model_icon.png')   # change this
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'ju#fieldworkmodeldict'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'ju#fieldworkmeasurementdict'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#pointclouddict'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'ju#giasscandict'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'ju#simplemeshdict'))
        self._widget = None
        self._configured = False

        self._addObjectMethods = [self._addFieldworkModels,
                                  self._addFieldworkMeasurements,
                                  self._addPointClouds,
                                  self._addImages,
                                  self._addSimplemeshes,
                                  ]
        self.objectContainer = MayaviViewerObjectsContainer()

    def configure(self):
        d = ConfigureDialog(self._main_window)
        d.setModal(True)
        if d.exec_():
            self._state = d.getState()
            self.serialize()
            
        self._configured = d.validate()
        if self._configured and self._configuredObserver:
            self._configuredObserver()
    
    def getIdentifier(self):
        return self._state._identifier
     
    def setIdentifier(self, identifier):
        self._state._identifier = identifier

    def serialize(self):
        '''
        Add code to serialize this step to disk. Returns a json string for
        mapclient to serialise.
        '''
        config = {'identifier':self._state._identifier,
                  'discretisation':self._state._discretisation,
                  'displaynodes':self._state._displayNodes,
                  'renderargs':self._state._renderArgs,
                    }
        return json.dumps(config, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def deserialize(self, string):
        '''
        Add code to deserialize this step from disk. Parses a json string
        given by mapclient
        '''
        config = json.loads(string)

        self._state._identifier = config['identifier']
        self._state._discretisation = config['discretisation']
        self._state._displayNodes = config['displaynodes']
        self._state._renderArgs = config['renderargs']

        if self._state._displayNodes=='True':
            self._state._displayNodes = True
        elif self._state._displayNodes=='False':
            self._state._displayNodes = False

        d = ConfigureDialog(self._main_window)
        self._configured = d.validate()
 
    def setPortData(self, index, dataIn):
        if not isinstance(dataIn, dict):
            raise TypeError('mayaviviewerstep expects a dictionary as input')

        self._addObjectMethods[index](dataIn)

    def execute(self):
        print('launching MayaviViewerStep')
        # if not self._widget:
        self._widget = MayaviViewerWidget(self.objectContainer)
        self._widget._ui.closeButton.clicked.connect(self._doneExecution)
        self._widget.setModal(True)

        self._setCurrentWidget(self._widget)

    def _addFieldworkModels(self, D):
        for name, model in list(D.items()):
            name = name+'#'+'FWModel'
            renderArgs = eval(self._state._renderArgs)
            obj = MayaviViewerFieldworkModel(name, model, [8,8], evaluator=None,
                                             renderArgs=renderArgs, fields=None,
                                             fieldName=None, PC=None)
            self.objectContainer.addObject(name, obj)

    def _addFieldworkMeasurements(self, D):
        for name, M in list(D.items()):
            name = name+'#'+'FWMeasure'
            renderArgs = eval(self._state._renderArgs)

            # a bit hacky yea
            if 'femur' in name.lower():
                print('ADDING MEASUREMENT', name)
                obj = MVFM.MayaviViewerFemurMeasurements(name, M)
                self.objectContainer.addObject(name, obj)
        
    def _addPointClouds(self, D):
        for name, P in list(D.items()):
            name = name+'#'+'DC'
            renderArgs = eval(self._state._renderArgs)
            obj = MayaviViewerDataPoints(name, P, renderArgs={'mode':'point', 'color':(0,1,0)})
            self.objectContainer.addObject(name, obj)
 
    def _addImages(self, D):
        for name, S in list(D.items()):
            name = name+'#'+'IM'
            renderArgs = eval(self._state._renderArgs)
            obj = MayaviViewerGiasScan(name, S, renderArgs=renderArgs)
            self.objectContainer.addObject(name, obj)

        
    def _addSimplemeshes(self, D):
        pass
        # for name, S in D.items():
        #     renderArgs = eval(self._state._renderArgs)
        #     obj = MayaviViewerSimpleMesh(name, model, renderArgs=renderArgs)
        #     self.objectContainer.addObject(name, obj)

def getConfigFilename(identifier):
    return identifier + '.conf'

def generateIdentifier(char_set=string.ascii_uppercase + string.digits):
    return ''.join(random.sample(char_set*6,6))
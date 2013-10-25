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
os.environ['ETS_TOOLKIT'] = 'qt4'
import random
import string
from PySide import QtCore, QtGui

from mountpoints.workflowstep import WorkflowStepMountPoint

import numpy as np
from mayaviviewerstep.mayaviviewerdata import StepState
from mayaviviewerstep.widgets.configuredialog import ConfigureDialog
from mayaviviewerstep.widgets.mayaviviewerwidget import MayaviViewerWidget, MayaviViewerObjectsContainer, MayaviViewerFieldworkModel

class MayaviViewerStep(WorkflowStepMountPoint):
    '''
    fieldvi view model step displays a given fieldwork model 
    using the fieldvi widget
    '''
    
    def __init__(self, location):
        super(MayaviViewerStep, self).__init__('Mayavi 3D Model Viewer', location)
        self._state = StepState()
        self._icon = QtGui.QImage(':/zincmodelsource/images/zinc_model_icon.png')   # change this
        # self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port', 'http://physiomeproject.org/workflow/1.0/rdf-schema#uses', 'ju#fieldviviewer'))
        # self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port', 'http://physiomeproject.org/workflow/1.0/rdf-schema#uses', 'ju#femurmeasurements'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port', 'http://physiomeproject.org/workflow/1.0/rdf-schema#uses', 'ju#fieldworkmodeldict'))
        # self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port', 'http://physiomeproject.org/workflow/1.0/rdf-schema#provides', 'ju#fieldviviewer'))
        self._widget = None
        self._configured = False

    def configure(self):
        d = ConfigureDialog(self._state)
        d.setModal(True)
        if d.exec_():
            self._state = d.getState()
            self.serialize(self._location)
            
        self._configured = d.validate()
        if self._configured and self._configuredObserver:
            self._configuredObserver()
    
    def getIdentifier(self):
        return self._state._identifier
     
    def setIdentifier(self, identifier):
        self._state._identifier = identifier
     
    def serialize(self, location):
        configuration_file = os.path.join(location, getConfigFilename(self._state._identifier))
        s = QtCore.QSettings(configuration_file, QtCore.QSettings.IniFormat)
        s.beginGroup('state')
        s.setValue('identifier', self._state._identifier)
        s.setValue('discretisation', self._state._discretisation)
        s.setValue('displaynodes', self._state._displayNodes)
        s.setValue('renderargs', self._state._renderArgs)
        s.endGroup()
     
    def deserialize(self, location):
        configuration_file = os.path.join(location, getConfigFilename(self._state._identifier))
        s = QtCore.QSettings(configuration_file, QtCore.QSettings.IniFormat)
        s.beginGroup('state')
        self._state._identifier = s.value('identifier', '')
        self._state._discretisation = s.value('discretisation', '')
        if s.value('displaynodes', '')=='True':
            self._state._displayNodes = True
        else:
            self._state._displayNodes = False
        self._state._renderArgs = s.value('renderargs', '')
        s.endGroup()
        d = ConfigureDialog(self._state)
        self._configured = d.validate()
        pass
 
    def execute(self, dataIn):
        print 'launching MayaviViewerStep'

        # package models the for viewer
        objectContainer = MayaviViewerObjectsContainer()
        for name, model in dataIn.items():
            # only GFs
            renderArgs = eval(self._state._renderArgs)
            obj = MayaviViewerFieldworkModel(name, model, [8,8], evaluator=None, renderArgs=renderArgs, fields=None, fieldName=None, PC=None)
            objectContainer.addObject(name, obj)

        if not self._widget:
            # self._widget = MayaviViewerWidget(objectContainer, parent=self)
            self._widget = MayaviViewerWidget(objectContainer)
            self._widget._ui.closeButton.clicked.connect(self._doneExecution)
            self._widget.setModal(True)

        self._setCurrentWidget(self._widget)
     
def getConfigFilename(identifier):
    return identifier + '.conf'

def generateIdentifier(char_set=string.ascii_uppercase + string.digits):
    return ''.join(random.sample(char_set*6,6))
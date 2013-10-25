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

from PySide.QtGui import QDialog, QFileDialog, QDialogButtonBox, QAbstractItemView, QTableWidgetItem
from PySide.QtCore import Qt

from mayaviviewerstep.widgets.ui_mayaviviewerwidget import Ui_Dialog
from traits.api import HasTraits, Instance, on_trait_change, \
    Int, Dict

from fieldwork.field import geometric_field
from mayaviviewerobjects import colours, MayaviViewerObjectsContainer, MayaviViewerFieldworkModel

class MayaviViewerWidget(QDialog):
    '''
    Configure dialog to present the user with the options to configure this step.
    '''

    GFD = [10,10]
    displayGFNodes = True
    defaultColor = colours['bone']
    objectTableHeaderColumns = {'visible':0, 'name':1, 'type':2}
    mergeGFVertices = False

    def __init__(self, viewerObjects, parent=None):
        '''
        Constructor
        '''
        QDialog.__init__(self, parent)
        self._ui = Ui_Dialog()
        self._ui.setupUi(self)

        # self._view = self._ui.MayaviScene.visualisation.view
        self._scene = self._ui.MayaviScene.visualisation.scene
        if isinstance(viewerObjects, MayaviViewerObjectsContainer):
            self._objects = viewerObjects       # models, point clouds, tri-mesh, measurements etc to be rendered {name:(type, object)}
        else:
            raise TypeError, 'viewerObject must be a MayaviViewerObjects instance'

        self._makeConnections()
        self._visibleCheckBoxes = {}
        self._initialiseObjectTable()
        
        self.selectedObjectName = None

        # self.testPlot()
        self.drawGFs()

    def _makeConnections(self):
        self._ui.tableWidget.itemClicked.connect(self._tableItemClicked)
        self._ui.tableWidget.itemChanged.connect(self._visibleBoxChanged)

    def _initialiseObjectTable(self):

        self._ui.tableWidget.setRowCount(self._objects.getNumberOfObjects())
        self._ui.tableWidget.verticalHeader().setVisible(False)
        self._ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._ui.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self._ui.tableWidget.resizeColumnToContents(self.objectTableHeaderColumns['visible'])
        row = 0
        for name in self._objects.getObjectNames():
            obj = self._objects.getObject(name)
            self._addObjectToTable(row, name, obj)
            row += 1

    def _addObjectToTable(self, row, name, obj):
        typeName = obj.typeName
        print typeName
        print name
        self._ui.tableWidget.setItem(row, self.objectTableHeaderColumns['name'], QTableWidgetItem(name))
        self._ui.tableWidget.setItem(row, self.objectTableHeaderColumns['type'], QTableWidgetItem(typeName))

        checkbox = QTableWidgetItem()
        checkbox.setCheckState(Qt.Checked)
        self._ui.tableWidget.setItem(row, self.objectTableHeaderColumns['visible'], checkbox); 
        self._visibleCheckBoxes[name] = checkbox

    def _tableItemClicked(self):
        selectedRow = self._ui.tableWidget.currentRow()
        self.selectedObjectName = self._ui.tableWidget.item(selectedRow, self.objectTableHeaderColumns['name']).text()
        self._populateScalarsDropDown(self.selectedObjectName)
        print selectedRow
        print self.selectedObjectName

    def _visibleBoxChanged(self):
        # get name of object selected
        name = self._getSelectedObjectName()

        # get visible status
        visible = self._visibleCheckBoxes[name].checkState()

        # toggle visibility
        obj = self._objects.getObject(name)
        if obj.sceneObject:
            obj.setVisibility(visible)
        else:
            obj.draw(self._scene)

    def _populateScalarsDropDown(self, objectName):
        pass

    def _scalarSelectionChanged(self):
        name = self._getSelectedObjectName()
        scalarName = self._getSelectedScalarName()
        self._objects.getObject(name).updateScalar(scalarName, self.scene)

    def _getSelectedObjectName(self):
        return self.selectedObjectName

    def _getSelectedScalarName(self):
        return 'none'

    #===============================================================================#
    def _drawGeometricField( self, name ):
        self._objects.getObject(name).draw(self._scene)

    def drawGFs(self):
        for name in self._objects.getObjectNames():
            self._drawGeometricField(name)

    #================================================================#
    @on_trait_change('scene.activated')
    def testPlot(self):
        # This function is called when the view is opened. We don't
        # populate the scene when the view is not yet open, as some
        # VTK features require a GLContext.
        print 'trait_changed'

        # We can do normal mlab calls on the embedded scene.
        self._scene.mlab.test_points3d()


    # def _saveImage_fired( self ):
    #     self.scene.mlab.savefig( str(self.saveImageFilename), size=( int(self.saveImageWidth), int(self.saveImageLength) ) )
        
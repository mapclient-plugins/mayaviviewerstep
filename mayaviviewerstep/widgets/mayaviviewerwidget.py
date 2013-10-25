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

from fieldwork.field import geometric_field

colours = {'bone':(0.84705882, 0.8, 0.49803922)}

class MayaviViewerObject(object):

    def __init__(self):
        pass

    def draw(self, scene):
        pass

    def setScalarSelection(self, scalarName):
        self.scalarName = scalarName

    def setVisibility(self, visible):
        pass

    def updateGeometry(self, params):
        pass

    def updateScalar(self, scalarName):
        pass


class MayaviViewerSceneObject(object):

    def __init__(self):
        pass

class MayaviViewerFieldworkModel(MayaviViewerObject):

    typeName = 'fieldworkmodel'

    def __init__(self, name, model, discret, evaluator=None, renderArgs=None, fields=None, fieldName=None, PC=None):
        self.name = name
        self.model = model
        self.discret = discret
        
        if evaluator==None:
            self.evaluator = geometric_field.makeGeometricFieldEvaluatorSparse( self.model, self.discret )
        else:
            self.evaluator = evaluator

        if renderArgs==None:
            self.renderArgs = {}
        else:
            self.renderArgs = renderArgs
        
        self.fields = fields
        self.fieldName = fieldName
        self.PC = PC
        self.sceneObject = None
        self._uniqueVertexIndices = None
        self.mergeGFVertices = False
        self.defaultColour = colours['bone']

    def setScalarSelection(self, fieldName):
        self.fieldName = fieldName

    def setVisibility(self, visible):
        self.sceneObject.setVisibility(visible)

    def draw(self, scene):
        scene.disable_render = True
        P = self.evaluator( self.model.get_field_parameters().ravel() )
        
        # calc scalar
        S = None
        if self.fieldName != 'none':
            if self.fieldName == 'mean curvature':
                K,H,k1,k2 = self.model.evaluate_curvature_in_mesh( self.discret )
                S = H
            elif self.fieldName == 'gaussian curvature':
                K,H,k1,k2 = self.model.evaluate_curvature_in_mesh( self.discret )
                S = K
            else:
                # check if S is a field that needs evaluating - TODO
                S = self.fields[self.fieldName]
                        
        # draw
        if g.ensemble_field_function.dimensions==2:
            # triangulate vertices
            T = self.model.triangulator._triangulate( self.discret )
            
            if mergeGFVertices:
                print scipy.unique(T).shape
                print scipy.where(P==0.0)[0].shape
                
                P, T, self._uniqueVertexIndices, vertMap = self.model.triangulator._mergePoints2( P.T )
                P = P.T
                
                print scipy.unique(T).shape
                print scipy.where(P==0.0)[0].shape
                
                if S!=None:
                    S = S[self.uniqueVertexIndices]
            
            if (S==None) or (S=='none'):
                print 'S = None'
                mayaviMesh = scene.mlab.triangular_mesh( P[0], P[1], P[2], T, name=self.name, color=color, **self.renderArgs )
            else:
                print S
                mayaviMesh = scene.mlab.triangular_mesh( P[0], P[1], P[2], T, scalars=S, name=self.name, **self.renderArgs )

        elif self.model.ensemble_field_function.dimensions==1:
            mayaviMesh = self.model._draw_curve( [self.discret[0]], name=self.name, **self.renderArgs )
            
        mayaviPoints = self.model._plot_points(glyph='sphere', label=None, scale=1.0, figure=scene)
        if not self.displayGFNodes:
            mayaviPoints.visible = False

        self._sceneObject = MayaviViewerFieldworkModelSceneObject(self.name, mayaviMesh, mayaviP)
        scene.disable_render = False

        return self._sceneObject

    def updateGeometry( self, params, scene ):
        
        if self.sceneObject==None:
            self.model.set_field_parameters(params)
            self.draw(scene)
        else: 
            V = self.evaluator(params)
            p = params.reshape((3,-1))  
            
            if self.mergeGFVertices:
                V = V[:,self.uniqueVertexIndices]

            self.sceneObject.mesh.mlab_source.set( x=V[0], y=V[1], z=V[2] )
            self.sceneObject.points.mlab_source.set(x=p[0], y=p[1], z=p[2])

    def updateScalar(self, fieldName, scene):
        self.setScalarSelection(fieldName)
        if self.sceneObject==None:
            self.model.set_field_parameters(params)
            self.draw(scene)
        else: 
            scalar = self._fields[self.fieldName]
            
            if scalar==None:
                if 'color' not in self.renderArgs:
                    colour = self.defaultColour
                else:
                    colour = self.renderArgs['color']
                    
                self.sceneObject.mesh.actor.mapper.scalar_visibility=False
                self.sceneObject.mesh.actor.property.specular_color = colour
                self.sceneObject.mesh.actor.property.diffuse_color = colour
                self.sceneObject.mesh.actor.property.ambient_color = colour
                self.sceneObject.mesh.actor.property.color = colour
            else:
                if self.mergeGFVertices:
                    scalar = scalar[self.uniqueVertexIndices]
                self.sceneObject.mesh.mlab_source.set( scalars=scalar )
                self.sceneObject.mesh.actor.mapper.scalar_visibility=True
      
    # def drawElementBoundaries( self, name, GD, evaluatorMaker, nNodesElemMap, elemBasisMap, renderArgs ):
    #     g = self.geometricFields[name]
        
    #     self.bCurves[name] = {}
    #     for elemN in g.ensemble_field_function.mesh.elements.keys():
    #         self.bCurves[name][name+'_elem_'+str(elemN)] = g.makeElementBoundaryCurve( elemN, nNodesElemMap, elemBasisMap )
            
    #     for b in self.bCurves[name]:
    #         evaluator = evaluatorMaker( self.bCurves[name][b], GD )
    #         self.addGeometricField( b, self.bCurves[name][b], evaluator, GD, renderArgs )
    #         self._drawGeometricField( b )

    # def hideElementBoundaries( self, name ):
    #     for b in self.bCurves[name]:
    #         SOb = self.sceneObjectGF.get(b)
    #         if SOb!=None:
    #             SOb.visible=False
        
    # def showElementBoundaries( self, name ):
    #     for b in self.bCurves[name]:
    #         SOb = self.sceneObjectGF.get(b)
    #         if SOb!=None:
    #             SOb.visible=True


class MayaviViewerFieldworkModelSceneObject(MayaviViewerSceneObject):

    typeName = 'fieldworkmodel'

    def __init__(self, name, mesh, points, elemLines):
        self.name = name
        self.mesh = mesh
        self.points = points
        self.elemLines = elemLines

    def setVisibility(self, visible):
        if self.mesh:
            self.mesh.visible = visible
        if self.points:
            self.points.visible = visible
        if self.elemLines:
            self.elemLines = visible

class MayaviViewerObjectsContainer(object):
    """
    stores objects to be rendered in the viewer
    """
    def __init__(self):
        self._objects = {}

    def addObject(self, name, obj):
        if name in self._objects.keys():
            raise ValueError, 'name must be unique'

        if not isinstance(obj, MayaviViewerObject):
            raise TypeError, 'obj must a MayaviViewerObject'

        self._objects[name] = obj

    def getObjectAll(self, name):
        return self._objects[name]

    def getObjectType(self, name):
        return self._objects[name][0]

    def getObject(self, name):
        return self._objects[name][1]

    def getObjectNamesOfType(self, typeName):
        ret = []
        for name, (t, o) in self._objects.items():
            if typeName==t:
                ret.append(name)

        return ret

    def getObjectNames(self):
        return self._objects.keys()

    def getNumberOfObjects(self):
        return len(self._objects.keys())


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

        self._view = self._ui.MayaviScene.visualisation.view
        self._scene = self._ui.MayaviScene.visualisation.scene
        if isinstance(viewerObjects, MayaviViewerObjectsContainer):
            self._objects = viewerObjects       # models, point clouds, tri-mesh, measurements etc to be rendered {name:(type, object)}
        else:
            raise TypeError, 'viewerObject must be a MayaviViewerObjects instance'


        # self._sceneObjects = {}  # handles to things added to mayavi

        self._populateObjectTable()
        self._makeConnections()

        self.selectedObjectName = None

    def _populateObjectTable(self):

        self._ui.tableWidget.setRowCount(self._objects.getNumberOfObjects())
        self._ui.tableWidget.verticalHeader().setVisible(False)
        self._ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self._ui.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        
        row = 0
        for name in self._objects.getObjectNames():
            typeName = self._objects.getObjectType(name)
            self._ui.tableWidget.setItem(row, self.objectTableHeaderColumns['name'], QTableWidgetItem(name))
            self._ui.tableWidget.setItem(row, self.objectTableHeaderColumns['type'], QTableWidgetItem(typeName))

    def _makeConnections(self):
        self._ui.tableWidget.itemClicked.connect(self._tableItemClicked)
    
    def _tableItemClicked(self):
        selectedRow = self._ui.tableWidget.currentRow()
        self.selectedObjectName = self._ui.tableWidget.item(selectedRow, self.objectTableHeaderColumns['name'])
        self._populateScalarsDropDown(self.selectedObjectName)


    def _populateScalarsDropDown(self, objectName):
        pass

    def _visibleBoxChanged(self):
        # get name of object selected
        name = self._getSelectedObjectName()

        # get visible status
        visible = True

        # toggle visibility
        obj = self._objects.getObject(name)
        if obj.sceneObject:
            obj.setVisibility(visible)
        else:
            obj.draw(self.scene)

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
        self._objects.getObject(name).draw(self.scene, scalarName)

    #================================================================+#
    # def _saveImage_fired( self ):
    #     self.scene.mlab.savefig( str(self.saveImageFilename), size=( int(self.saveImageWidth), int(self.saveImageLength) ) )
        
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

from PySide.QtGui import QDialog, QFileDialog, QDialogButtonBox, QAbstractItemView, QTableWidgetItem
from PySide.QtCore import Qt

from mayaviviewerstep.widgets.ui_mayaviviewerwidget import Ui_MayaviViewerWidget

class MayaviViewerObject(class):

    def __init__(self):
        pass

class MayaviViewerSceneObject(class):

    def __init__(self):
        pass

class MayaviViewerFieldworkModel(MayaviViewerObject):

    typeName = 'fieldworkmodel'

    def __init__(self, name, model, discret, evaluator=None, renderArgs=None, fields=None, PC=None):
        self.name = name
        self.model = model
        self.discret = discret
        self.evaluator = evaluator
        if renderArgs==None:
            self.renderArgs = {}
        else:
            self.renderArgs = renderArgs
        self.fields = fields
        self.PC = PC

class MayaviViewerFieldworkModelSceneObject(MayaviViewerSceneObject):

    typeName = 'fieldworkmodel'

    def __init__(self, name, mesh, points, elemLines):
        self.name = name
        self.mesh = mesh
        self.points = points
        self.elemLines = elemLines

class MayaviViewerObjectsContainer(class):
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

        self._object[name] = (typeName, obj)

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
    colours = {'bone':(0.84705882, 0.8, 0.49803922)}
    defaultColor = colours['bone']
    objectTableHeaderColumns = {'visible':0, 'name':1, 'type':2}
    mergeGFVertices = False

    def __init__(self, viewerObjects, parent=None):
        '''
        Constructor
        '''
        QDialog.__init__(self, parent)
        self._ui = Ui_MayaviViewerWidget()
        self._ui.setupUi(self)

        self._view = self._ui.MayaviScene.visualisation.view
        self._scene = self._ui.MayaviScene.visualisation.scene
        if isinstance(viewerObjects, MayaviViewerObjectsContainer):
            self._objects = viewerObjects       # models, point clouds, tri-mesh, measurements etc to be rendered {name:(type, object)}
        else:
            raise TypeError, 'viewerObject must be a MayaviViewerObjects instance'


        self._sceneObjects = {}  # handles to things added to mayavi

        self._makeConnections()
        self._populateObjectTable()

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
        objectName = self._ui.tableWidget.item(selectedRow, self.objectTableHeaderColumns['name'])
        self._populateScalarsDropDown(self, objectName)

    def _populateScalarsDropDown(self, objectName):
        pass

    def _visibleBoxChanged(self):
        # get name of object selected

        # get type 

        # toggle visibility

    def _getScalarName(self):
        return 'none'

    #===============================================================================#
    def _drawGeometricField( self, name ):
        
        self.scene.disable_render = True
        
        modelObject = self._objects.getOject(name)
        g = modelObject.GF
        evaluator = modelObject.evaluator
        renderArgs = modelObject.renderArgs
        # evaluate mesh at triangle vertices
        # evaluate field at the desired element descritisation
        # P[0] = x, P[1] = y, P[2] = z
        P = evaluator( g.get_field_parameters().ravel() )
        GFD = self.GFDSpecific[name]
        renderArgs = self.GFRenderArgs[name]
        
        # calc scalar
        S = None
        scalarName = self._getScalarName()
        if scalarName != 'none':
            if scalarName == 'mean curvature':
                K,H,k1,k2 = g.evaluate_curvature_in_mesh( GFD )
                S = H
            elif scalarName == 'gaussian curvature':
                K,H,k1,k2 = g.evaluate_curvature_in_mesh( GFD )
                S = K
            else:
                S = self.modelObject.fields[scalarName]
                        
        # draw
        if g.ensemble_field_function.dimensions==2:
            # triangulate vertices
            T = g.triangulator._triangulate( modelObject.discret )
            
            if self.mergeGFVertices:
                print scipy.unique(T).shape
                print scipy.where(P==0.0)[0].shape
                
                P, T, self.uniqueVertexIndices, vertMap = g.triangulator._mergePoints2( P.T )
                P = P.T
                
                print scipy.unique(T).shape
                print scipy.where(P==0.0)[0].shape
                
                if S!=None:
                    S = S[self.uniqueVertexIndices]
            
            if (S==None) or (S=='none'):
                print 'S = None'
                mayaviMesh = self.scene.mlab.triangular_mesh( P[0], P[1], P[2], T, name=name, color=self.defaultColor, **renderArgs )
            else:
                print S
                mayaviMesh = self.scene.mlab.triangular_mesh( P[0], P[1], P[2], T, scalars=S, name=name, **renderArgs )

        elif g.ensemble_field_function.dimensions==1:
            mayaviMesh = g._draw_curve( [GFD[0]], name=name, **renderArgs )
            
        mayaviPoints = g._plot_points(glyph='sphere', label=None, scale=1.0, figure=None)
        if not self.displayGFNodes:
            mayaviPoints.visible = False

        self._sceneObjects[name] = MayaviViewerFieldworkModelSceneObject(name, mayaviMesh, mayaviP)
        
        self.scene.disable_render = False

    def _GFVisible_changed( self ):
        try:
            self.sceneObjectGF[self.GFList0].visible = self.GFVisible
            if self.displayGFNodes:
                self.sceneObjectGFPoints[self.GFList0].visible = self.GFVisible
        except KeyError:
            if self.GFVisible:
                self._drawGeometricField( self.GFList0 )

    def _GFUpdate_fired( self ):
        self.updateGeometricField( self.GFList0 )

    def _renderGeometricFields_fired( self ):
        """ redraw all geometric fields
        """
        for i in self.sceneObjectGF.values():
            i.remove()
            
        self.sceneObjectGF = {}
        for i in self.geometricFields.keys():
            self._drawGeometricField( i )

    def updateGeometricField( self, name, params=None ):
        
        if self.sceneObjectGF.get(name) == None:
            self._drawGeometricField( name )
        else:
            if params == None:
                params = self.geometricFields[name].get_field_parameters().ravel()
    
            V = self.GFEvaluators[name]( params )
            p = params.reshape((3,-1))  
            
            if self.mergeGFVertices:
                V = V[:,self.uniqueVertexIndices]

            scalar = self._getGFScalarData(self.GFScalarList0, name)
            renderArgs = self.GFRenderArgs[name]
            
            if scalar==None:
                if 'color' not in renderArgs:
                    color = self.defaultColor
                else:
                    color = renderArgs['color']
                    
                self.sceneObjectGF[name].actor.mapper.scalar_visibility=False
                self.sceneObjectGF[name].actor.property.specular_color = color
                self.sceneObjectGF[name].actor.property.diffuse_color = color
                self.sceneObjectGF[name].actor.property.ambient_color = color
                self.sceneObjectGF[name].actor.property.color = color
                self.sceneObjectGF[name].mlab_source.set( x=V[0], y=V[1], z=V[2] )
            else:
                if self.mergeGFVertices:
                    scalar = scalar[self.uniqueVertexIndices]
                self.sceneObjectGF[name].mlab_source.set( x=V[0], y=V[1], z=V[2], scalars=scalar )
                self.sceneObjectGF[name].actor.mapper.scalar_visibility=True
            
            self.sceneObjectGFPoints[name].mlab_source.set(x=p[0], y=p[1], z=p[2])
            
    def drawElementBoundaries( self, name, GD, evaluatorMaker, nNodesElemMap, elemBasisMap, renderArgs ):
        g = self.geometricFields[name]
        
        self.bCurves[name] = {}
        for elemN in g.ensemble_field_function.mesh.elements.keys():
            self.bCurves[name][name+'_elem_'+str(elemN)] = g.makeElementBoundaryCurve( elemN, nNodesElemMap, elemBasisMap )
            
        for b in self.bCurves[name]:
            evaluator = evaluatorMaker( self.bCurves[name][b], GD )
            self.addGeometricField( b, self.bCurves[name][b], evaluator, GD, renderArgs )
            self._drawGeometricField( b )

    def hideElementBoundaries( self, name ):
        for b in self.bCurves[name]:
            SOb = self.sceneObjectGF.get(b)
            if SOb!=None:
                SOb.visible=False
        
    def showElementBoundaries( self, name ):
        for b in self.bCurves[name]:
            SOb = self.sceneObjectGF.get(b)
            if SOb!=None:
                SOb.visible=True

    #================================================================+#
    def _saveImage_fired( self ):
        self.scene.mlab.savefig( str(self.saveImageFilename), size=( int(self.saveImageWidth), int(self.saveImageLength) ) )
        
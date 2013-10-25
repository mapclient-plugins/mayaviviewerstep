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

from fieldwork.field import geometric_field
import numpy as np

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

    def __init__(self, name, model, discret, evaluator=None, renderArgs=None,\
                 fields=None, fieldName=None, PC=None, displayGFNodes=False,\
                 mergeGFVertices=False):
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
        
        if fields==None:
            self.fields = {}
        else:
            self.fields = fields
        
        self.fieldName = fieldName
        self.PC = PC
        self.sceneObject = None
        self._uniqueVertexIndices = None
        self.mergeGFVertices = mergeGFVertices
        self.displayGFNodes = displayGFNodes
        self.defaultColour = colours['bone']
        if 'color' not in self.renderArgs.keys():
            self.renderArgs['color'] = self.defaultColour

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
                S = self.fields.get(self.fieldName)
                        
        # draw
        if self.model.ensemble_field_function.dimensions==2:
            # triangulate vertices
            T = self.model.triangulator._triangulate( self.discret )
            
            if self.mergeGFVertices:
                print np.unique(T).shape
                print np.where(P==0.0)[0].shape
                
                P, T, self._uniqueVertexIndices, vertMap = self.model.triangulator._mergePoints2( P.T )
                P = P.T
                
                print np.unique(T).shape
                print np.where(P==0.0)[0].shape
                
                if S!=None:
                    S = S[self.uniqueVertexIndices]
            
            if (S==None) or (S=='none'):
                print 'S = None'
                mayaviMesh = scene.mlab.triangular_mesh( P[0], P[1], P[2], T, name=self.name, **self.renderArgs )
            else:
                print S
                mayaviMesh = scene.mlab.triangular_mesh( P[0], P[1], P[2], T, scalars=S, name=self.name, **self.renderArgs )

        elif self.model.ensemble_field_function.dimensions==1:
            mayaviMesh = self.model._draw_curve( [self.discret[0]], name=self.name, **self.renderArgs )
            
        mayaviPoints = self._plot_points(scene)
        if not self.displayGFNodes:
            mayaviPoints.visible = False

        self._sceneObject = MayaviViewerFieldworkModelSceneObject(self.name, mayaviMesh, mayaviPoints)
        scene.disable_render = False

        return self._sceneObject

    def _plot_points( self, scene, glyph='sphere', label=None, scale=0.5):
        """ uses mayavi points3d to show the positions of all points 
        (with labels if label is true)
        
        label can be 'all', or 'landmarks'
        """
        
        # get point positions
        p = np.array(self.model.get_all_point_positions())
        
        if len(p)>0:
            s = np.arange(len(p))
            points_plot = scene.mlab.points3d(p[:,0], p[:,1], p[:,2], s, mode='sphere', scale_mode='none', scale_factor=scale, color=(1,0,0))
                 
            # label all ensemble points with their index number
            if label=='all':
                labels = range(len(p))
                for i in range(len(labels)):
                    l = scene.mlab.text(p[i,0], p[i,1], str(labels[i]), z=p[i,2], line_width=0.01, width=0.005*len(str(labels[i]))**1.1)
            
            elif label=='landmarks':
                m = self.model.named_points_map
                labels = m.keys()
                for label in labels:
                    l = scene.mlab.text(p[m[label]][0], p[m[label]][1], label, z=p[m[label]][2], line_width=0.01, width=0.005*len(label)**1.1)
            return points_plot
        else:
            raise ValueError, 'model has no nodes'

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
    #     for elemN in self.model.ensemble_field_function.mesh.elements.keys():
    #         self.bCurves[name][name+'_elem_'+str(elemN)] = self.model.makeElementBoundaryCurve( elemN, nNodesElemMap, elemBasisMap )
            
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

    def __init__(self, name, mesh, points, elemLines=None):
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
        return self._objects[name].typeName

    def getObject(self, name):
        return self._objects[name]

    def getObjectNamesOfType(self, typeName):
        ret = []
        for name, o in self._objects.items():
            if o.typeName==t:
                ret.append(name)

        return ret

    def getObjectNames(self):
        return self._objects.keys()

    def getNumberOfObjects(self):
        return len(self._objects.keys())
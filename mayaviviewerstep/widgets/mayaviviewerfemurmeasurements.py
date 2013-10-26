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

from mayaviviewerobjects import MayaviViewerSceneObject, MayaviViewerObject
import numpy as np

class MayaviViewerFemurMeasurementsSceneObject(MayaviViewerSceneObject):

    typeName = 'femurMeasurements'

    def __init__(self, name, sceneObjects=None):
        self.name = name
        if sceneObjects==None:
        	self.sceneObjects = {}
        else:
        	self.sceneObjects = sceneObjects

    def addSceneObject(self, name, obj):
    	self.sceneObjects[name] = obj

    def setVisibility(self, visible):
        for obj in self.sceneObjects.values():
        	obj.visible = visible

class MayaviViewerFemurMeasurements(MayaviViewerObject):

	typeName = 'femurmeasurements'
	textMeasurements = ('head_diameter', 'neck_width', 'neck_shaft_angle', 'femoral_axis_length', 'subtrochanteric_width')

	def __init__(self, name, model, measurements, drawWidthTubes=False, text2d=False):
		self.name = name
		self._model = model
		self._M = measurements
		self._drawWidthTubes = drawWidthTubes
		self._text2d = text2d
		self.sceneObject = MayaviViewerFemurMeasurementsSceneObject(self.name)

	def setVisibility(self, visible):
		self.sceneObject.setVisibility(visible)

	def draw(self, scene):
    	# draw axes
		self._drawAxes(scene)		
		# plot head sphere
		self._drawHead(scene)		
		# draw femoral axis length intercepts
		self._drawFemoralAxisLength(scene)			
		# draw neck width and tube
		self._drawNeckWidth(scene)
		# draw subtrochanteric width
		self._drawSubTrochantericWidth(scene)
		# draw midshaft width and tube
		self._drawMidshaftWidth(scene)
		# draw epicondyle intercepts
		self._drawEpicondyleWidth(scene)		
		# add text of measurements
		if self._text2d:
			self._drawText2D(scene)

	def _drawText2D(self, scene):
		tx = 0.02
		ty = 0.02
		tspacing = 0.05
		charWidth = 0.01
		for m in self.textMeasurements:
			value = self._M.measurements[m].value
			mString = '{m}: {v:5.2f}'.format(m=m, v=value)
			sObj = scene.mlab.text(tx, ty, mString, width=len(mString)*charWidth, name='text2d_'+m)
			self.sceneObjects.addSceneObject('text2d_'+m, sObj)
			ty += tspacing

	def _addText3D(self, scene, name, value, unit, mOrigin, offset):
		charWidth = 0.01
		lineWidth = 0.2
		textOrigin = np.array(mOrigin)+np.array(offset)
		textLine = np.array([mOrigin, textOrigin]).T
		mStr = '{}: {:5.2f} {}'.format(name, value, unit)
		texts = scene.mlab.text(textOrigin[0], textOrigin[1], mStr, z=textOrigin[2], width=len(mStr)*charWidth, name='text3d_'+name)
		self.sceneObjects.addSceneObject('text3d_'+name, texts)
		lines = scene.mlab.plot3d(textLine[0], textLine[1], textLine[2], tube_radius=lineWidth, name='text3dline_'+name)
		self.sceneObjects.addSceneObject('text3dline_'+name, lines)

	def _drawAxes(self, scene):
		saPoints = self._M.shaftAxis.eval(np.array([-300,300])).T
		saSObj = scene.mlab.plot3d(saPoints[0], saPoints[1], saPoints[2], name='axis_shaft', tube_radius=1.0 )
		self.sceneObjects.addSceneObject('axis_shaft', saSObj)

		naPoints = self._M.neckAxis.eval(np.array([-100,100])).T
		naSObj = scene.mlab.plot3d(naPoints[0], naPoints[1], naPoints[2], name='axis_neck', tube_radius=1.0 )
		self.sceneObjects.addSceneObject('axis_neck', naSObj)

		ecPoints = self._M.epicondylarAxis.eval(np.array([-100,100])).T
		ecSObj = scene.mlab.plot3d(ecPoints[0], ecPoints[1], ecPoints[2], name='axis_epicondylar', tube_radius=1.0 )	
		self.sceneObjects.addSceneObject('axis_epicondylar', ecSObj)

	def _drawHead(self, scene):
		headM = self._M.measurements['head_diameter']
		C = headM.centre
		headSphere = scene.mlab.points3d( C[0], C[1], C[2], mode='sphere', scale_factor=headM.value, resolution=16, name='glyph_headSphere', color=(0.0,1.0,0.0), opacity=0.3 )
		self.sceneObjects.addSceneObject('glyph_headSphere', headSphere)
		self._addText3D(F, 'head diameter', headM.value, 'mm', C, [-50.0,0,-50])

	def _drawNeckWidth(self, scene):

		# width
		NW = self._M.measurements['neck_width']
		NWC = NW.centre
		NWSup = NW.interceptSup
		NWInf = NW.interceptInf
		# NWMin = NW.searchMin
		# NWMax = NW.searchMax
		# NWPoints = np.array([NWSup, NWC, NWInf, NWMin, NWMax]).T
		NWPoints = np.array([NWSup, NWInf]).T
		NWPoints = scene.mlab.points3d( NWPoints[0], NWPoints[1], NWPoints[2], name='glyph_neckWidthPoints', mode='sphere', scale_factor=5, resolution=16, color=(1.0,0.0,0.0) )
		self.sceneObjects.addSceneObject('glyph_neckWidthPoints', NWPoints)

		NWLinePoints = np.array([NWSup, NWInf]).T
		NWLine = scene.mlab.plot3d(NWLinePoints[0], NWLinePoints[1], NWLinePoints[2], name='glyph_neckWidthLine', tube_radius=1.0 )
		self.sceneObjects.addSceneObject('glyph_neckWidthLine', NWLine)

		self._addText3D(F, 'neck width', NW.value, 'mm', NWC, [0.0,0.0,-100])

		# tube
		if self._drawWidthTubes:
			neckRadiusM = self._M.measurements['neck_width']
			# neckEnds = M.neckAxis.eval(np.array([-50,10])).T
			# NW = M.measurements['neck_width']
			# neckEnds = np.array([NW.searchMin, NW.searchMax]).T
			neckEnds = self._M.neckAxis.eval(np.array([-30,20])).T
			NWTube = scene.mlab.plot3d(neckEnds[0], neckEnds[1], neckEnds[2], name='glyph_neckWidthTube', tube_radius=neckRadiusM.value/2.0, tube_sides=16, color=(0.0,0.0,1.0), opacity=0.3 )
			self.sceneObjects.addSceneObject('glyph_neckWidthTube', NWTube)

	def _drawFemoralAxisLength(self, scene):
		FAL = self._M.measurements['femoral_axis_length']
		H = FAL.headIntercept[1]
		G = FAL.gTrocIntercept[1]
		FALPoints = scene.mlab.points3d( [H[0], G[0]], [H[1], G[1]], [H[2], G[2]], name='glyph_FALPoints', mode='sphere', scale_factor=5, resolution=16, color=(1.0,0.0,0.0) )
		self.sceneObjects.addSceneObject('glyph_FALPoints', FALPoints)
		self._addText3D(F, 'femoral axis length', FAL.value, 'mm', G, [200.0,0.0,-150.0])

	def _drawNeckShaftAngle(self, scene):
		pass
		# NSA = M.measurements['neck_shaft_angle']
		# O = 
		# self._addText3D(F, 'neck shaft angle', NSA.value, 'degrees', O, [-100.0,0.0,0.0])

	def _drawSubTrochantericWidth(self, scene):
		sTW = self._M.measurements['subtrochanteric_width']
		points = np.array([sTW.p1, sTW.p2]).T
		centre = (sTW.p1+sTW.p2)*0.5
		
		sTWPoints = scene.mlab.points3d( points[0], points[1], points[2], name='glyph_sTWPoints', mode='sphere', scale_factor=5, resolution=16, color=(1.0,0.0,0.0) )
		self.sceneObjects.addSceneObject('glyph_sTWPoints', sTWPoints)

		sTWLine = scene.mlab.plot3d(points[0], points[1], points[2], name='glyph_sTWLine', tube_radius=1.0 )
		self.sceneObjects.addSceneObject('glyph_sTWLine', sTWLine)

		self._addText3D(F, 'subtrochanteric width', sTW.value, 'mm', centre, [-100.0,0.0,0.0])

	def _drawMidshaftWidth(self, scene):
		mSW = self._M.measurements['midshaft_width']
		points = np.array([mSW.p1, mSW.p2]).T
		centre = (mSW.p1+mSW.p2)*0.5
		
		mSWPoints = scene.mlab.points3d( points[0], points[1], points[2], name='glyph_midshaftWidthPoints', mode='sphere', scale_factor=5, resolution=16, color=(1.0,0.0,0.0) )
		self.sceneObjects.addSceneObject('glyph_midshaftWidthPoints', mSWPoints)

		mSWLine = scene.mlab.plot3d(points[0], points[1], points[2], name='glyph_midshaftWidthLine', tube_radius=1.0 )
		self.sceneObjects.addSceneObject('glyph_midshaftWidthLine', mSWLine)

		self._addText3D(F, 'midshaft width', mSW.value, 'mm', centre, [-100.0,0.0,0.0])

		# draw midshaft tube
		if drawTube:
			midshaftEnds = self._M.shaftAxis.eval(np.array([-20,20])).T
			mSWTube = scene.mlab.plot3d(midshaftEnds[0], midshaftEnds[1], midshaftEnds[2], name='glyph_midshaftWidthTube', tube_radius=mSW.value/2.0, tube_sides=16, color=(0.0,0.0,1.0), opacity=0.3 )
			self.sceneObjects.addSceneObject('glyph_midshaftWidthTube', mSWTube)

	def _drawEpicondyleWidth(self, scene):
		ECW = self._M.measurements['epicondylar_width']
		# l = EP[ ECW.p1[0] ]
		l = ECW.p1[1]
		# m = EP[ ECW.p2[0] ]
		m = ECW.p2[1]
		c = (l+m)*0.5
		ECWPoints = scene.mlab.points3d( [l[0], m[0]], [l[1], m[1]], [l[2], m[2]], name='glyph_epicondylarWidthPoints', mode='sphere', scale_factor=5, resolution=16, color=(1.0,0.0,0.0) )
		self.sceneObjects.addSceneObject('glyph_epicondylarWidthPoints', ECWPoints)
		self._addText3D(F, 'epicondylar width', ECW.value, 'mm', c, [-50.0,0.0,100.0])
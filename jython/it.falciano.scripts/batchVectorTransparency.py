#!/usr/bin/env jython
#################################################################################
#
# Project:  gvSIG Jython script samples
# Name:     batchVectorTransparency.py
# Purpose:  Apply the same opacity options to a set of vector layers.
# Author:   Antonio Falciano, afalciano@yahoo.it
#
#################################################################################
# Copyright (c) 2011, Antonio Falciano <afalciano@yahoo.it>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
# 
#################################################################################

from gvsiglib import *
from javax.swing import JOptionPane, JFrame, JCheckBox, JSlider, JButton
from java.awt import FlowLayout, Dimension, Color

def getActiveLayers():
	view=gvSIG.getActiveDocument()
	if view.getClass().getCanonicalName() <> 'com.iver.cit.gvsig.project.documents.view.gui.View':
		JOptionPane.showMessageDialog(None, 
			"The active document is not a view.", "Batch Transparency", JOptionPane.WARNING_MESSAGE)
		return
	else:
		mctrl=view.getMapControl()
		mctxt=mctrl.getMapContext()
		layers=mctxt.getLayers()
		activeLayers=layers.getActives()
		return activeLayers

def setAlpha(sym, value):
	
	if outCheckbox.isSelected(): 
		outValue = value
	else:
		outValue = 0
	
	if fillCheckbox.isSelected():
		fillValue = value
	else:
		fillValue = 0
	
	# set alpha for outline
	outline=sym.getOutline()
	outline.setAlpha(outValue)
	# set alpha for fillcolor
	fColor=sym.getFillColor()
	fillColor=Color(fColor.getRed(), fColor.getGreen(), fColor.getBlue(), fillValue)
	sym.setFillColor(fillColor)
	return sym

def action(e):
	
	value = slider.getValue() * 255 / 100
	activeLayers=getActiveLayers()
	for i in range(len(activeLayers)):
		lyr=activeLayers[i]
		if lyr.getClass().getCanonicalName() == "com.iver.cit.gvsig.fmap.layers.FLyrVect":
			legend=lyr.getLegend()			
			if legend.getClassName() == 'com.iver.cit.gvsig.fmap.rendering.SingleSymbolLegend':
				sym = legend.getDefaultSymbol()
				if lyr.getShapeType() == 1:   # points
					color = sym.getColor()
					newColor = Color(color.getRed(), color.getGreen(), color.getBlue(), value)
					sym.setColor(newColor)					
				elif lyr.getShapeType() == 2:  # lines
					sym.setAlpha(value)
				else:
					sym = setAlpha(sym, value)
				legend.setDefaultSymbol(sym)
			else:
				try:
					syms=legend.getSymbols()
					for j in range(len(syms)):
						sym=syms[j]
						if lyr.getShapeType() == 1:   # points
							color = sym.getColor()
							newColor = Color(color.getRed(), color.getGreen(), color.getBlue(), value)
							sym.setColor(newColor)
						elif lyr.getShapeType() == 2:  # lines
							sym.setAlpha(value)
						else:
							sym = setAlpha(sym, value)
						legend.setDefaultSymbol(sym)
				except Exception, e:
					JOptionPane.showMessageDialog(None, legend.getClassName() + " not yet implemented!", 
						"Batch Transparency", JOptionPane.WARNING_MESSAGE)
					accept(e)
	return

def accept(e):
	frame.dispose()
	return

def main():
	
	activeLayers=getActiveLayers()

	if len(activeLayers)==0:
		JOptionPane.showMessageDialog(None, 
			"Add and activate at least one vector layer in the view. Retry!",
			"Batch Transparency", JOptionPane.WARNING_MESSAGE)
		return
	else:
		numFLyrVect=0
		for i in range(len(activeLayers)):
			if activeLayers[i].getClass().getCanonicalName()=="com.iver.cit.gvsig.fmap.layers.FLyrVect":
				numFLyrVect=numFLyrVect+1
		if numFLyrVect==0:
			JOptionPane.showMessageDialog(None, 
				"You have to add and activate at least one vector layer in the view. Retry!", 
				"Batch Transparency", JOptionPane.WARNING_MESSAGE)
			return
		else:
			global frame, outCheckbox, fillCheckbox, slider
			frame = JFrame("Batch Transparency", defaultCloseOperation=JFrame.DISPOSE_ON_CLOSE, 
				bounds=(100, 100, 450, 80), layout=FlowLayout(), resizable=0)

			outCheckbox = JCheckBox("outline", 1)
			fillCheckbox = JCheckBox("fill", 1)

			# Create a horizontal slider with min=0, max=100, value=50
			slider = JSlider()
			slider.setPreferredSize(Dimension(200, 50))
			slider.setValue(100)
			slider.setMajorTickSpacing(25)
			slider.setMinorTickSpacing(5)
			slider.setPaintTicks(1)
			slider.setPaintLabels(1)

			applyButton = JButton("Apply", actionPerformed=action)
			acceptButton = JButton("Accept", actionPerformed=accept)
			
			frame.add(outCheckbox)
			frame.add(fillCheckbox)
			frame.add(slider)
			frame.add(applyButton)
			frame.add(acceptButton)
			
			frame.show()
	return

main()
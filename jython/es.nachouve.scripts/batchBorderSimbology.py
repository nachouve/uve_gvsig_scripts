#!/usr/bin/env jython
#################################################################################
#
# Project:  gvSIG Jython script samples
# Name:     batchBorderSymbology.py
# Purpose:  Apply the same border symbology to a set of vector layers.
# Author:   Nacho Varela, nachouve@gmail.com
#
#################################################################################
# Copyright (c) 2012, Nacho Varela <nachouve@gmail.com>
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

#execfile("/var/tmp/uve_gvsig_scripts/jython/es.nachouve.scripts/batchBorderSimbology.py")
#activeLayers=getActiveLayers()
#legend=activeLayers[0].getLegend()
#legend=activeLayers[0].getLegend()
#sym = legend.getDefaultSymbol()

from gvsiglib import *
from javax.swing import JOptionPane, JFrame, JCheckBox, JSlider, JButton, JLabel, JColorChooser, JTextField
from java.awt import FlowLayout, Dimension, Color

def getActiveLayers():
	view=gvSIG.getActiveDocument()
	if view.getClass().getCanonicalName() <> 'com.iver.cit.gvsig.project.documents.view.gui.View':
		JOptionPane.showMessageDialog(None, 
			"The active document is not a view.", "Border Symbology", JOptionPane.WARNING_MESSAGE)
		return
	else:
		mctrl=view.getMapControl()
		mctxt=mctrl.getMapContext()
		layers=mctxt.getLayers()
		activeLayers=layers.getActives()
		return activeLayers

def setBorder(sym, ncolor, nwidth, nalpha):

	lineColor=Color(ncolor.getRed(), ncolor.getGreen(), ncolor.getBlue(), nalpha)

	# Molaria poner el mismo que el relleno.
	if (sym.getClassName() == 'com.iver.cit.gvsig.fmap.core.symbols.SimpleFillSymbol'):
		outline = sym.getOutline()
		outline.setLineWidth(nwidth)
		outline.setLineColor(ncolor)
		outline.setAlpha(nalpha)
		sym.setOutline(outline)
	else:
		sym.setLineColor(lineColor)
		sym.setLineWidth(nwidth)
		sym.setAlpha(nalpha)
	return sym

def getFirstSymbol():
	color_alpha_width = {}
	activeLayers=getActiveLayers()
	if (len(activeLayers)>0):
		lyr=activeLayers[0]
		if lyr.getClass().getCanonicalName() == "com.iver.cit.gvsig.fmap.layers.FLyrVect":
			legend=lyr.getLegend()
			print legend
			if legend.getClassName() == 'com.iver.cit.gvsig.fmap.rendering.SingleSymbolLegend':
				sym = legend.getDefaultSymbol()
				color_alpha_width["color"] = sym.getColor()
				color_alpha_width["alpha"] = sym.getAlpha()
				if (sym.getClassName() == 'com.iver.cit.gvsig.fmap.core.symbols.SimpleLineSymbol'):
					color_alpha_width["width"] = sym.getLineWidth()
			elif legend.getClassName() == 'com.iver.cit.gvsig.fmap.rendering.VectorialUniqueValueLegend':
				sym = legend.getSymbol(0)
				if (sym.getClassName() == 'com.iver.cit.gvsig.fmap.core.symbols.SimpleFillSymbol'):
					color_alpha_width["color"] = sym.getOutline().getColor()
					color_alpha_width["width"] = sym.getOutline().getLineWidth()
					color_alpha_width["alpha"] = sym.getOutline().getAlpha()
			else:
				try:
					color_alpha_width["color"] = sym.getOutline().getColor()
					color_alpha_width["width"] = sym.getOutline().getLineWidth()
					color_alpha_width["alpha"] = sym.getOutline().getAlpha()
				except Exception, e:
					JOptionPane.showMessageDialog(None, legend.getClassName() + " not yet implemented!", 
								      "Border Symbology", JOptionPane.WARNING_MESSAGE)
					close(e)
	print sym
	return color_alpha_width

def action(e):
	global color, alpha, width
	color = colorTF.getBackground()
	alpha = slider.getValue() * 255 / 100
	width = float(widthTF.getText())
	changeColorGUI(color)
	
	activeLayers=getActiveLayers()
	for i in range(len(activeLayers)):
		lyr=activeLayers[i]
		if lyr.getClass().getCanonicalName() == "com.iver.cit.gvsig.fmap.layers.FLyrVect":
			legend=lyr.getLegend()			
			if legend.getClassName() == 'com.iver.cit.gvsig.fmap.rendering.SingleSymbolLegend':
				sym = legend.getDefaultSymbol()
				if lyr.getShapeType() == 1:   # points
					#color = sym.getColor()
					newColor = Color(color.getRed(), color.getGreen(), color.getBlue(), alpha)
					sym.setColor(newColor)					
				elif lyr.getShapeType() == 2:  # lines
					#sym.setAlpha(alpha)
					sym = setBorder(sym, color, width, alpha)
				else:
					sym = setBorder(sym, color, width, alpha)
				legend.setDefaultSymbol(sym)
			else:
				try:
					syms=legend.getSymbols()
					for j in range(len(syms)):
						sym=syms[j]
						if lyr.getShapeType() == 1:   # points
							#color = sym.getColor()
							newColor = Color(color.getRed(), color.getGreen(), color.getBlue(), alpha)
							sym.setColor(newColor)
						elif lyr.getShapeType() == 2:  # lines
							#sym.setAlpha(alpha)
							sym = setBorder(sym, color, width, alpha)
						else:
							sym = setBorder(sym, color, width, alpha)
						legend.setDefaultSymbol(sym)
				except Exception, e:
					JOptionPane.showMessageDialog(None, legend.getClassName() + " not yet implemented!", 
						"Border Symbology", JOptionPane.WARNING_MESSAGE)
					close(e)
	return

def accept(e):
	action(e)
	frame.dispose()
	return

def close(e):
	frame.dispose()
	return

def changeColorGUI(ncolor):
	global color, alpha, colorTF
	alpha = slider.getValue() * 255 / 100

	color = Color(ncolor.getRed(), ncolor.getGreen(), ncolor.getBlue(), alpha)
	colorTF.setText("")
	colorTF.setText(color.toString())
	# To avoid transparency to the before color on the textField 
	colorTF.setBackground(Color(255,255,255,255))
	colorTF.setBackground(color)
	print color
	print alpha
	print colorTF.getBackground()

def colorChooser(e):
	global color
	colorChooser = JColorChooser()
	color = colorChooser.showDialog(None, "Border Color", color)
	changeColorGUI(color)
	return

def getGUI(sym_dict):
	global frame, outCheckbox, fillCheckbox, slider, colorTF, widthTF
	frame = JFrame("Border Symbology", defaultCloseOperation=JFrame.DISPOSE_ON_CLOSE, 
		       bounds=(100, 100, 450, 200), layout=FlowLayout(), resizable=0)

	colorL = JLabel('Color: ')
	colorTF = JTextField(20)
	color = sym_dict["color"]
	color = Color(color.getRed(), color.getGreen(), color.getBlue(), sym_dict["alpha"])
	colorTF.setBackground(color)
	colorTF.setText(color.toString())

	colorB = JButton('...', actionPerformed=colorChooser)
	frame.add(colorL)
	frame.add(colorTF)
	frame.add(colorB)

	widthL = JLabel('Width: ')
	widthTF = JTextField(3)
	widthTF.setText(str(sym_dict["width"]))
	frame.add(widthL)
	frame.add(widthTF)

	alphaL = JLabel('Transparency: ')
	frame.add(alphaL)

	# Create a horizontal slider with min=0, max=100, value=50
	slider = JSlider()
	slider.setPreferredSize(Dimension(200, 50))
	slider.setValue(sym_dict["alpha"]*100/255)
	slider.setMajorTickSpacing(25)
	slider.setMinorTickSpacing(5)
	slider.setPaintTicks(1)
	slider.setPaintLabels(1)

	applyButton = JButton("Apply", actionPerformed=action)
	acceptButton = JButton("Accept", actionPerformed=accept)

	frame.add(slider)
	frame.add(applyButton)
	frame.add(acceptButton)

	frame.show()
    
def main():
	
	activeLayers=getActiveLayers()

	if len(activeLayers)==0:
		JOptionPane.showMessageDialog(None, 
			"Add and activate at least one vector layer in the view. Retry!",
			"Border Symbology", JOptionPane.WARNING_MESSAGE)
		return
	else:
		numFLyrVect=0
		for i in range(len(activeLayers)):
			if activeLayers[i].getClass().getCanonicalName()=="com.iver.cit.gvsig.fmap.layers.FLyrVect":
				numFLyrVect=numFLyrVect+1
		if numFLyrVect==0:
			JOptionPane.showMessageDialog(None, 
				"You have to add and activate at least one vector layer in the view. Retry!", 
				"Border Symbology", JOptionPane.WARNING_MESSAGE)
			return
		else:
			color_alpha_width = getFirstSymbol()
			getGUI(color_alpha_width)

			return

main()

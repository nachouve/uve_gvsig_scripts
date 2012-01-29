#!/usr/bin/env jython
#################################################################################
#
# Project:  gvSIG Jython script samples
# Name:     batchLegend.py
# Purpose:  Apply the same .gvl legend file to a set of vectorial layers.
# Author:   Antonio Falciano, afalciano@yahoo.it
#
#################################################################################
# Copyright (c) 2009-2010, Antonio Falciano <afalciano@yahoo.it>
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

from java.io import InputStreamReader, FileInputStream, File
from javax.swing import JOptionPane

from gvsiglib import *
from com.iver.utiles.xmlEntity.generate import XmlTag
from com.iver.utiles import XMLEntity
from com.iver.andami import PluginServices

def openGVL():
    from javax.swing import JFileChooser
    GUIUtil=PluginServices.getPluginServices("com.iver.cit.gvsig.cad").getClassLoader().loadClass("com.iver.cit.gvsig.gui.GUIUtil")
    chooser = JFileChooser()
    chooser.setFileFilter(GUIUtil().createFileFilter("GVL Legend File",["gvl"]))
    from java.util.prefs import Preferences
    lastPath = Preferences.userRoot().node("gvsig.foldering").get("DataFolder", "null")
    chooser.setCurrentDirectory(File(lastPath))
    chooser.setFileSelectionMode(JFileChooser.FILES_ONLY)
    returnVal = chooser.showOpenDialog(None)
    if returnVal == chooser.APPROVE_OPTION:
        gvlPath = chooser.getSelectedFile().getPath()
    elif returnVal == chooser.CANCEL_OPTION:
        JOptionPane.showMessageDialog(None, "You have to open a .gvl file. Retry!","Batch Legend",JOptionPane.WARNING_MESSAGE)
        gvlPath = ""
    return gvlPath

def loadLegendFromFile(pathToFile):
	# see on http://runas.cap.gva.es/pipermail/gvsig_internacional/2007-March/000324.html
	LegendFactory=gvSIG.classForName("com.iver.cit.gvsig.fmap.rendering.LegendFactory")
	myReader=InputStreamReader(FileInputStream(File(pathToFile)),"UTF-8")
	myXML=XMLEntity(XmlTag.unmarshal(myReader))
	return LegendFactory.createFromXML(myXML) 

def main():
	view=gvSIG.getActiveDocument()
	mctrl=view.getMapControl()
	mctxt=mctrl.getMapContext()
	layers=mctxt.getLayers()

	if len(layers.getActives())==0:
		JOptionPane.showMessageDialog(None, "Add and activate at least one vector layer in the view. Retry!","Batch Legend",JOptionPane.WARNING_MESSAGE)
		return
	else:
		path=openGVL()
		if path<>"":
			legend=loadLegendFromFile(path)
		else:
			return
		numFLyrVect=0
		numSetLegend=0
		for i in range(layers.getLayersCount()):
			if layers.getLayer(i).isActive() and layers.getLayer(i).getClass().getCanonicalName()=="com.iver.cit.gvsig.fmap.layers.FLyrVect":
				numFLyrVect=numFLyrVect+1
				# if layers.getLayer(i).getShapeType()==legend.getSymbols()[0].getSymbolType() and layers.getLayer(i).getRecordset().getFieldNames().count(legend.getFieldName())==1:
				if layers.getLayer(i).getShapeType()==legend.getShapeType():
					numSetLegend=numSetLegend+1
					layers.getLayer(i).setLegend(legend)
		if numFLyrVect==0:
			JOptionPane.showMessageDialog(None, "You have to add and activate at least one vector layer in the view. Retry!","Batch Legend",JOptionPane.WARNING_MESSAGE)
			return
		elif numSetLegend==0:
			JOptionPane.showMessageDialog(None, "Active layers doesn't match with this legend! Retry!","Batch Legend",JOptionPane.WARNING_MESSAGE)
			return
	mctrl.invalidate()
	return
	
main()



#!/usr/bin/env jython
#################################################################################
#
# Project:  gvSIG Jython script samples
# Name:     csv2sql.py
# Purpose:  Convert CSV files (';' as separator) to SQL sentence to import to PostgreSQL
# Author:   Nacho Varela, nachouve@gmail.com
# Date: 2012 Febrary
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
from java.awt.event import *
from javax.swing import *
from javax.swing.event import *
from javax.swing.filechooser import FileNameExtensionFilter
from java.awt import FlowLayout, Dimension, Color

import os

def createInsert(tablename, types, k, v):
    stmt = 'INSERT INTO '+ tablename+' ('
    for col in k:
        stmt = stmt +'"'+ col +'", '
        stmt = stmt[:-2]+ ") VALUES ("
        i = 0
        for col in k:
            if (types[col] == 'text'):
                stmt = stmt +"'"+ v[i] +"', "
else: 
    number = v[i]
    number = number.replace('.','')
    number = number.replace(',','.')
    ## Remove all not numeric elements
    aux = ''
    for c in str(number):
        try:
            aux = aux+str(int(c))
        except ValueError:
            if (c in ('-','.')):
                aux = aux + c
    number = aux
    stmt = stmt + number +", "
i = i + 1
stmt = stmt[:-2]+ ");\n"
print stmt
return stmt

def createTable(tablename, cols, types):
    stmt = "CREATE TABLE "+tablename+" ("
    for col in cols:
        stmt = stmt +'"'+ col +'" '+types[col]+", "
        stmt = stmt[:-2] + "); \n"
        print stmt
        return stmt

def action(e):
    global jlist, col_types, selectedfile, outputfile, tablename
    
    sqlfile = open(outputfile, 'w')

    cols = []
    model = jlist.getModel()
    for i in range(model.getSize()):
        cols.append(model.getElementAt(i))
i = i + 1

stmt = createTable(tablename, cols, col_types)
sqlfile.write(stmt)

csvfile = open(selectedfile,'r')
header = csvfile.readline()
for line in csvfile.readlines():
    line = str(line).strip()
line = line.replace("\n", '')

values = []
vals = line.split(';')
for v in vals:
    v = cleanColumnName(v)
    values.append(v)

if (len(values) != len(cols)):
    print 'ERROR: Wrong number of values!!!'
    #return
try:
    stmt = createInsert(tablename, col_types, cols, values)
    sqlfile.write(stmt)
except Exception, e:
    print e

    sqlfile.close()
    return

def accept(e):
    action(e)
    frame.dispose()
    return

def close(e):
    frame.dispose()
    return

def csvChooser(e):
    global selectedfile
    
    selectedfile = ''
    chooser = JFileChooser()
    #filter = FileNameExtensionFilter("CSV files", "csv")
    #chooser.setFileFilter(filter)
    returnVal = chooser.showOpenDialog(None)
    if(returnVal == chooser.APPROVE_OPTION): 
        selectedfile = str(chooser.getSelectedFile())
try:
    print selectedfile
    addColumns()
except Exception, e:
    print 'Error!!!'
    print e
    return selectedfile

def cleanColumnName(col):
    col = str(col).strip()
    col = col.replace('"', '')
    col = col.replace("\n", '')
    col = str(col).strip()
    return col

def addColumns():
    global col_types, selectedfile, jlist, outputfile, tablename, csvTF, tbTF
    
    csvTF.setText(selectedfile)
    tablename = cleanTableName(selectedfile)
    tbTF.setText(tablename)
    outputfile = toSQL(selectedfile)

    f = ''
    if (len(selectedfile.strip())>0):
        f = selectedfile.strip()
        if (not os.path.isfile(f)):
            # TODO AVISO!!!!
            return False
        csvfile = open(f,'r')
        header = csvfile.readline()
        cols = header.split(';')
        count = 0
        for col in cols:
            col = cleanColumnName(col)
print "["+str(col)+"]"
if (len(col)>0):
    cols[count] = col
    count = count + 1
    col_types[col] = 'text'
    jlist.setListData(cols)

def changeGUI(event):
    global jlist
    
    enabled = 1
    if (jlist.isSelectionEmpty()):
        enabled = 0
        intRB.setEnabled(enabled)
        doubleRB.setEnabled(enabled)
        stringRB.setEnabled(enabled)
        
        selectedValue = jlist.getSelectedValue()
        if (selectedValue != None):
            type = col_types[selectedValue]
if (type == 'int'):
    intRB.setSelected(1)
elif (type == 'double precision'):
    doubleRB.setSelected(1)
else:
    stringRB.setSelected(1)

def getRBSelected():
    if (intRB.isSelected()):
        return 'int'
    elif (doubleRB.isSelected()):
        return 'double precision'
    else:
        return 'text'

class MyAction(ListSelectionListener):
    def valueChanged(self,e):
        changeGUI(e)

class MyRBListener(ActionListener):
    def actionPerformed(self,e):
        #print 'Clicked ' +  getRBSelected()
        col_types[jlist.getSelectedValue()] = getRBSelected()

class MyTFListener(ActionListener):
    def actionPerformed(self,e):
        global selectedfile
selectedfile = csvTF.getText()
addColumns()

def cleanTableName(name):
    name = name[name.rfind('/')+1:]
    name = name[name.rfind('\\')+1:]
    name = name[:name.find('.')]
    return name

def toSQL(name):
    return name[:-3]+'sql'

def getGUI():
    global frame, col_types, jlist, intRB, doubleRB, stringRB, outputfile, selectedfile, tablename, csvTF, tbTF
    
    selectedfile = 'C:/Temp/lonja2s.csv'
    outputfile = toSQL(selectedfile)
    col_types = {}
    
    frame = JFrame("CSV 2 SQL", defaultCloseOperation=JFrame.DISPOSE_ON_CLOSE, 
                          bounds=(100, 100, 450, 400), layout=FlowLayout(), resizable=1)

    csvL = JLabel('CSV: ')
    csvTF = JTextField(20)
    csvTF.setText(selectedfile)
    csvTF.addActionListener(MyTFListener())
    csvB = JButton('...', actionPerformed=csvChooser)
    frame.add(csvL)
    frame.add(csvTF)
    frame.add(csvB)
    
    tbL = JLabel('TableName: ')
    tbTF = JTextField(10)
    tablename = cleanTableName(selectedfile)
    tbTF.setText(tablename)
    frame.add(tbL)
    frame.add(tbTF)
    
    jlist = JList(['           ','                                                         ']);
    jlist.setVisibleRowCount(10)
    #Font displayFont = new Font("Serif", Font.BOLD, 18);
    #jlist.setFont(displayFont);
    #jlist.addListSelectionListener(new ValueReporter());
    listPane = JScrollPane(jlist)
    
    #myListener.valueChange = changeGUI
    jlist.addListSelectionListener(MyAction())
    frame.add(listPane)
    
    typePanel = JPanel(FlowLayout());
    intRB = JRadioButton("Entero")
    intRB.addActionListener(MyRBListener())
    doubleRB = JRadioButton("Decimal")
    doubleRB.addActionListener(MyRBListener())
    stringRB = JRadioButton("Texto")
    stringRB.addActionListener(MyRBListener())
    
    typeGroup = ButtonGroup()
    typeGroup.add(intRB)
    typeGroup.add(doubleRB)
    typeGroup.add(stringRB)
    
    stringRB.setSelected(1)
    
    typePanel.add(intRB)
    typePanel.add(doubleRB)
    typePanel.add(stringRB)
    
    frame.add(typePanel)

    if (len(selectedfile)>0 and os.path.isfile(selectedfile)):
        addColumns()
        
        applyButton = JButton("Apply", actionPerformed=action)
        acceptButton = JButton("Accept", actionPerformed=accept)

        #frame.add(slider)
        frame.add(applyButton)
        frame.add(acceptButton)

        changeGUI(None)
        frame.show()
    
def main():
    
    getGUI()
    return

main()


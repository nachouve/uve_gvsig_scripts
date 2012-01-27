#/bin/python

# -*- coding: utf-8 -*-

import sys, commands, codecs
from xml.dom.minidom import parse, parseString

def getExtension(project, extension, o_list):
    for ext in extension:
        r = dict()
        r["project"] = project
        r["class-name"] = ext.getAttribute("class-name")
        r["type"] = "extension"
        r["active"] = ext.getAttribute("active")
        r["description"] = ext.getAttribute("description")
        r["priority"] = ext.getAttribute("priority")
        o_list.append(r)
    return o_list

def getMenu(project, extension, o_list):
    for ext in extension:
        menu = ext.getElementsByTagName("menu")
        for m in menu:
            r = dict()
            r["project"] = project
            r["class-name"] = ext.getAttribute("class-name")
            r["type"] = "menu"
            r["separator"] = m.getAttribute("is_separator")
            r["action-command"] = m.getAttribute("action-command")
            r["text"] = m.getAttribute("text")
            r["tooltip"] = m.getAttribute("tooltip")
            r["icon"] = m.getAttribute("icon")
            r["key"] = m.getAttribute("key")
            r["position"] = m.getAttribute("position")
            o_list.append(r)
    return o_list

def getToolbar(project, extension, o_list):
    for ext in extension:
        toolbar = ext.getElementsByTagName("tool-bar")
        for m in toolbar:
            r = dict()
            r["project"] = project
            r["class-name"] = ext.getAttribute("class-name")
            r["type"] = "toolbar"
            r["name"] = m.getAttribute("name")
            r["position"] = m.getAttribute("position")
            o_list.append(r)
    return o_list


def getActionTool(project, extension, o_list):
    for ext in extension:
        toolbar = ext.getElementsByTagName("tool-bar")
        for i in range(toolbar.length):
            t = toolbar.item(i)
            act = t.getElementsByTagName("action-tool")
            for m in act:
                r = dict()
                r["project"] = project
                r["toolbar"] = t.getAttribute("name")
                print t.getAttribute("name")
                r["class-name"] = ext.getAttribute("class-name")
                r["type"] = "action-tool"
                r["action-command"] = m.getAttribute("action-command")
                #r["text"] = m.getAttribute("text")
                r["tooltip"] = m.getAttribute("tooltip")
                r["icon"] = m.getAttribute("icon")
                r["position"] = m.getAttribute("position")
                o_list.append(r)
            act = t.getElementsByTagName("selectable-tool")
            for m in act:
                r = dict()
                r["project"] = project
                r["toolbar"] = t.getAttribute("name")
                print t.getAttribute("name")
                r["class-name"] = ext.getAttribute("class-name")
                r["type"] = "selectable-tool"
                r["action-command"] = m.getAttribute("action-command")
                #r["text"] = m.getAttribute("text")
                r["tooltip"] = m.getAttribute("tooltip")
                r["icon"] = m.getAttribute("icon")
                r["position"] = m.getAttribute("position")
                o_list.append(r)
    return o_list

def createCSV(path, o_list):

    output = codecs.open(path, 'w', 'ISO-8859-15')
    obj = o_list[0]
    keys = sorted(obj.keys())
    line = keys[0]
    for k in keys[1:]:
        line = line + ";" + k
    output.write(line + '\n')
    print "createCSV: " + str(len(o_list))

    for r in o_list:
        line = r[keys[0]]
        try:
            for k in keys[1:]:
                line = line + ";" + r[k]
                #print line
            output.write(line + '\n')
        except UnicodeEncodeError as e:
            print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>< UnicodeError at: ' + str(f) 
            print e.args 
            print e.message

## EXEC AT THE ROOT OF GVSIG PROJECT EXTENSIONS

a = commands.getstatusoutput('find | grep config.xml$')
aList = a[1].split('\n')

menus = list()
toolbars = list()
actions = list()
extensions = list()

for f in aList:
    print f
    try: 
        dom = parse(f)
        extension = dom.getElementsByTagName("extension")
        menus = getMenu(f, extension, menus)
        actions = getActionTool(f, extension, actions)
        toolbars = getToolbar(f, extension, toolbars)
        extensions = getExtension(f, extension, extensions)
    except Exception as e:
        print '>>>>>>>>> Error in the config: ' + str(f) + "  error: " + str(e)
        print e.args 
        print e.message

createCSV('/tmp/menus.csv', menus)
createCSV('/tmp/toolbars.csv', toolbars)
createCSV('/tmp/actions.csv', actions)
createCSV('/tmp/extensions.csv', extensions)

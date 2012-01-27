#/bin/python

import os, sys, shutil, commands
from xml.dom.minidom import parse, parseString

#GVSIGPATH = '/home/nachouve/gvSIG_1.11/bin/gvSIG/extensiones/'
GVSIGPATH = os.getcwd() + '/'

input = open('/tmp/actions.csv', 'r')

header = input.readline()
headers = header.split(';')

col_name = dict()
i = 0
for h in headers:
    if (h.endswith('\n')):
        h = h.replace('\n', '')
    col_name[h]=i
    i = i + 1

print str(col_name)

row_num = 0
for l in input:
    r = dict()
    cols = l.split(';')
    
    config_path = cols[col_name["project"]]
    config_path = GVSIGPATH + config_path[2:]

    ## Make a backup
    backup_path = config_path+'_BACK'
    if (not os.path.exists(backup_path)):
        shutil.copy2(config_path, backup_path)

    try:
        dom = parse(config_path)
    except Exception as e:
        print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ERROR parsing: ' + str(config_path) 
        print e.message
        continue

    print 'Parsing ' + str(config_path)
    extension = dom.getElementsByTagName("extension")
    for ext in extension:
        if (ext.getAttribute("class-name") != cols[col_name["class-name"]]):
            continue
        toolbar = ext.getElementsByTagName("tool-bar")
        
        for tb in toolbar:
            if (cols[col_name["type"]] == 'action-tool\n'):
                item = ext.getElementsByTagName("action-tool")
            elif (cols[col_name["type"]] == 'selectable-tool\n'):
                item = ext.getElementsByTagName("selectable-tool")
            for it in item:            
                if (it.getAttribute("action-command") != cols[col_name["action-command"]]):
                    continue
                if (it.getAttribute("icon") != cols[col_name["icon"]]):
                    continue
                position = cols[col_name["position"]]
                it.setAttribute('position', position)
                ## Name of the toolbar
                toolbar = cols[col_name["toolbar"]]
                tb.setAttribute('name', toolbar)
                ## Copy first 5 numbers of the position... Works?
                position_tb = position[:5]
                tb.setAttribute('position', position_tb)

        row_num = row_num + 1

    try:
        ## Test dom.toxml() before write
        dom.toxml(encoding="ISO-8859-1")
        ##
        output = open(config_path, 'wb')
        output.write(dom.toxml(encoding="ISO-8859-1"))
        output.close()
    except UnicodeEncodeError as e:
            print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>< UnicodeError at: ' + str(config_path) 
            print e.message + "  -> \n" + str(e.args)

input.close()

# ################################################
# ## Toolbar
# ################################################

# input = open('/tmp/toolbars.csv', 'r')

# header = input.readline()
# headers = header.split(';')

# col_name = dict()
# i = 0
# for h in headers:
#     if (h.endswith('\n')):
#         h = h.replace('\n', '')
#     col_name[h]=i
#     i = i + 1

# print str(col_name)

# row_num = 0
# for l in input:
#     r = dict()
#     cols = l.split(';')
    
#     config_path = cols[col_name["project"]]
#     config_path = GVSIGPATH + config_path[2:]

#     ## Make a backup
#     backup_path = config_path+'_BACK'
#     if (not os.path.exists(backup_path)):
#         shutil.copy2(config_path, backup_path)

#     try:
#         dom = parse(config_path)
#     except Exception as e:
#         print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ERROR parsing: ' + str(config_path) 
#         print e.message
#         continue

#     print 'Parsing ' + str(config_path)
#     extension = dom.getElementsByTagName("extension")
#     for ext in extension:
#         if (ext.getAttribute("class-name") != cols[col_name["class-name"]]):
#             continue
#         toolbar = ext.getElementsByTagName("tool-bar")
        
#         for tb in toolbar:            
#             position = cols[col_name["position"]]
#             if (len(position.strip())>0):
#                 tb.setAttribute('position', position)
#             ## Name of the toolbar
#             toolbar = cols[col_name["toolbar"]]
#             tb.setAttribute('name', toolbar)

#         row_num = row_num + 1

#     try:
#         ## Test dom.toxml() before write
#         dom.toxml(encoding="ISO-8859-1")
#         ##
#         output = open(config_path, 'wb')
#         output.write(dom.toxml(encoding="ISO-8859-1"))
#         output.close()
#     except UnicodeEncodeError as e:
#             print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>< UnicodeError at: ' + str(config_path) 
#             print e.message + "  -> \n" + str(e.args)

# input.close()

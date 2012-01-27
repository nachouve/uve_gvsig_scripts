#/bin/python

import os, sys, shutil, commands
from xml.dom.minidom import parse, parseString

#GVSIGPATH = '/home/nachouve/gvSIG_1.11/bin/gvSIG/extensiones/'
print os.getcwd()
GVSIGPATH = os.getcwd() + '/'

input = open('/tmp/menus.csv', 'r')

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
print str(col_name["project"])

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
        menu = ext.getElementsByTagName("menu")
        
        for it in menu:
#            for it in item:
            if (it.getAttribute("action-command") != cols[col_name["action-command"]]):
                continue
            if (it.getAttribute("icon") != cols[col_name["icon"]]):
                continue

            ## TEST: this try to check if is_separator
            is_separator = (cols[col_name["is_separator"]].lower().strip()=="true")
            item_separator = it.hasAttribute("is_separator")
            if (is_separator != item_separator):
                continue

            position = cols[col_name["position"]]            
            it.setAttribute('position', position)

            text = cols[col_name["text"]]
            if (len(text)>1):
                it.setAttribute('text', text)
            elif it.hasAttribute('text'):
                it.removeAttribute('text')

            tooltip = cols[col_name["tooltip"]]
            if (len(tooltip)>1):
                it.setAttribute('tooltip', tooltip)
            elif it.hasAttribute('tooltip'):
                it.removeAttribute('tooltip')

            key = cols[col_name["key"]]
            if (len(key)>0):
                it.setAttribute('key', key)
            elif it.hasAttribute('key'):
                it.removeAttribute('key')


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


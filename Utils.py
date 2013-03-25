import os


def kindOfField(field):
    kindOfField = ""
    if field == "integer":
        kindOfField = "integer"
    elif field == "string":
        kindOfField = "char"
    elif field == "boolean":
        kindOfField = "boolean"
    elif field == "one2many":
        kindOfField = "one2many"
    elif field == "many2one":
        kindOfField = "many2one"
    elif field == "float":
        kindOfField = "float"
    else:
        kindOfField = "char"
    return kindOfField

def createInitFile(moduleName):
    moduleFileName = moduleName + '/__init__.py'
    moduleInitFile = open(moduleFileName, 'w')
    moduleInitFile.write('import %s\n' % (moduleName))
    moduleInitFile.close()

def createOpenErpFile(moduleName, classes, dependences):
    moduleFileName = moduleName + '/__openerp__.py'
    moduleInitFile = open(moduleFileName, 'w')
    moduleInitFile.write("{\n")
    moduleInitFile.write('    "name" : "%s",\n' % (moduleName))
    moduleInitFile.write('    "version" : "%s",\n' % ("1.0"))
    moduleInitFile.write('    "author" : "%s",\n' % ("xx"))
    moduleInitFile.write('    "category" : "%s",\n' % ("xx"))
    moduleInitFile.write('    "description" : "%s",\n' % ("xx"))
    moduleInitFile.write('    "init_xml" : %s,\n' % ("[]"))
    moduleInitFile.write('    "depends" : %s,' % ("['base'"))
    for key in dependences:
        moduleInitFile.write("'%s'," % (key))
    moduleInitFile.write('],\n')
    moduleInitFile.write('    "update_xml" : %s' % ("["))
    for key in classes:
        moduleInitFile.write("'%s'," % (moduleName + "_" + key + '_view.xml' ))
    moduleInitFile.write('],\n')
    moduleInitFile.write('    "active" : %s,\n' % ("False"))
    moduleInitFile.write('    "installable" : %s,\n' % ("True"))
    moduleInitFile.write("}")
    moduleInitFile.close()

def createModuleFile(moduleName):
    moduleFileName = moduleName + '/' + moduleName + '.py'
    moduleFile = open(moduleFileName, 'w')
    moduleFile.write("from osv import fields, osv\n")
    moduleFile.write("\n")
    moduleFile.write("\n")
    moduleFile.close()

def createSkeleton(moduleName, classes, dependences):
    if not os.path.isdir(moduleName):
        os.mkdir(moduleName)
        createModuleFile(moduleName)
        createInitFile(moduleName)
        createOpenErpFile(moduleName, classes, dependences)

def createClass(moduleName, className, atributes):
    moduleFileName = moduleName + '/' + moduleName + '.py'
    moduleFile = open(moduleFileName, 'a')
    moduleFile.write('class %s(osv.osv):\n' % (moduleName + "_" + className))
    moduleFile.write('    _name = "%s"\n' % (moduleName + "." + className))
    moduleFile.write('    _description = "%s"\n' % (moduleName + " " + className))
    moduleFile.write('    _columns = { \n')
    for key in atributes.keys():
        field = kindOfField(atributes[key]['field'])
        if field == "one2many":
            modClass = atributes[key]['module'] + "." + atributes[key]['class']
            keyField = atributes[key]['keyField']
            label = atributes[key]['label']
            moduleFile.write("        '%s' : fields.%s('%s','%s','%s'),\n" % (key, field, modClass, keyField, label ))
        elif field == "many2one":
            modClass = atributes[key]['module'] + "." + atributes[key]['class']
            label = atributes[key]['label']
            moduleFile.write("        '%s' : fields.%s('%s','%s', select=True, ondelete='cascade'),\n" % (key, field, modClass, label))
        elif field == "char":
            moduleFile.write("        '%s' : fields.%s('%s',size=255, translate = True , required = False , readonly = True),\n" % (key, field, key))
        elif field == "float":
            moduleFile.write("        '%s' : fields.%s('%s',digits=(12,4) ,required = False , readonly = True),\n" % (key, field, key))
        elif field == "integer":
            moduleFile.write("        '%s' : fields.%s('%s',required = False , readonly = True),\n" % (key, field, key))
        elif field == "boolean":
            moduleFile.write("        '%s' : fields.%s('%s'),\n" % (key, field, key))
        else:
            moduleFile.write("        '%s' : fields.%s('%s',required = False , readonly = True),\n" % (key, field, key))

    moduleFile.write('    }\n')
    moduleFile.write('    _defaults = { \n')
    moduleFile.write('    }\n')
    moduleFile.write('    _auto = True \n')
    moduleFile.write('    _log_access = True \n')
    moduleFile.write('    __rec_name = _name \n')
    moduleFile.write('    _constraints = [] \n')
    moduleFile.write('    _sql_constraints = [] \n')
    moduleFile.write('    _order = "name" \n')
    moduleFile.write("    #_inherit = '' \n")
    moduleFile.write('    #_inherits = {\n')
    moduleFile.write('    #}\n')
    moduleFile.write('    #_table = "%s"\n' % (moduleName + "_" + className))
    moduleFile.write('%s()\n' % (moduleName + "_" + className))
    moduleFile.write("\n")
    moduleFile.close()

def createView(moduleName, className):
    moduleViewName = moduleName + '/' + moduleName + "_" + className + '_view.xml'
    moduleFile = open(moduleViewName, 'w')
    moduleFile.write('<?xml version="1.0"?>\n')
    moduleFile.write("<openerp>\n")
    moduleFile.write("<data>\n")
    moduleFile.close()

def closeView(moduleName, className):
    moduleViewName = moduleName + '/' + moduleName + "_" + className + '_view.xml'
    moduleFile = open(moduleViewName, 'a')
    moduleFile.write("</data>\n")
    moduleFile.write("</openerp>\n")
    moduleFile.close()

def createClassView(moduleName, className, atributes):
    moduleViewName = moduleName + '/' + moduleName + "_" + className + '_view.xml'
    moduleFile = open(moduleViewName, 'a')
    moduleFile.write('    <record model="ir.ui.view" id="%s">\n' % (moduleName + "_" + className +"_form"))
    moduleFile.write('        <field name="name">%s</field>\n' % (moduleName + "." + className +".form"))
    moduleFile.write('            <field name="model"> %s </field>\n' % (moduleName + "." + className ))
    moduleFile.write('            <field name="type">form</field>\n')
    moduleFile.write('            <field name="arch" type="xml">\n')
    moduleFile.write('                <form string="%s">\n' % (moduleName + " " + className))
    for key in atributes.keys():
        moduleFile.write('                    <field name="%s"/>\n' % (key))
    moduleFile.write('                </form>\n')
    moduleFile.write('           </field>\n')
    moduleFile.write('    </record>\n')

    moduleFile.write('    <record model="ir.ui.view" id="%s">\n' %(moduleName + "_" + className +"_tree"))
    moduleFile.write('        <field name="name">%s</field>\n' % (moduleName + "." + className +".tree"))
    moduleFile.write('        <field name="model"> %s </field>\n' % (moduleName + "." + className ))
    moduleFile.write('        <field name="type">tree</field>\n')
    moduleFile.write('        <field name="arch" type="xml">\n')
    moduleFile.write('            <tree string="%s">\n' % (moduleName + " " + className))
    for key in atributes.keys():
        moduleFile.write('                <field name="%s"/>\n' % (key))
    moduleFile.write('            </tree>\n')
    moduleFile.write('        </field>\n')
    moduleFile.write('        </record>\n')

    moduleFile.write('<record model="ir.actions.act_window" id="action_%s_seq">\n ' % (className))
    moduleFile.write('<field name="name">%s</field>\n' % (moduleName + " " + className))
    moduleFile.write(' <field name="res_model">%s</field> \n' % (moduleName + "." + className ))
    moduleFile.write('<field name="view_type">form</field>\n')
    moduleFile.write('<field name="view_mode">tree,form</field>\n')
    moduleFile.write('</record>\n')

    moduleFile.write('<menuitem id="menu_%s_main" name="%s"/>\n' % (moduleName + "_" + className,moduleName + " " + className))
    moduleFile.write('<menuitem id="menu_%s" parent="menu_%s_main" name="%s" action="action_%s_seq"/>\n' % (moduleName + "_" + className,moduleName + "_" + className,moduleName + " " + className,className))
    moduleFile.close()
    closeView(moduleName, className)

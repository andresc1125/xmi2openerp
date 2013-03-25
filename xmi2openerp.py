import xml.etree.ElementTree as xml
import Utils as erp
import string as stru
import sys

tree = xml.parse(sys.argv[1])

rootElement = tree.getroot()

modelioMap = {}
classMap = {}

#map all modules and modules' classes

for modules in rootElement.findall('packagedElement'):
    moduleName = modules.get('name').lower()
    modelioMap.update({moduleName: {'classes': {}, 'dependences': {}}})
    #erp.createSkeleton(moduleName)
    moduleclases = modules.findall('packagedElement')
    for moduleclase in moduleclases:
        if moduleclase.get('memberEnd') is None:
            className = moduleclase.get('name').lower()
            modelioMap[moduleName]['classes'].update({className: {}})
            classMap.update({className: {}})
            classMap[className].update({'module': moduleName})
            classMap[className].update({'attributes': {}})

#map classes' attributes

for modules in rootElement.findall('packagedElement'):
    moduleName = modules.get('name').lower()
    moduleclases = modules.findall('packagedElement')
    for moduleclase in moduleclases:
        if moduleclase.get('memberEnd') is None:
            className = moduleclase.get('name').lower()
            claseAtributes = moduleclase.findall('ownedAttribute')
            for atribute in claseAtributes:
                if atribute.get('association') is None:
                    typetag = atribute.find('type')
                    typefield = typetag.get('href')
                    items = stru.split(typefield, '#')
                    params = {'field': items[1]}
                    classMap[className]['attributes'].update({atribute.get('name').lower(): params})
                else:
                    nameLocalField = atribute.get('name').lower() + "s"
                    targetClass = atribute.get('name').lower()
                    module = classMap[targetClass]['module']
                    keyField = atribute.get('name') + "_id" #keyField = atribute.get('name') + "_" + className
                    label = atribute.get('name').lower() + "s"
                    localParams = {'field':'one2many','module':module ,'class':targetClass, 'keyField' :keyField, 'label' : label }
                    classMap[className]['attributes'].update({nameLocalField: localParams})

                    localModule = classMap[className]['module']
                    targetParams = {'field':'many2one','module':localModule ,'class':className , 'label': className}
                    classMap[targetClass]['attributes'].update({keyField: targetParams})
                    requiredModule = classMap[targetClass]['module']
                    if not modelioMap[requiredModule]['dependences'].has_key(localModule):
                        if requiredModule is not localModule:
                            modelioMap[requiredModule]['dependences'].update({localModule:{}})

for module in modelioMap.keys():
    erp.createSkeleton(module,modelioMap[module]['classes'].keys(),modelioMap[module]['dependences'].keys())
    for mClass in modelioMap[module]['classes'].keys():
        erp.createClass(classMap[mClass]['module'], mClass, classMap[mClass]['attributes'])
        erp.createView(classMap[mClass]['module'], mClass)
        erp.createClassView(classMap[mClass]['module'], mClass, classMap[mClass]['attributes'])

print "Finished"

#Impot MiniDom to WORK with XML
from xml.dom import minidom

#Template to class
strClassBegin = """unit SAS_Synchro{0};

interface
    {1}

  type TSynchro{0} = class
  private
  public
{2}
"""

#Template to end of the class
strClassEnd = """
  end;



implementation


end."""


#Return first caracter of string in Upper case
def upperFirst(str):
    return str[0].upper() + str[1:]


#Process the type and the name of property
def processProperty(name):
    temp = name
    typeProperty = 'string'
    if(name[1].upper() == name[1]):
        if(name[0] == 'v'):
            temp = 'Vlr' + name[1:]
            typeProperty = 'Extended'
        if(name[0] == 'p'):
            typeProperty = 'Extended'
        elif(name[0] == 'c'):
            temp = 'Cod' + name[1:]
            typeProperty = 'Integer'
        elif(name[0] == 'x'):  # name[0] == 'x'
            if (('DESCR' not in name) and 'TEXTO' not in name):
                temp = 'Descr' + name[1:]
            temp = name[1:];
    if(name.upper() == 'MOD'):
        temp = 'mode';
    return upperFirst(temp), typeProperty

#process type of the class
def processType(name):
    return upperFirst(name)

#Visit a node and the add file and propertys in a class
def visitNode(node, currentFile, dictPropertys):
    result = [];
    #final Node
    if node.height == 2:
        #if not declared type in father
        if (node.tagName not in dictPropertys):
            name, typeProperty = processProperty(node.tagName)
            result.append(
                "    property {0} : {1};\n".format(name, typeProperty))
            dictPropertys[node.tagName] = True
    else:
        #Create new file to Class
        typeName = processType(node.tagName)
        newFile = open("SAS_Synchro{0}.pas".format(typeName), 'w')
        newDic = {}
        strUses = '';
        propertys = [];
        for child in node.childNodes:
            if child.height != 1:
                propertys.extend(visitNode(child, newFile, newDic))
                if child.height > 2:
                    childTypeName = processType(child.tagName)
                    if (childTypeName not in newDic):
                        propertys.append(
                            "    property {0} : TSynchro{0};\n".format(childTypeName))
                        if(strUses == ''):
                            strUses = 'uses SAS_Synchro{0}';
                        else:
                            strUses += ', SAS_Synchro{0}'
                        strUses = strUses.format(
                            childTypeName);
                        newDic[childTypeName] = True
        if(strUses != ''):
            strUses += ';';
        newFile.write(strClassBegin.format(typeName, strUses, ''.join(propertys)));

        newFile.write(strClassEnd)
    return result;

#Calc Height of nodes in XML document
def calcHeight(node):
    if node.nodeType == node.TEXT_NODE:
        node.height = 1
        return node.height
    maxV = 0
    for child in node.childNodes:
        v = calcHeight(child)
        if(v > maxV):
            maxV = v
    node.height = maxV + 1
    return node.height

#Get root element
root = minidom.parse('Exemplo_CTEOS_SynchroRS.xml').documentElement
#Calc height of all nodes
calcHeight(root)

#Visit Nodes and create files
visitNode(root, '', None)

#Finish the process
print('Success')

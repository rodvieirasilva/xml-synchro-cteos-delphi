
from xml.dom import minidom


strClassBegin = """unit uSynchro{0};

interface
    {1}

  type TSynchro{0} = class
  private
  public
{2}
"""

strClassEnd = """
  end;



implementation


end."""


def upperFirst(str):
    return str[0].upper() + str[1:]


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

    return upperFirst(temp), typeProperty


def processType(name):
    return upperFirst(name)


def visitNode(node, currentFile, dictPropertys):
    result = [];
    if node.height == 2:
        if (node.tagName not in dictPropertys):
            name, typeProperty = processProperty(node.tagName)
            result.append(
                "    property {0} : {1};\n".format(name, typeProperty))
            dictPropertys[node.tagName] = True
    else:
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
                            strUses = 'use SAS_Synchro{0}';
                        else:
                            strUses += ', {0}'
                        strUses = strUses.format(
                            childTypeName);
                        newDic[childTypeName] = True
        if(strUses != ''):
            strUses += ';';
        newFile.write(strClassBegin.format(typeName, strUses, ''.join(propertys)));

        newFile.write(strClassEnd)
    return result;


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


root = minidom.parse('Exemplo_CTEOS_SynchroRS.xml').documentElement

calcHeight(root)

visitNode(root, '', None)

print('Sucesso')

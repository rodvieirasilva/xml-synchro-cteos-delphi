
from xml.dom import minidom


strClassBegin = """unit uSynchro{0};

interface
  type TSynchro{0} = class
  private
  public

"""

strClassEnd = """
  end;



implementation

{{ TSynchro{0} }}

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

    if node.height == 2:
        if  (node.tagName not in dictPropertys):
            name, typeProperty = processProperty(node.tagName)
            currentFile.write(
                "    property {0} : {1};\n".format(name, typeProperty))
            dictPropertys[node.tagName] = True
    else:
        typeName = processType(node.tagName)
        newFile = open("SAS_Synchro{0}.pas".format(typeName), 'w')
        newDic = {}
        newFile.write(strClassBegin.format(typeName))
        for child in node.childNodes:
            if child.height != 1:
                visitNode(child, newFile, newDic)
                if child.height > 2:
                    childTypeName = processType(child.tagName)
                    if  (childTypeName not in newDic):
                        newFile.write(
                            "    property {0} : TSynchro{0};\n".format(childTypeName))
                        newDic[childTypeName] = True

        newFile.write(strClassEnd.format(typeName))


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

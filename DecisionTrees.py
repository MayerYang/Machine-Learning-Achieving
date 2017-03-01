from math import log
import operator
import pygraphviz as pgv


def createTestData():
    dataSet = [[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]
    labels = ['no surfacing','flippers']
    return dataSet,labels

def calcShannonEnt(dataSet):    #Shannon Entropy is a measure to the complecity of datas, high entropy means high complecity
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob*log(prob,2)
    return shannonEnt

def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

def chooseBestFeatureToSplit(dataSet):      #the best way is a way by which the complecity is lowest, in other words, the lowest entropy
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(0,numFeatures):
        featList = [example[i] for example in dataSet]  # get cloumn i  
        uniqueVals = set(featList)  #get rid of repetitive features 
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet,i,value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy     
        if (infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

def majorityCnt(classList):     #retrun the item in a list whose count is the lagrest
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet,labels):     #create decision tree
    copyLabels = labels[:]
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):  #overdone!
        return classList[0]
    if len(dataSet[0]) == 1:       #there are still more than kinds in the dataSet but no more features to use
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = copyLabels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(copyLabels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = copyLabels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return myTree

def classify(inputTree, featLabels, testVec):   #use decision tree to determin a testVec's label
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]) == dict:
                classLabel = classify(secondDict[key], featLabels, testVec)
            else:
                classLabel = secondDict[key]
    return classLabel

def storeTree(inTree, filename):    #to store the decision tree in disk
    import pickls
    f = open(filename, 'w')
    pickle.dump(inTree, f)
    f.close()

def grabTree(filename):     #get the dicision tree from a file 
    import pickls
    f = open(filename, 'r')
    retTree = f.load(f)
    f.close()
    return retTree

def drawTree(tree,picName):     #draw the decision tree 
    g = pgv.AGraph(directed=True, strict=True)
    node = [1]
    def drawSubtree(Tree,node):  #inherent node 
        if type(Tree) == dict:
            if len(Tree) == 1:  #one label
                nodeLabel = '%s' % Tree.keys()[0]
                subTree = Tree[Tree.keys()[0]]
                thisNode = node[0]
                g.add_node(thisNode,shape="rect",label=nodeLabel)
                node[0] += 1
                subNodes = drawSubtree(subTree,node)
                for i in range(0,len(subNodes)):
                    g.add_edge(thisNode, subNodes[i], label="%s"%(subTree.keys()[i]))
                return thisNode 
            else:   #diffenent edges
                retNodesList = []
                for edge in Tree:
                    retNodesList.append(drawSubtree(Tree[edge],node))
                return retNodesList
        else:   #leaf
            thisNode = node[0]
            g.add_node(thisNode,shape='circle', label=Tree)
            node[0] += 1
            return thisNode
    drawSubtree(tree,node)
    g.layout('dot')
    g.draw(picName+'.jpg',format="jpg")



        
        
    
    

    
    
            
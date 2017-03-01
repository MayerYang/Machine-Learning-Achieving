from numpy import *
import operator
import matplotlib
import matplotlib.pyplot as plt

def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group,labels
    
def classify0(dataSet, trainSet, trainLabels, k):
    returnLabels = []
    for n in range(0,dataSet.shape[0]):
        diffMat = trainSet-tile(dataSet[n],(trainSet.shape[0],1))  #use inX to make a array in which row num is dataSetSize and column num is 1
        sqDiffMat = diffMat**2    #to calculate each element's square
        sqDistance = sqDiffMat.sum(axis=1)
        distance = sqDistance**0.5
        sortedDistIndicies = distance.argsort()
        classCount = [0,0,0]
        for i in range(k):
            voteIlabel = trainLabels[sortedDistIndicies[i]]
            classCount[voteIlabel-1] += 1
        returnLabels.append(classCount.index(max(classCount))+1)
    return returnLabels

def file2matrix(filename,option=0,inMax=0,inMin=0):
    f = open(filename)
    lines = f.readlines()
    numOfLines = len(lines)
    mat = zeros((numOfLines,3))
    classLabelVector = []
    for i in range(0,numOfLines):
        line = lines[i]
        lineEx = line.strip()
        listFormLine = lineEx.split('\t')
        for j in range(0,3):
            listFormLine[j] = float(listFormLine[j][0:6])
        mat[i,:] = listFormLine[0:3]
        classLabelVector.append(int(listFormLine[-1]))
    if option == 0:
        columnMax = mat.max(0)
        columnMin = mat.min(0)
    else:
        columnMax = inMax
        columnMin = inMin
    returnMat = zeros((numOfLines,3))
    for i in range(0,numOfLines):
        for j in range(0,3):
            returnMat[i,j] = (mat[i,j]-columnMin[j])/(columnMax[j]-columnMin[j])
    f.close()
    if option == 0:
        return returnMat, classLabelVector,columnMax,columnMin
    elif option == 1:
        return returnMat, classLabelVector

def classily0(trainFileName,testFileName):
    trainSet,trainLabels,trainMax,trainMin = file2matrix(trainFileName,0)
    dataSet,dataLabels = file2matrix(testFileName,1,trainMax,trainMin)
    antiLabels = classify0(dataSet,trainSet,trainLabels,100)
    correctCount = 0
    for i in range(0,len(dataLabels)):
        if antiLabels[i] == dataLabels[i]:
            correctCount += 1
    print correctCount
    print "Correct Rate:\t%f\n"%(float(correctCount)/len(dataLabels))
    return trainSet,trainLabels,dataSet,dataLabels
    
def showResult(figure1,figure2,Set,labels):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(Set[:,figure1],Set[:,figure2],15.0*array(labels),15.0*array(labels))
    plt.show()

#use range to draw a circle, counting the labes of every point in the circle, the difficult is to choose range but the time use to sort is saved
def classfy1(dataSet,trainSet,trainLabels,Range):   
    returnLabels = []
    for n in range(0,dataSet.shape[0]):
        diffMat = trainSet-tile(dataSet[n],(trainSet.shape[0],1))  #use inX to make a array in which row num is dataSetSize and column num is 1
        sqDiffMat = diffMat**2    #to calculate each element's square
        sqDistance = sqDiffMat.sum(axis=1)
        distance = sqDistance**0.5
        classCount = [0,0,0]
        for i in range(0,trainSet.shape[0]):
            if distance[i] <= Range:
                    classCount[trainLabels[i]-1] += 1
        returnLabels.append(classCount.index(max(classCount))+1)
    return returnLabels

def classily1(trainFileName,testFileName):
    trainSet,trainLabels,trainMax,trainMin = file2matrix(trainFileName,0)
    dataSet,dataLabels = file2matrix(testFileName,1,trainMax,trainMin)
    antiLabels = classfy1(dataSet,trainSet,trainLabels,0.3)
    correctCount = 0
    for i in range(0,len(dataLabels)):
        if antiLabels[i] == dataLabels[i]:
            correctCount += 1
    print correctCount
    print "Correct Rate:\t%f\n"%(float(correctCount)/len(dataLabels))
    return trainSet,trainLabels,dataSet,dataLabels

def getMidPoint(trainSet,trainLabels):
    midPoint = array([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])
    for i in range(0,trainSet.shape[0]):
        for j in range(0,3):
            midPoint[trainLabels[i]-1,j] += trainSet[i,j] 
    midPoint = midPoint/float(trainSet.shape[0])
    return midPoint

def classfy2(dataSet,trainSet,trainLabels):
    returnLabels = []
    midPoint = getMidPoint(trainSet,trainLabels)
    for n in range(0,dataSet.shape[0]):
        currentDis = [0.0,0.0,0.0]
        for j in range(0,3):
            currentDis[j] = (dataSet[n,0] - midPoint[j,0])**2 + (dataSet[n,1] - midPoint[j,1])**2 +(dataSet[n,2] -midPoint[j,2])**2
        returnLabels.append(currentDis.index(min(currentDis))+1)
    return returnLabels

def classily2(trainFileName,testFileName):
    trainSet,trainLabels,trainMax,trainMin = file2matrix(trainFileName,0)
    dataSet,dataLabels = file2matrix(testFileName,1,trainMax,trainMin)
    antiLabels = classfy2(dataSet,trainSet,trainLabels)
    correctCount = 0
    for i in range(0,len(dataLabels)):
        if antiLabels[i] == dataLabels[i]:
            correctCount += 1
    print correctCount
    print "Correct Rate:\t%f\n"%(float(correctCount)/len(dataLabels))
    return trainSet,trainLabels,dataSet,dataLabels
    

            
        
    
    
    
    
    
   
    
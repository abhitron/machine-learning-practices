import numpy as np
import math

class LOGREG():

    def __init__(self):
        self.dataMat=np.mat([])
        self.labelMat=np.mat([])

    def sigmoid(self,inData):
        return 1.0/(1+np.exp(-inData))

    def stochasticGradDescent(self):
        [numOfRow,numOfCol]=np.shape(self.dataMat)
        alpha=0.01
        weights=np.mat([1 for i in xrange(numOfCol)])
        for index in xrange(numOfRow):
            h=self.sigmoid(sum(weights*self.dataMat[index].T))
            error=self.labelMat[0,index]-h
            weights=weights+alpha*error*self.dataMat[index]
        return weights

    def modStochasticGradDescent(self,numIter=150):
        [numOfRow,numOfCol]=np.shape(self.dataMat)
        weights=np.ones(numOfCol)
        for j in xrange(numIter):
            dataIndex=range(numOfRow)
            for i in xrange(numOfRow):
                alpha=0.01+(4/(1.0+j+i))
                randIndex=int(np.random.uniform(0,len(dataIndex)))
                h=self.sigmoid(sum(weights*self.dataMat[randIndex].T))
                error=self.labelMat[0,randIndex]-h
                weights=weights+error*alpha*self.dataMat[randIndex]
                del(dataIndex[randIndex])
        return weights

    def trainClassifier(self,trainData,trainLabel,numIter):
        self.dataMat=trainData
        self.labelMat=trainLabel
        return self.modStochasticGradDescent(numIter)

    def classify(self,testVec,weights):
        return self.sigmoid(sum(weights*testVec.T))

def testFun():
    trainFile=open('horseColicTraining.txt')
    testFile=open('horseColicTest.txt')
    trainingSet=[]; trainingLabel=[]
    for line in trainFile.readlines():
        line=line.strip().split('\t')
        trainingSet.append([float(line[i]) for i in xrange(len(line)-1)])
        trainingLabel.append(float(line[len(line)-1]))
    classifier=LOGREG()
    trainWeights=classifier.trainClassifier(np.mat(trainingSet),np.mat(trainingLabel),1000)
    errorCount=0
    numTestExp=0
    for line in testFile.readlines():
        line=line.strip().split('\t')
        testVec=[float(line[i]) for i in xrange(len(line)-1)]
        if(round(classifier.classify(np.mat(testVec),trainWeights))!=int(line[len(line)-1])):
            errorCount+=1
        numTestExp+=1
    errorRate=float(errorCount)/numTestExp
    print "The Error Rate= %f"%errorRate

testFun()
            
    

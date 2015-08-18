from numpy import *
#from math import *
import re

def loadDataset():
    postList=[['my','dog','has','flea','problems','help','please'],
               ['maybe','not','take','him','to','dog','park','stupid'],
               ['my','dalmation','is','so','cute','I','love','him'],
               ['stop','posting','stupid','worthless','garbage'],
               ['mr','licks','ate','my','steak','how','to','stop','him'],
               ['quit','buying','worthless','dog','food','stupid']]
    classVec=[0,1,0,1,0,1]
    return postList,classVec

def createVocablist(dataSet):
    vocabSet=set([])
    for document in dataSet:
        vocabSet=vocabSet|set(document)
    return list(vocabSet)

def wordToVec(vocabList,inputSet):
    retVec=[0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            retVec[vocabList.index(word)]+=1
    return retVec
    
def trainFun(trainMatrix,trainCategory):
    numTrainDocs=len(trainCategory)
    numWords=len(trainMatrix[0])
    probAbusive=sum(trainCategory)/float(numTrainDocs)
    probClass1=ones(numWords);probClass0=ones(numWords)
    wordsInClass1=2;wordsInClass0=2
    for i in range(numTrainDocs):
        if trainCategory[i]==1:
            probClass1+=trainMatrix[i]
            wordsInClass1+=sum(trainMatrix[i])
        else:
            probClass0+=trainMatrix[i]
            wordsInClass0+=sum(trainMatrix[i])

    prob1Vec=log(probClass1/wordsInClass1)
    prob0Vec=log(probClass0/wordsInClass0)
    return prob0Vec,prob1Vec,probAbusive

def classify(vecToClassify,prob0Vec,prob1Vec,probAbusive):
    prob1=sum(vecToClassify*prob1Vec)+log(probAbusive)
    prob0=sum(vecToClassify*prob0Vec)+log(1.0-probAbusive)
    if prob1>prob0:
        return 1
    else:
        return 0

def testClassifier():
    listOfPosts,listClasses=loadDataset()
    myVocablist=createVocablist(listOfPosts)
    trainMat=[]
    for post in listOfPosts:
        trainMat.append(wordToVec(myVocablist,post))
    prob0Vec,prob1Vec,probAbusive=trainFun(array(trainMat),array(listClasses))
    testInput=['stupid','garbage']
    testVec=wordToVec(myVocablist,testInput)
    print "Test input classified as: ",classify(testVec,prob0Vec,prob1Vec,probAbusive)
    

def textParser(textInput):
    listOfTokens=re.split(r'\W',textInput)
    return [tok.lower() for tok in listOfTokens]

def spamTest():
    docList=[];classList=[];fullText=[];
    for i in range(1,26):      #No. of input files
        wordList=textParser(open('email/spam/%d.txt'%i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)     # 1 for spam
        wordList=textParser(open('email/ham/%d.txt'%i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)

    vocabList=createVocablist(docList)
    trainingSet=range(50)
    testSet=[]
    for i in xrange(10):
        randIndex=int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat=[];trainClasses=[]
    for docIndex in trainingSet:
        trainMat.append(wordToVec(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])
    prob0V,prob1V,probSpam=trainFun(array(trainMat),array(trainClasses))
    errorCount=0
    for docIndex in testSet:
        wordVector=wordToVec(vocabList,docList[docIndex])
        if classify(array(wordVector),prob0V,prob1V,probSpam)!=classList[docIndex]:
            print docList[docIndex]
            errorCount+=1
    print 'the error rate is:',float(errorCount)/len(testSet)

spamTest()    
    
    
            
    
    
    

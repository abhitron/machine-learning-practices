from numpy import *
from os import listdir

def image_vector(filename):
        vect=zeros((1,1024))
        f=open(filename)
        for i in xrange(32):
            line=f.readline()
            for j in xrange(32):
                vect[0,32*i+j]=int(line[j])
        return vect


def digit_data_preprocess():
        training_labels=[]
        training_file_list=listdir('trainingDigits')
        num_file=len(training_file_list)
        training_mat=zeros((num_file,1024))
        for i in xrange(num_file):
            filename=training_file_list[i]
            class_name=(filename.split('.')[0]).split("_")[0]
            training_labels.append(class_name)
            training_mat[i,:]=image_vector('trainingDigits/%s'%filename)
        #self.classifier.group=training_mat
        #self.classifier.labels=training_labels
        print training_labels
        test_file_list=listdir('testDigits')
        num_testfile=len(test_file_list)
        test_mat=zeros((num_testfile,1024))
        test_labels=[]
        for i in xrange(num_testfile):
                
            filename=test_file_list[i]
            class_name=(filename.split('.')[0]).split("_")[0]
            test_labels.append(class_name)
            training_mat[i,:]=image_vector('testDigits/%s'%filename)
        

        print training_mat.shape()
        #self.clssifier.test_group=test_mat
        #self.classifier.test_labels=test_lables


digit_data_preprocess()

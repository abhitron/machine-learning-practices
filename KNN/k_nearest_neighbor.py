# Training dataset should be a matrix of m*n where 'm' is the number of training
# data available and 'n' is the number of features.
# Labels should be in the form of list of size 'm' representing the group to
# which each dataset belongs.

# For testing the classifier i provide here 2 example functions
# dating_data_preprocess() and digit_data_preprocess().



from numpy import *
import operator
from os import listdir

class kNN():

    def __init__(self):
        self.group=0
        self.labels=0
        self.test_group=0
        self.test_labels=0

    def create_sample_dataset(self):
        self.group=array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
        self.labels=['A','A','B','B']

    def normalization(self):
        ho_ratio=0.09
        min_values=self.group.min(0)
        max_values=self.group.max(0)
        ranges=max_values-min_values
        norm_dataset=zeros(shape(self.group))
        num=self.group.shape[0]
        norm_dataset=self.group-tile(min_values,(num,1))
        norm_dataset=norm_dataset/tile(ranges,(num,1))
        num_test_vec=int(num*ho_ratio)
        self.group=norm_dataset[num_test_vec:num,:]
        self.test_group=norm_dataset[0:num_test_vec,:]
        self.test_labels=self.labels[:num_test_vec]
        self.labels=self.labels[num_test_vec:num]
            

    def classify(self,in_data,k):
        dataset_size=self.group.shape[0]
        diff_mat=tile(in_data,(dataset_size,1))-self.group
        sq_diff_mat=diff_mat**2
        distances=(sq_diff_mat.sum(axis=1))**0.5
        sort_distances=distances.argsort()
        class_count={}
        for i in xrange(k):
            label=self.labels[sort_distances[i]]
            class_count.setdefault(label,0)
            class_count[label]+=1

        sort_class_count=sorted(class_count.iteritems(),key=operator.itemgetter(1),reverse=True)
        return sort_class_count[0][0]


    def test(self):
        self.create_sample_dataset()
        return self.classify([0,0],3)
        
                
#Testing classifier using two datasets           
#1.datingTestSet
#2.Digit dataset
        
class Test(object):

    def __init__(self,kNN):
        self.classifier=kNN

    def dating_data_preprocess(self,filename='datingTestSet.txt'):
        f=open(filename)
        lines=f.readlines()
        num_lines=len(lines)
        data_mat=zeros((num_lines,3))
        label_vector=[]
        index=0
        for line in lines:
            features=line.strip().split('\t')
            data_mat[index,:]=features[0:3]
            label_vector.append(features[-1])
            index+=1

        self.classifier.group=data_mat
        self.classifier.labels=label_vector
        self.classifier.normalization()
        self.test()

    def image_vector(self,filename):
        vect=zeros((1,1024))
        f=open(filename)
        for i in xrange(32):
            line=f.readline()
            for j in xrange(32):
                vect[0,32*i+j]=int(line[j])
        return vect

    def digit_data_preprocess(self):
        training_labels=[]
        training_file_list=listdir('trainingDigits')
        num_file=len(training_file_list)
        training_mat=zeros((num_file,1024))
        for i in xrange(num_file):
            filename=training_file_list[i]
            class_name=(filename.split('.')[0]).split("_")[0]
            training_labels.append(class_name)
            training_mat[i,:]=self.image_vector('trainingDigits/%s'%filename)
            print "processed" + filename
        self.classifier.group=training_mat
        self.classifier.labels=training_labels
        test_file_list=listdir('testDigits')
        num_testfile=len(test_file_list)
        test_mat=zeros((num_testfile,1024))
        test_labels=[]
        for i in xrange(num_testfile):
            filename=test_file_list[i]
            class_name=(filename.split('.')[0]).split("_")[0]
            test_labels.append(class_name)
            test_mat[i,:]=self.image_vector('testDigits/%s'%filename)
        self.classifier.test_group=test_mat
        self.classifier.test_labels=test_labels
        print "Training completed. Now Testing.."
        self.test()     
        
    def test(self):
        error=0
        num=self.classifier.test_group.shape[0]
        for i in xrange(num):
            result=self.classifier.classify(self.classifier.test_group[i,:],4)
            if(result!=self.classifier.test_labels[i]):
                error+=1
                print result,
                print self.classifier.test_labels[i],
                print "error"

            else:
                print result,
                print self.classifier.test_labels[i]
        print "error rate:%f"%(float(error)/num)
        
        
    
    
#cls=kNN()
#print Test(cls).digit_data_preprocess()

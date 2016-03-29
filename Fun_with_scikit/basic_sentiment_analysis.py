#error in prediction is high because small dataset is used here.

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.cross_validation import train_test_split

data=pd.read_csv('data\imdb_labelled.txt', delimiter='\t',header=None)
print(len(data))
X_train_raw, X_test_raw, y_train, y_test = train_test_split(data[0],data[1])

vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(X_train_raw)
X_test = vectorizer.transform(X_test_raw)

classifier = LogisticRegression()
classifier.fit(X_train, y_train)
predictions = classifier.predict(X_test)

i=0
for sentence in X_test_raw[:5]:
    print("sentence: %s \t prediction: %d" %(sentence,predictions[i]))
    i+=1

false_prediction=0
i =0
for e in y_test[:len(y_test)]:
    if(e!=predictions[i]):
        false_prediction+=1
    i+=1
print(false_prediction)
error_perc=false_prediction/len(y_test)*100

print("Error in predictions: %f" % error_perc)







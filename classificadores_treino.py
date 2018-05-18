import pandas as pd
import numpy as np
import pickle
import gzip

from sklearn import preprocessing
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.metrics import f1_score
from sklearn.svm import LinearSVC
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB

with gzip.open('sent_list.txt.gz', 'rb') as f: vector_sentences = pickle.load(f)

classifiers = [(MLPClassifier(), "MLP"),
               (DecisionTreeClassifier(), "Decision Tree"),
               (LinearSVC(), "Linear SVC"), 
               (MultinomialNB(), "Multinomial Naive-Bayes")]

for classifier, name in classifiers:

    print("\nXXX " + name + " XXX\n")

    X = np.array([x for x in range(len(vector_sentences))])
    kf = KFold(n_splits=10)
    kf.get_n_splits(X)

    precision_total = recall_total = a = b = i = 0
    
    for train_index, test_index in kf.split(X):

        acertos_totais = recall = precision = 0
        
        X_train, X_test = X[train_index], X[test_index]

        feature_test = []
        classi_test = []
        feature_train = []
        classi_train = []
        sentences = []
        words = []

        for sentence in X_test:
            
            aux_f = []
            aux_c = []
            aux_w = []

            for word_feature in vector_sentences[sentence][0]:
                
                aux_f.append(word_feature[2:])
                aux_c.append(int(word_feature[0]))
                aux_w.append(word_feature[1])

            if aux_f != []:
                
                feature_test.append(aux_f)
                classi_test.append(aux_c)
                sentences.append(vector_sentences[sentence][1])
                words.append(aux_w)

        for sentence in X_train:

            for word_feature in vector_sentences[sentence][0]:

                feature_train.append(word_feature[2:])
                classi_train.append(int(word_feature[0]))

        le = preprocessing.LabelEncoder()

        df = pd.DataFrame(feature_train)
        data = df.apply(le.fit_transform, axis=0).values
        target = le.fit_transform(classi_train)

        classifier.fit(data.tolist(), target.tolist())

        predictions = []

        for sentence in feature_test:

            df = pd.DataFrame(sentence)
            data = df.apply(le.fit_transform, axis=0).values

            predictions.append(classifier.predict(data).tolist()) 

        for x in range(len(classi_test)): 

            relation = []

            for y in range(len(predictions[x])): 
                
                if predictions[x][y] == 1: relation.append(words[x][y])

            if 1 in classi_test[x]: a += 1
            else: b += 1
            
            if classi_test[x] == predictions[x] and 1 in classi_test[x]: 

                recall += 1
                precision += 1
                acertos_totais += 1
            
            elif 1 not in classi_test[x] and 1 not in predictions[x]: continue
            elif 1 in classi_test[x]: recall += 1
            elif 1 in predictions[x]: precision += 1

            print("frase: " + str(sentences[x]) +  "\ntripla: (" + words[x][0] + ", " + " ".join(relation) + ", " + words[x][-1] + ")" + "\ncerto: " + str(classi_test[x]) + "\nprevi: " + str(predictions[x]) + "\n")

        if not precision == 0: precision_total += acertos_totais / precision
        recall_total += acertos_totais / recall
        i += 1
        
    print("\nprecision: " + str(precision_total / i) + "\nrecall: " + str(recall_total / i))
    if precision_total == 0 and recall_total == 0: print("f1: 0")
    else: 
        print("f1: " + str((2 * (((precision_total / i) * (recall_total / i)) / ((precision_total / i) + (recall_total / i))))))
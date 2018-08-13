import pandas as pd
import numpy as np
import pickle
import gzip
import sys
import random

from sklearn.model_selection import KFold
from sklearn_crfsuite import CRF

def train_crf(features):
    with gzip.open(features, 'rb') as f: vector_sentences = pickle.load(f)

    random.shuffle(vector_sentences)

    X = np.array([x for x in range(len(vector_sentences))])
    kf = KFold(n_splits=10)
    kf.get_n_splits(X)

    precision_total = recall_total = a = b = c = d = e = i = 0

    with open("saida_treino.txt", "w") as saida: 
      
        for train_index, test_index in kf.split(X):
            
            acertos_totais = recall = precision = 0

            X_train, X_test = X[train_index], X[test_index]

            feature_test = []
            classi_test = []
            feature_train = []
            classi_train = []
            sentences = []
            words = []
            en1 = []
            en2 = []

            for sentence in X_test:
                
                aux_f = []
                aux_c = []
                aux_w = []

                for word_feature in vector_sentences[sentence][0]:

                    dict_f = {}

                    for x in range(len(word_feature[2:])): dict_f[str(x)] = word_feature[2:][x]

                    aux_f.append(dict_f)
                    aux_c.append(word_feature[0])
                    aux_w.append(word_feature[1])

                feature_test.append(aux_f)
                classi_test.append(aux_c)
                sentences.append(vector_sentences[sentence][1])
                words.append(aux_w)
                en1.append(vector_sentences[sentence][2])
                en2.append(vector_sentences[sentence][3])

            for sentence in X_train:

                aux_f = []
                aux_c = []

                for word_feature in vector_sentences[sentence][0]:

                    dict_f = {}

                    for x in range(len(word_feature[2:])): dict_f[str(x)] = word_feature[2:][x]

                    aux_f.append(dict_f)
                    aux_c.append(word_feature[0])
                    
                feature_train.append(aux_f)
                classi_train.append(aux_c)

            crf = CRF(
                algorithm='lbfgs',
                c1=0.1,
                c2=0.1,
                max_iterations=100,
                all_possible_transitions=True
            )

            crf.fit(feature_train, classi_train)

            predictions = crf.predict(feature_test)
            
            # CALCULA AS ESTATÍSTICAS DE PRECISION E RECALL PARA CADA FOLD

            for x in range(len(classi_test)):

                relation = []

                for y in range(len(predictions[x])): 
                    
                    if predictions[x][y] == '1': relation.append(words[x][y])

                if '1' in classi_test[x]: a += 1
                else: b += 1

                if classi_test[x] == predictions[x] and '1' in classi_test[x]: 

                    recall += 1
                    precision += 1
                    acertos_totais += 1
                    
                elif '1' not in classi_test[x] and '1' not in predictions[x]: continue
                elif '1' in classi_test[x]: recall += 1
                elif '1' in predictions[x]: precision += 1
                    
                saida.write("frase: " + str(sentences[x]) +  "\ntripla: (" + en1[x] + ", " + " ".join(relation) + ", " + en2[x] + ")" + "\ncerto: " + str(classi_test[x]) + "\nprevi: " + str(predictions[x]) + "\n\n")

            c += acertos_totais
            d += precision
            e += recall
            
            i += 1
            precision_total += acertos_totais / precision
            recall_total += acertos_totais / recall

        # CALCULA AS ESTATÍSTICAS DE PRECISION E RECALL PARA TODOS OS FOLDS

        saida.write("\nprecision: " + str(precision_total / i) + "\nrecall: " + str(recall_total / i) + "\n")
        if precision_total == 0 and recall_total == 0: saida.write("f1: 0")
        else: 
            saida.write("f1: " + str((2 * (((precision_total / i) * (recall_total / i)) / ((precision_total / i) + (recall_total / i))))) + "\n")

        saida.write("positivos: " + str(a) + "\nnegativos: " + str(b))
        saida.write("\nacertos totais: " + str(c))
        saida.write("\nencontrados: " + str(d))
        saida.write("\ntotal positivos: " + str(e))

    # GERA O MODELO TREINADO COM DATASET INTEIRO

    for sentence in range(len(vector_sentences)): 

        aux_f = []
        aux_c = []

        for word_feature in vector_sentences[sentence][0]:

            dict_f = {}

            for x in range(len(word_feature[2:])): dict_f[str(x)] = word_feature[2:][x]

            aux_f.append(dict_f)
            aux_c.append(word_feature[0])
            
        feature_train.append(aux_f)
        classi_train.append(aux_c)    

    modelo_treinado = CRF(
            algorithm='lbfgs',
            c1=0.1,
            c2=0.1,
            max_iterations=100,
            all_possible_transitions=True
        )

    modelo_treinado.fit(feature_train, classi_train)

    with gzip.open('modelo_treinado.txt.gz', 'wb') as g: pickle.dump(modelo_treinado, g)

def run_crf(features, model):

    with gzip.open(features, 'rb') as f: vector_sentences = pickle.load(f)
    with gzip.open(model, 'rb') as g: crf = pickle.load(g)

    with open("saida_teste.txt", "w") as saida: 

        feature_test = []
        sentences = []
        words = []
        en1 = []
        en2 = []

        for sentence in range(len(vector_sentences)):
            
            aux_f = []
            aux_w = []

            for word_feature in vector_sentences[sentence][0]:

                dict_f = {}

                for x in range(len(word_feature[1:])): dict_f[str(x)] = word_feature[1:][x]

                aux_f.append(dict_f)
                aux_w.append(word_feature[0])

            feature_test.append(aux_f)
            sentences.append(vector_sentences[sentence][1])
            words.append(aux_w)
            en1.append(vector_sentences[sentence][2])
            en2.append(vector_sentences[sentence][3])

        predictions = crf.predict(feature_test)
        
        for x in range(len(predictions)):

            relation = []

            for y in range(len(predictions[x])):

                if predictions[x][y] == '1': relation.append(words[x][y])   

            saida.write("frase: " + str(sentences[x]) +  
                        "\ntripla: (" + en1[x] + ", " + 
                        " ".join(relation) + ", " + en2[x] + ")\n\n")
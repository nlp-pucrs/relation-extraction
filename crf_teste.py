import pandas as pd
import numpy as np
import pickle
import gzip
import sys
import random

from sklearn_crfsuite import CRF

try: 
    
    sys.argv[1]
    sys.argv[2]

except: 
    
    print("Informe o arquivos de entrada como parâmetro")
    sys.exit(1)

with gzip.open(sys.argv[1], 'rb') as f: vector_sentences = pickle.load(f)
with gzip.open(sys.argv[2], 'rb') as g: crf = pickle.load(g)

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

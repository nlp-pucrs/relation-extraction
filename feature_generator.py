import pickle
import gzip
import sys
import subprocess
import os
import time
import psutil
import signal
import re

from cogroo_interface import Cogroo
from math import fabs

def gap(analyzer, vector, idx, x):

    try: 
            
        vector.append(analyzer[idx + x].pos)
        vector.append(analyzer[idx + x].lemma)
        vector.append(analyzer[idx + x].chunk[2:])
        
        aux = analyzer[idx + x].synchunk if len(analyzer[idx + x].synchunk) <= 2 else analyzer[idx + x].synchunk[2:]
        
        vector.append(aux)
        
    except: 

        for x in range(4): vector.append("_")

def consecutive(analyzer, vector, idx, x, y):

    try: 
                
        vector.append(analyzer[idx + x].lemma + " " + analyzer[idx + y].lemma)
        vector.append(analyzer[idx + x].pos + " " + analyzer[idx + y].pos)
        vector.append(analyzer[idx + x].chunk[2:] + " " + analyzer[idx + y].chunk[2:])

        aux = analyzer[idx + x].synchunk if len(analyzer[idx + x].synchunk) <= 2 else analyzer[idx + x].synchunk[2:]
        aux += " "
        aux += analyzer[idx + y].synchunk if len(analyzer[idx + y].synchunk) <= 2 else analyzer[idx + y].synchunk[2:]

        vector.append(aux)

    except: 
        
        for x in range(4): vector.append("_")

def generate_features(name):

    sys.tracebacklimit = None

    #File que guarda entrada do gerador
    f = open("entrada.txt","w+")
    

    file = open(name, "r")

    path = 'java -jar ' + str(os.path.dirname(os.path.realpath(sys.argv[0]))) + '/cogroo4py.jar'

    ##Have to make it work for multiple platforms.
    proc = subprocess.Popen(['gnome-terminal', '-e', path])
    pobj = psutil.Process(proc.pid)

    time.sleep(15)

    cogroo = Cogroo.Instance()
    sentences = []

    for idx, line in enumerate(file):

        aux = line.strip().split("\t")

        #Sentença original de entrada e entidades nomeadas
        f.write("Frase original -" + str(aux[0]) + "\n")
        f.write("EN1 -" + str(aux[2]) + "\n")
        f.write("EN2 -" + str(aux[7]) + "\n")
        

        train_set = False

        if(len(aux) > 7):
            train_set = True

        # PRÉ-PROCESSAMENTO

        frase = aux[0]
        sentence = aux[0].replace("'", '"').replace(":", "#").replace(";", "$").replace(".", "%")
        if(train_set):
            loc = 6
            en1ind = aux[1]
            en2ind = aux[6]
            en1 = aux[2].replace("=", "_").replace(".", "%").replace("'", '"').replace(":", "#").replace(";", "$")
            rel_num = aux[4].split(",")
            rel = aux[5].split(" ")
            en2 = aux[7].replace("=", "_").replace(".", "%").replace("'", '"').replace(":", "#").replace(";", "$")
        else:
            loc = 4
            en1 = aux[2].replace("=", "_").replace(".", "%").replace("'", '"').replace(":", "#").replace(";", "$")
            en2 = aux[5].replace("=", "_").replace(".", "%").replace("'", '"').replace(":", "#").replace(";", "$")
        
        if(train_set):
            if rel_num[0] == 'None': rel_start = 0
            else: rel_start = int(rel_num[0])

        if int(aux[1].split(",")[0]) > int(aux[loc].split(",")[0]): 
            
            small = en2
            big = en1

        else:

            small = en1
            big = en2


        applebits1 = [m.start() for m in re.finditer(en1, sentence)]
        applebits2 = [m.start() for m in re.finditer(en2, sentence)]
        en1ind = en1ind.split(',')[0]
        en2ind = en2ind.split(',')[0]
        minDist = -1
        index_change = -1
        sentence_words = sentence.split(" ")
        print("en1")
        for ab in applebits1:
            index_this = len(sentence[:ab].split(' '))
            dist = abs(int(en1ind) - index_this)
            if minDist == -1:
                minDist = dist
                index_change = index_this -1
            elif minDist > dist:
                minDist = dist
                index_change = index_this - 1
        sentence_words[index_change] = sentence_words[index_change].replace(en1, 'en1')
        print(sentence_words)
        minDist = -1
        index_change = -1
        print("en2")
        for ab in applebits2:
            index_this = len(sentence[:ab].split(' '))
            dist = abs(int(en2ind) - index_this)
            if minDist == -1:
                minDist = dist
                index_change = index_this - 1
            elif minDist > dist:
                minDist = dist
                index_change = index_this - 1
        sentence_words[index_change] = sentence_words[index_change].replace(en2, 'en2')
        print(sentence_words)
        '''
        print(sentence[:int(en1ind)].split(' '))
        print(len(sentence[:int(en1ind)].split(' ')))
        print(en1ind)

        print([m.start() for m in re.finditer(en2, sentence)])
        print(len(sentence[:int(en2ind)].split(' ')))
        print(en2ind)
        '''
        sentence = " ".join(sentence_words)
        if sentence.find('en1') == -1:
        	sentence = sentence.replace(en1, "en1")
        if sentence.find('en2') == -1:
        	sentence = sentence.replace(en2, "en2")

        #Sentença processada para processamento de features e relação entre entidades
        f.write("Frase modificada -" + str(sentence) + "\n")
        ajuda = "Sem relação" if rel == [''] else " ".join(rel)
        f.write(str(ajuda) + "\n")
        

        aux_features = []
        aux_lexeme = []
        pos = ""
        check_en = 0

        if(train_set):
            aux_rel = []
            count_rel = 0
        
        analyzer = cogroo.analyze(sentence).sentences[0].tokens
        words = []

        for idx, t in enumerate(analyzer):

            if check_en == 0 and (t.lexeme == "en1" or t.lexeme == "en2"):

                check_en = 1
                aux_lexeme.append(t.lexeme)
                t.lemma = small.replace("%", ".").replace('"', "'").replace("#", ":").replace("$", ";")
                t.lexeme = small.replace("%", ".").replace('"', "'").replace("#", ":").replace("$", ";")
                continue

            elif check_en == 1 and (t.lexeme == "en1" or t.lexeme == "en2"):
                
                if not t.lexeme == aux_lexeme[0]:

                    t.lemma = big.replace("%", ".").replace('"', "'").replace("#", ":").replace("$", ";")
                    t.lexeme = big.replace("%", ".").replace('"', "'").replace("#", ":").replace("$", ";")
                    break

            elif check_en == 0: continue

            # CLASSE
            
            if(train_set):
                if count_rel == len(rel): classification = 0
                
                elif t.lexeme == rel[count_rel].replace("=", "_").replace(".", "%").replace("'", '"').replace(":", "#").replace(";", "$"):
                    classification = 1
                    count_rel += 1

                else: 
                    classification = 0

            # FEATURES
            
            aux = t.synchunk if len(t.synchunk) <= 2 else t.synchunk[2:]

            pos += " " + t.pos
            vector = [t.lemma, t.pos, t.chunk[2:], aux]

            vector.append("1") if t.pos[0] == "v" else vector.append("0")
            vector.append("1") if t.pos == "adv" else vector.append("0")

            # POS, Lemma and Syntactic Tags (-2, -1, 1, 2)

            gap(analyzer, vector, idx, -2)
            gap(analyzer, vector, idx, -1)
            gap(analyzer, vector, idx, 1)
            gap(analyzer, vector, idx, 2)
            
            consecutive(analyzer, vector, idx, -2, -1)
            consecutive(analyzer, vector, idx, -1, 0)
            consecutive(analyzer, vector, idx, 0, 1)
            consecutive(analyzer, vector, idx, 1, 2)

            # Pattern based features

            try: vector.append("1") if analyzer[idx - 2].pos[0] == "v" else vector.append("0")
            except: vector.append("0")

            try: vector.append("1") if analyzer[idx - 1].pos[0] == "v" else vector.append("0")
            except: vector.append("0")

            try: vector.append("1") if analyzer[idx + 1].pos[0] == "v" else vector.append("0")
            except: vector.append("0")

            try: vector.append("1") if analyzer[idx + 2].pos[0] == "v" else vector.append("0")
            except: vector.append("0")

            try: vector.append("1") if analyzer[idx + 1].pos == "prp" and t.pos[0] == "v" else vector.append("0")
            except: vector.append("0")

            try: vector.append("1") if analyzer[idx + 1].pos == "art" and t.pos[0] == "v" else vector.append("0")
            except: vector.append("0")

            try: vector.append("1") if analyzer[idx + 2].pos == "art" and analyzer[idx + 1].pos == "prp" and t.pos[0] == "v" else vector.append("0")
            except: vector.append("0")

            try: vector.append("1") if analyzer[idx + 1].pos == "prp" and t.pos == "n" else vector.append("0")
            except: vector.append("0")

            try: vector.append("1") if analyzer[idx + 1].pos == "prp" and t.pos == "adv" else vector.append("0")
            except: vector.append("0")

            try: vector.append("1") if analyzer[idx + 2].pos == "art" and analyzer[idx + 1].pos == "prp" and t.pos == "adv" else vector.append("0")
            except: vector.append("0")

            # Syntactic features

            # Núcleo do sintagma

            if not t.lexeme in ("o", "a", "os", "as") and t.pos in ("n", "prop", "pron-det", "pron-pers", "pron-indp") and "NP" in t.chunk: vector.append("1")
            else: vector.append("0")

            # Objeto Direto

            if aux == "ACC": vector.append("1")
            else: vector.append("0")

            vector.insert(0, t.lexeme)

            if(train_set):
                vector.insert(0, str(classification))

            aux = line.strip().split("\t")

            if aux[3] == "PER" or aux[loc+2] == "PER": vector.append("O-PER")
            elif aux[3] == "PLC" or aux[loc+2] == "PLC": vector.append("O-PLC")
            else: vector.append("O-O")

            aux_features.append(vector)

            #Classificação encontrada
            f.write(str(classification) + str(t.lexeme) + "\n")
            

        for x in aux_features:

            x.append(pos[1:])
            x.append(str(len(pos[1:].split(" "))))

            words.append(x)
           
        #Separação entre entradas
        f.write("\n")
        

        en1 = en1.replace("%", ".").replace("'", '"').replace(":", "#").replace(";", "$")
        en2 = en2.replace("%", ".").replace("'", '"').replace(":", "#").replace(";", "$")
        sentences.append([words, frase, en1, en2])

    # SALVA OS VETORES DE FEATURES

    cogroo._end_gateway()

    #Fecha arquivo para escrita de entradas
    f.close()
    
    
    if(train_set):
        with gzip.open('features_treino.txt.gz', 'wb') as f: pickle.dump(sentences, f)
    else:
        with gzip.open('features_teste.txt.gz', 'wb') as f: pickle.dump(sentences, f)

    proc_iter = psutil.process_iter(attrs=["pid", "cmdline"])
    for p in proc_iter:
        process_path = p.info["cmdline"]
        if(len(process_path) == 3 and process_path[2] == (str(os.path.dirname(os.path.realpath(sys.argv[0]))) + '/cogroo4py.jar')):
                os.kill(p.info["pid"], signal.SIGTERM)
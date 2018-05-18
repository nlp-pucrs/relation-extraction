import pickle
import gzip
import sys

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

def main(name):

    file = open(name, "r")

    cogroo = Cogroo.Instance()
    sentences = []

    for idx, line in enumerate(file):

        aux = line.strip().split("\t")

        #print("Frase original -",aux[0])
        #print("EN1 -", aux[2])
        #print("EN2 -",aux[7])

        frase = aux[0]
        sentence = aux[0].replace("'", '"').replace(":", "#").replace(";", "$").replace(".", "%")
        en1 = aux[2].replace("=", "_").replace(".", "%")
        rel_num = aux[4].split(",")
        rel = aux[5].split(" ")
        en2 = aux[7].replace("=", "_").replace(".", "%")
        
        if rel_num[0] == 'None': rel_start = 0
        else: rel_start = int(rel_num[0])

        if int(aux[1].split(",")[0]) > int(aux[6].split(",")[0]): 
            
            small = en2
            big = en1

        else:

            small = en1
            big = en2
        
        sentence = sentence.replace(en1, "en1").replace(en2, "en2")
        
        #print("Frase modificada -",sentence, "\n")
        #ajuda = "Sem relação" if rel == [''] else " ".join(rel)
        #print(ajuda, "\n")

        aux_rel = []
        aux_features = []
        aux_lexeme = []
        pos = ""
        check_en = 0
        count_rel = 0
        
        analyzer = cogroo.analyze(sentence).sentences[0].tokens
        words = []

        for idx, t in enumerate(analyzer):

            if check_en == 0 and (t.lexeme == "en1" or t.lexeme == "en2"):

                check_en = 1
                aux_lexeme.append(t.lexeme)
                t.lemma = small.replace("%", ".")
                t.lexeme = small.replace("%", ".")
                continue

            elif check_en == 1 and (t.lexeme == "en1" or t.lexeme == "en2"):
                
                if not t.lexeme == aux_lexeme[0]:

                    t.lemma = big.replace("%", ".")
                    t.lexeme = big.replace("%", ".")
                    break

            elif check_en == 0: continue

            if count_rel == len(rel): classification = 0
            
            elif t.lexeme == rel[count_rel]: 

                classification = 1
                count_rel += 1

            else: classification = 0
            
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
            vector.insert(0, str(classification))

            aux = line.strip().split("\t")

            if aux[3] == "PER" or aux[8] == "PER": vector.append("O-PER")
            elif aux[3] == "PLC" or aux[8] == "PLC": vector.append("O-PLC")
            else: vector.append("O-O")

            aux_features.append(vector)

            #print(classification, t.lexeme)
            
        for x in aux_features:

            x.append(pos[1:])
            x.append(str(len(pos[1:].split(" "))))

            words.append(x)
            
        #print("\n")

        en1 = en1.replace("%", ".")
        en2 = en2.replace("%", ".")
        sentences.append([words, frase, en1, en2])

    # SALVA OS VETORES DE FEATURES

    with gzip.open('features_treino.txt.gz', 'wb') as f: pickle.dump(sentences, f)

try: sys.argv[1]
except: 
    
    print("Informe o arquivo de entrada como parâmetro")
    sys.exit(1)

main(sys.argv[1])
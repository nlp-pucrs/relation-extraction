#!/bin/bash

python3 relp++.py -fg $1
python3 relp++.py -fg $2
python3 relp++.py -crfgen features_treino.txt.gz
python3 relp++.py -crf features_teste.txt.gz modelo_treinado.txt.gz
#!/bin/bash

python3 relp++.py -fg $1
python3 relp++.py -crfgen features_treino.txt.gz
rm features_treino.txt.gz
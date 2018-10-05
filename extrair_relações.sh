#!/bin/bash

python3 relp++.py -fg $1
python3 relp++.py -crf features_teste.txt.gz $2
rm features_teste.txt.gz
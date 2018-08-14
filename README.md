# Relp++

# Pré-requisitos
 - Java Runtime Environment 8+
 - interpretador Python 3.x
 - Pacote py4j, scikit-learn, sklearn-crfsuite, scipy, pandas, argparse, psutil (*pip3 install py4j scikit-learn sklearn-crfsuite scipy pandas argparse psutil*)


# Execução

- Gerar Features para Treino

    Argumentos de Entrada:
     arquivo com as sentenças (O formato do arquivo deve estar como em Exemplos/texto_treino.txt)

    Argumentos de Saída:
     features de treino (features_treino.txt.gz - O arquivo é substituído a cada execução)

    Exemplo de Uso:
    * python3 relp++ -fg Exemplo/texto_treino.txt

- Gerar Modelo CRF (crf_treino.py)

    Argumento de Entrada:
     features de treino (features_treino.txt.gz)

    Argumentos de Saída:
     modelo treinado (modelo_treinado.txt.gz) 
            resultado da classificação (saida_treino.txt)

    Exemplo de uso:
    *  python3 relp++.py -crfgen features_treino.txt.gz

- Gerar Features para Teste

    Argumento de Entrada:
     arquivo com as sentenças (O formato do arquivo deve estar como em Exemplos/texto_teste.txt)

    Argumento de Saída:
     features de teste (features_teste.txt.gz)

    Exemplo de Uso:
    * python3 relp++.py -fg Exemplo/texto_teste.txt

- Teste do Modelo Treinado

    Argumento de Entrada:
     features de teste (features_teste.txt.gz)
     modelo treinado (modelo_treinado.txt.gz)
    
    Argumento de Saída:
     resultado da classificação de teste (saida_teste.txt)

    Exemplo de Uso:
    * python3 relp++.py -crf features_teste.txt.gz modelo_padrao.txt.gz


# Relp++

# Pré-requisitos
 - Java Runtime Environment 8+
 - interpretador Python 3.x
 - Pacote py4j, scikit-learn, sklearn-crfsuite, scipy, pandas, argparse, psutil (*pip3 install py4j scikit-learn sklearn-crfsuite scipy pandas argparse psutil*)


# Execução
O Relp++ necessita da execução paralela da ferramenta CoGroo4py, disponível no site: https://github.com/gpassero/cogroo4py.

Esta ferramenta já foi proporcionada no pacote de instalação do Relp++ e para executá-la é necessário somente utilizar a seguinte linha de comando na pasta principal:
    * java -jar cogroo4py.jar

# Execução para Treino:

- Gerador de Features para Treino (features_treino.py)

    Argumentos de Entrada:
   	 arquivo com as sentenças (O formato do arquivo deve estar como em Exemplos/texto_treino.txt)

    Argumentos de Saída:
   	 features de treino (features_treino.txt.gz - O arquivo é substituído a cada execução)

    Exemplo de Uso:
   	* python3 features_treino.py Exemplo/texto_treino.txt

- Gerador do Modelo (crf_treino.py)

    Argumento de Entrada:
   	 features de treino (features_treino.txt.gz)
    
    Argumentos de Saída:
   	 modelo treinado (modelo_treinado.txt.gz) 
            resultado da classificação (saida_treino.txt)

    Exemplo de uso:
   	*  python3 crf_treino.py features_treino.txt.gz

# Execução para Teste:

- Gerador de Features para Teste (features_teste.py)

    Argumento de Entrada:
   	 arquivo com as sentenças (O formato do arquivo deve estar como em Exemplos/texto_teste.txt)
    
    Argumento de Saída:
   	 features de teste (features_teste.txt.gz)

    Exemplo de Uso:
   	* python3 features_teste.py Exemplo/texto_teste.txt

- Teste do Modelo Treinado (crf_teste.py)

    Argumento de Entrada:
   	 features de teste (features_teste.txt.gz)
   	 modelo treinado (modelo_treinado.txt.gz)
    
    Argumento de Saída:
   	 resultado da classificação de teste (saida_teste.txt)

    Exemplo de Uso:
   	* python3 crf_teste.py features_teste.txt.gz modelo_padrao.txt.gz


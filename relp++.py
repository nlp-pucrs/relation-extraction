import sys, traceback, os
import feature_generator
import crf
import argparse

parser = argparse.ArgumentParser(description="Relp++ relation extractor")
parser.add_argument("-fg", "--featuregenerator", metavar=('FORMATED_TEXT'), help="Gera features para uso nos geradores de modelo e testes.")
parser.add_argument("-crfgen", "--crfmodelgenerator", metavar=('FEATURES'), help="Gera um modelo de aprendizado de máquina CRF utilizando features indicadas.")
#parser.add_argument("-ftr", "--featurestrain", help="Indica local de features para treino já existentes.")
#parser.add_argument("-fts", "--featurestest", metavar=('FEATURES'), help="Indica local de features para teste já existentes.")
parser.add_argument("-crf", nargs=2, metavar=('FEATURES', 'MODEL'), help="Extrai relações dos textos")

args = parser.parse_args()

try:
	if args.featuregenerator:
		feature_generator.generate_features(args.featuregenerator)
		print("Features criadas com sucesso.")
except:
	print("\nErro na criação de features. Checar se argumento de entrada está no formato correto.\n")
	traceback.print_exc(file=sys.stdout)
	sys.exit(1)

try:
	if args.crfmodelgenerator:
			crf.train_crf(args.crfmodelgenerator)
			print("Modelo CRF gerado com sucesso.")
except:
	print("\nErro na gereção do modelo CRF. Checar se argumento de entrada está no formato correto.\n")
	traceback.print_exc(file=sys.stdout)
	sys.exit(1)

try:
	if args.crf:
			crf.run_crf(args.crf[0], args.crf[1])
			print("Resultados utilizando modelo CRF gerados com sucesso.")
except:
	print("\nErro na geração de resultados para modelo CRF. Checar se argumento de entrada está no formato correto.\n")
	traceback.print_exc(file=sys.stdout)
	sys.exit(1)

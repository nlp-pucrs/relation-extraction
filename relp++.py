import sys, traceback, os
import feature_generator
import crf
import argparse

parser = argparse.ArgumentParser(description="Relp++ relation extractor")
parser.add_argument("-fg", "--featuregenerator", help="Gera features para uso nos geradores de modelo e testes.")
parser.add_argument("-crfgen", "--crfmodelgenerator", nargs="?", const="combo", help="Gera um modelo de aprendizado de máquina CRF utilizando features indicadas.")
parser.add_argument("-ftr", "--featurestrain", help="Indica local de features para treino já existentes.")
parser.add_argument("-fts", "--featurestest", help="Indica local de features para teste já existentes.")
parser.add_argument("-crf", help="Extrai relações dos textos")

args = parser.parse_args()

try:
	if args.featuregenerator:
		feature_generator.generate_features(args.featuregenerator)
		print("Features para treino criadas com sucesso.")
except:
	print("\nErro na criação de features. Checar se argumento de entrada está no formato correto.\n")
	traceback.print_exc(file=sys.stdout)
	sys.exit(1)

try:
	if args.crfmodelgenerator:
		if args.featurestrain:
			crf.train_crf(args.featurestrain)
			print("Modelo CRF gerados com sucesso.")
		elif args.featuregenerator:
			crf.train_crf('features_treino.txt.gz')
			print("Modelo CRF gerados com sucesso.")
		elif args.crfmodelgenerator != "combo":
			feature_generator.generate_features(args.crfmodelgenerator)
			crf.train_crf('features_treino.txt.gz')
			os.remove('features_treino.txt.gz')
			print("Modelo CRF gerados com sucesso.")
		else:
			sys.exit(1)
except:
	print("\nErro na criação do modelo CRF. Checar se argumento de entrada está no formato correto.\n")
	traceback.print_exc(file=sys.stdout)
	sys.exit(1)

try:
	if args.crf:
		if args.featurestest:
			crf.run_crf(args.featurestest, args.crf)
			print("Resultados utilizando modelo CRF gerados com sucesso.")
		else:
			sys.exit(1)
except:
	print("\nErro na criação do modelo CRF. Checar se argumento de entrada está no formato correto.\n")
	traceback.print_exc(file=sys.stdout)
	sys.exit(1)

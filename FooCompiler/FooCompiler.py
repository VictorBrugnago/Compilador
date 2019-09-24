from AnalisadorLexico.AnalisadorLexico import lexical_analyzer
import argparse

param = argparse.ArgumentParser()
param.add_argument("codigo",type=str,help="Codigo fonte")
args = param.parse_args()

print('Lexical')
result = lexical_analyzer(args.codigo)
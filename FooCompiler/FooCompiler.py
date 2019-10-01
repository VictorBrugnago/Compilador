from Analyzers.LexicalAnalyzer.AnalisadorLexico import lexical_analyser
from Analyzers.SyntacticAnalyzer.AnalisadorSintatico import syntactic_analyzer
from Analyzers.SemanticAnalyzer.AnalisadorSemantico import semantic_analyzer
from colorama import Fore
import argparse
import colorama
import logging
import sys

source_code_name = ''

vla_flag = False
vsa_flag = False
vsma_flag = False
lt_flag = False
ls_flag = False

# Set colorama library init
colorama.init(autoreset=True)

# Parameters
parameters = sys.argv[1:]

# Checking Parameters
if not parameters:
    print('No parameters detected!')
    print('Type -> python3 FooCompiler.py [filename].foo [parameters]')
    print('For help, type -> python3 FooCompiler.py -h')
    sys.exit()
else:
    if parameters[0] == '-h':
        print('Use: \n  python3 FooCompiler.py [FILENAME].foo [PARAMETERS]')
        print('\nThe FILENAME should always be BEFORE the parameters!!')
        print('PARAMETERS are optional!')
        print('\nYou can run with ONE or MORE parameters, as long as they are separated by SPACE')
        print('Example: \n  python3 FooCompiler.py [FILENAME].foo -lt -BR')
        print('\n\nAvailable parameters:')
        print('  -lt\tGenerates a listing of the detected tokens, the result is shown in the terminal')
        print('  -tudo\tDisplays a detailed output of the compiler')
        print('  -vla\tDisplays a detailed output of the lexicon analyzer')
        print('  -vsa\tDisplays a detailed output of the syntactic analyzer')
        print('  -vsma\tDisplays a detailed output of the syntactic analyzer')
        print('  -BR \tIt chooses the language of the outputs for Brazilian Portuguese, by default is English. -BR -> '
              'Brazilian Portuguese')
        sys.exit()
    elif str(parameters[0]).endswith('.foo'):
        source_code_name = parameters[0]
        for param in parameters[1:]:
            if param == '-lt':
                lt_flag = True
            elif param == '-ls':
                ls_flag = True
            elif param == '-tudo':
                logging.basicConfig(format='%(message)s', level=logging.DEBUG)
                vla_flag = True
                vsa_flag = True
                vsma_flag = True
            elif param == '-vla':
                vla_flag = True
            elif param == '-vsa':
                vsa_flag = True
            elif param == '-vsma':
                vsma_flag = True
            elif param == '-BR':
                langBR = True
                # br = gettext.translation('base', localedir='locales', languages=['pt'])
                # br.install()
                # _ = br.gettext
    elif not str(parameters[0]).endswith('.foo'):
        print('\n' + Fore.RED + 'Nonexistent file')
        print(Fore.RED + 'File \"{}\" Not found!'.format(str(parameters[0])))
        sys.exit()

print('Performing lexical analysis...')
result_lexicon = lexical_analyser(source_code_name, vla=vla_flag)
print('DONE!')

if lt_flag is True:
    print("List of detected Tokens\n")
    for i in result_lexicon:
        print(i.split(',')[0].center(24), i.split(',')[1].center(24), i.split(',')[2].center(8), i.split(',')[3])

print('\nPerforming syntactic analysis...')
result_syntactic = syntactic_analyzer(result_lexicon, vsa=vsa_flag)

print('\nperforming semantic analysis...')
result_semantic = semantic_analyzer(result_lexicon, vsma=vsma_flag)

if ls_flag is True:
    for i in result_syntactic:
        print(i)
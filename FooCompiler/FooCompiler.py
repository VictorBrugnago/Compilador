from Analyzers.LexicalAnalyzer.AnalisadorLexico import lexical_analyser
from Analyzers.SyntacticAnalyzer.AnalisadorSintatico import syntactic_analyzer
from Analyzers.SemanticAnalyzer.AnalisadorSemantico import semantic_analyzer
from colorama import Fore
import colorama
import gettext
import logging
import sys
import os

# Flags
vlex_flag = False
vsyn_flag = False
vsem_flag = False
all_flag = False
lt_flag = False
lp_flag = False
ls_flag = False
langBR = False

# Source Code
source_code_name = ''

# Set colorama library init
colorama.init(autoreset=True)

if langBR is False:
    _ = lambda s: s

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
        print('  -lp\tGenerates a listing of the productions performed, the result is shown in the terminal')
        print('  -ls\tShows all steps performed on detected variables, the result is shown in the terminal')
        print('  -tudo\tDisplays a detailed output of the compiler')
        print('  -vlex\tDisplays a detailed output of the lexicon analyzer')
        print('  -vsyn\tDisplays a detailed output of the syntactic analyzer')
        print('  -vsem\tDisplays a detailed output of the semantic analyzer')
        print('  -BR \tIt chooses the language of the outputs for Brazilian Portuguese, by default is English. -BR -> '
              'Brazilian Portuguese')
        sys.exit()
    elif str(parameters[0]).endswith('.foo'):
        source_code_name = parameters[0]
        for param in parameters[1:]:
            if param == '-lt':
                lt_flag = True
            elif param == '-lp':
                lp_flag = True
            elif param == '-ls':
                ls_flag = True
            elif param == '-tudo':
                all_flag = True
            elif param == '-vlex':
                vlex_flag = True
            elif param == '-vsyn':
                vsyn_flag = True
            elif param == '-vsem':
                vsem_flag = True
            elif param == '-BR':
                langBR = True
                br = gettext.translation('base_main', localedir='locales', languages=['pt'])
                br.install()
                _ = br.gettext
    elif not str(parameters[0]).endswith('.foo'):
        print('\n' + Fore.RED + _('Nonexistent file'))
        print(Fore.RED + _('File \"{}\" Not found!').format(str(parameters[0])))
        sys.exit()

# Creating a log folder
if not os.path.isdir('logs'):
    os.makedirs('logs')

print(_('Performing lexical analysis...'))
result_lexicon = lexical_analyser(source_code_name, vlex=vlex_flag, vall=all_flag, lang=langBR)

if lt_flag is True:
    print(_('List of detected Tokens\n'))
    for i in result_lexicon:
        print(i.split(',')[0].center(24), i.split(',')[1].center(24), i.split(',')[2].center(8), i.split(',')[3])

print(_('\n\nPerforming syntactic analysis...'))
result_syntactic = syntactic_analyzer(result_lexicon, vsyn=vsyn_flag, vall=all_flag, lang=langBR)

if lp_flag is True:
    print(_('List of production rules carried out\n'))
    for i in result_syntactic:
        print(i)

print(_('\n\nPerforming semantic analysis...'))
result_semantic = semantic_analyzer(result_lexicon, vsem=vsem_flag, vall=all_flag, lang=langBR)

if ls_flag is True:
    for i in result_syntactic:
        print(i)

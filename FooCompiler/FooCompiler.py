from Analyzers.LexicalAnalyzer.AnalisadorLexico import lexical_analyser
from colorama import Fore
import argparse
import colorama
import logging
import sys

source_code_name = ''

val_flag = False

# Set colorama library init
colorama.init(autoreset=True)

# Parameters
parameters = sys.argv[1:]

# Checking Parameters
if not parameters:
    print('No parameters detected!')
    print('Type -> python3 AnalisadorLexico.py [filename].foo [parameters]')
    print('For help, type -> python3 AnalisadorLexico.py -h')
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
        print('  -vc\tDisplays a detailed output of the script')
        print('  -val\tDisplays a detailed output of the script')
        print('  -vas\tDisplays a detailed output of the script')
        print('  -BR \tIt chooses the language of the outputs for Brazilian Portuguese, by default is English. -BR -> '
              'Brazilian Portuguese')
        sys.exit()
    elif str(parameters[0]).endswith('.foo'):
        source_code_name = parameters[0]
        for param in parameters[1:]:
            if param == '-lt':
                lt_flag = True
            elif param == '-BR':
                langBR = True
                # br = gettext.translation('base', localedir='locales', languages=['pt'])
                # br.install()
                # _ = br.gettext
            elif param == '-vc':
                logging.basicConfig(format='%(message)s', level=logging.DEBUG)
            elif param == '-val':

    elif not str(parameters[0]).endswith('.foo'):
        print('\n' + Fore.RED + _('Nonexistent file'))
        print(Fore.RED + _('File \"{}\" Not found!').format(str(parameters[0])))
        sys.exit()

print('Lexical')
result = lexical_analyser(source_code_name, lex_param=[val_flag])

for i in result:
    print(i.split(',')[0].center(24), i.split(',')[1].center(24), i.split(',')[2].center(8), i.split(',')[3])
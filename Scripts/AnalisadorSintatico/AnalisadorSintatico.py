from collections import deque
from colorama import Fore
import colorama
import logging
import csv
import sys

# Set colorama library init
colorama.init(autoreset=True)

# Lists
syntactic_result_list = []
productions_list = []
syntactic_list = []
tokens_list = []

# Dicts
syntactic_state_dict = {}
grammar_state_dict = {}

# Queue & Stack
queue = []
stack = deque()

# Count
location_error = 0

# Flags
lp_flag = False

# Parameters
parameters = sys.argv[1:]

# Checking Parameters
if not parameters:
    pass
else:
    for params in parameters[0:]:
        if params == '-h':
            print('Use: \n  python3 AnalisadorSintatico.py [PARAMETERS]')
            print('PARAMETERS are optional!')
            print('\nYou can run with ONE or MORE parameters, as long as they are separated by SPACE')
            print('Example: \n  python3 AnalisadorSintatico.py -lp -BR')
            print('\n\nAvailable parameters:')
            print('  -lp\tGenerates a listing of the detected productions , the result is shown in the terminal')
            print('  -v\tDisplays a detailed output of the script')
            print('  -BR \tIt chooses the language of the outputs for Brazilian Portuguese, by default is English. -BR '
                  '-> '
                  'Brazilian Portuguese')
            sys.exit()
        if params == '-lp':
            lp_flag = True
        if params == '-v':
            logging.basicConfig(format='%(message)s', level=logging.DEBUG)


def transition(non_terminal_word, terminal_word):
    logging.debug('\n(transition def) Test Transition --> Non Terminal: {}  |  Terminal: {}'.
          format(non_terminal_word, terminal_word))
    if (non_terminal_word, terminal_word) in syntactic_state_dict:
        logging.debug('(transition def) Grammar id: ', syntactic_state_dict[non_terminal_word, terminal_word])
        return syntactic_state_dict[non_terminal_word, terminal_word]
    else:
        return 'error'


# Reading the Production Rules file
with open('Production_Rules.config', newline='', encoding='utf-8') as config:
    buff_reader_config = csv.reader(config, delimiter=',', skipinitialspace=True)
    for line in buff_reader_config:
        productions_list.append(line)

# Reading the Syntactic file
with open('Syntactic_Table.config', newline='') as config:
    buff_reader_config = csv.reader(config, delimiter=',', skipinitialspace=True)
    for line in buff_reader_config:
        syntactic_list.append(line)

# Loading Production Rules
for line_productions in range(len(productions_list)):
    config_id_grammar = productions_list[line_productions][0]
    config_grammar = productions_list[line_productions][1:]
    grammar_state_dict[config_id_grammar] = config_grammar

# Loading Syntactic's dict
for line_syntactic in range(len(syntactic_list)):
    config_final_nonterminal = syntactic_list[line_syntactic][0]
    config_terminal = syntactic_list[line_syntactic][1]
    config_id_grammar = syntactic_list[line_syntactic][2]
    syntactic_state_dict[config_final_nonterminal, config_terminal] = config_id_grammar

# Open list of Tokens and inserting '$' at the beginning of the list
with open('TokensResultLexical.txt', 'r', encoding='utf-8', newline='') as token_file:
    # Creating a list of tokens to using as referencial to syntax erros
    tokens_list = token_file.readlines()
    del tokens_list[0]
    token_file.seek(0)

    # Loading the queue
    tokens_readed = csv.reader(token_file, delimiter=',', skipinitialspace=True)
    for line in (list(tokens_readed)[1:]):  # Starts from line 1
        queue.append(line[0])
    queue.append('$')

# Inserting '$' in the end of stack and inserting the Sentential symbol
stack.append('$')
stack.append('<PROGRAM>')

while queue and stack:
    logging.debug('\nUnstacking...')
    non_terminal_symb = stack[-1]
    logging.debug('NonTerminal symbol on top of stack: ', non_terminal_symb)

    if non_terminal_symb.isupper():
        logging.debug('\nDequeuing...')
        terminal_symb = queue[0]
        logging.debug('Terminal symbol queued: ', terminal_symb)

        grammar = transition(non_terminal_symb, terminal_symb)  # Testing
        if grammar == 'error':
            print(Fore.RED + 'SyntaxError: invalid syntax \'{}\' in line {}'.format(
                tokens_list[location_error].split(', ')[1],
                tokens_list[location_error].split(', ')[2]
            ))
            sys.exit()
        stack.pop()

        logging.debug('\nGrammar id: ', grammar)
        logging.debug('Grammar: ', grammar_state_dict.get(grammar))
        syntactic_result_list.append(non_terminal_symb + ' -> ' + ' '.join(grammar_state_dict.get(grammar)))

        grammar_count = len(grammar_state_dict.get(grammar)) - 1
        while grammar_count >= 0:
            if grammar_state_dict.get(grammar)[grammar_count] != 'î':
                stack.append(grammar_state_dict.get(grammar)[grammar_count])
            grammar_count -= 1
    elif stack[-1] == queue[0]:
        logging.debug('Sentence recognized: {} -> {}'.format(non_terminal_symb, queue[0]))
        del queue[0]
        location_error += 1
        stack.pop()

if not queue and not stack:
    print('\nSyntactic Analyzer completed!')

    if lp_flag is True:
        print('\nList of productions:')
        for i in syntactic_result_list:
            print(i)
else:
    print("Error --> Stack or Queue are not empty")
    sys.exit()

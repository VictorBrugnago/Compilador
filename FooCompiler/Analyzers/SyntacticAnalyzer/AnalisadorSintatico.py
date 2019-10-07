from collections import deque
from colorama import Fore
import colorama
import gettext
import logging
import csv
import sys
import os

# Set colorama library init
colorama.init(autoreset=True)

# Lists
syntactic_result_list = []
reserved_words_list = []
productions_list = []
syntactic_list = []
tokens_list = []

# Dicts
syntactic_state_dict = {}
reserved_words_dict = {}
grammar_state_dict = {}

# Queue & Stack
stack = deque()
queue = []

# Setting up logger
syntactic_logger = logging.getLogger(__name__)
syntactic_logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(message)s'))
syntactic_logger.addHandler(handler)
syntactic_logger.disabled = True


# Reading the Production Rules file
with open(os.path.join(os.path.dirname(__file__), 'Production_Rules.config'), newline='', encoding='utf-8') as config:
    buff_reader_config = csv.reader(config, delimiter=',', skipinitialspace=True)
    for line in buff_reader_config:
        productions_list.append(line)

# Reading the Syntactic file
with open(os.path.join(os.path.dirname(__file__), 'Syntactic_Table.config'), newline='') as config:
    buff_reader_config = csv.reader(config, delimiter=',', skipinitialspace=True)
    for line in buff_reader_config:
        syntactic_list.append(line)

# Reading the Reserved Words file
with open(os.path.join(os.path.dirname(__file__), 'Reserved_Words.config'), newline='', encoding='utf-8') as config:
    buff_reader_config = csv.reader(config, delimiter=',', skipinitialspace=True)
    for line in buff_reader_config:
        reserved_words_list.append(line)

# Loading Production Rules dict
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

# Loading Reserved Words dict
for line_reserved_words in range(len(reserved_words_list)):
    config_token = reserved_words_list[line_reserved_words][0]
    config_lexeme = reserved_words_list[line_reserved_words][1:]
    reserved_words_dict[config_token] = config_lexeme


def syntactic_analyzer(token_list, **syn_param):
    def transition(non_terminal_word, terminal_word):
        syntactic_logger.debug(_('\n(transition def) Test Transition --> Non Terminal: {}  |  Terminal: {}').
                               format(non_terminal_word, terminal_word))
        if (non_terminal_word, terminal_word) in syntactic_state_dict:
            syntactic_logger.debug(_('(transition def) Grammar id: %s'),
                                   syntactic_state_dict[non_terminal_word, terminal_word])
            return syntactic_state_dict[non_terminal_word, terminal_word]
        else:
            return 'error'

    if syn_param.get('lang') is False:
        _ = lambda s: s

    if syn_param.get('lang') is True:
        br = gettext.translation('base_syntactic', localedir='locales', languages=['pt'])
        br.install()
        _ = br.gettext

    if syn_param.get('vsyn') is True or syn_param.get('vall') is True:
        file_handler = logging.FileHandler('logs/syntactic.log', 'w+')
        file_handler.setFormatter(logging.Formatter('%(message)s'))
        syntactic_logger.addHandler(file_handler)
        syntactic_logger.disabled = False

    del token_list[0]
    for token_list_line in list(token_list):
        queue.append(token_list_line.split(',')[0])
    queue.append('$')

    # Count
    location_error = 0

    # Inserting '$' in the end of stack and inserting the Sentential symbol
    stack.append('$')
    stack.append('<PROGRAM>')

    while queue and stack:
        syntactic_logger.debug(_('\nUnstacking...'))
        non_terminal_symb = stack[-1]
        syntactic_logger.debug(_('NonTerminal symbol on top of stack: %s'), non_terminal_symb)

        if non_terminal_symb.isupper():
            syntactic_logger.debug(_('\nDequeuing...'))
            terminal_symb = queue[0]
            syntactic_logger.debug(_('Terminal symbol queued: %s'), terminal_symb)

            grammar = transition(non_terminal_symb, terminal_symb)  # Testing
            if grammar == 'error':
                if reserved_words_dict.get(non_terminal_symb) is None:
                    print(Fore.RED + _('SyntaxError: unexpected \'{}\', invalid character on line {} column {}').format(
                        token_list[location_error].split(',')[1],
                        token_list[location_error].split(',')[2],
                        token_list[location_error].split(',')[3]
                    ))
                    syntactic_logger.error(_('SyntaxError: unexpected \'{}\', invalid character on line {} column {}').
                                           format(token_list[location_error - 1].split(',')[1],
                                                  token_list[location_error].split(',')[2],
                                                  token_list[location_error].split(',')[3]
                                                  ))
                    sys.exit()
                print(Fore.RED + _('SyntaxError: unexpected \'{}\', expecting \'{}\' on line {} column {}').format(
                    token_list[location_error].split(',')[1],
                    ''.join(reserved_words_dict.get(non_terminal_symb)),
                    token_list[location_error].split(',')[2],
                    token_list[location_error].split(',')[3]
                ))
                syntactic_logger.error(_('SyntaxError: unexpected \'{}\', expecting \'{}\' on line {} column {}').
                                       format(token_list[location_error].split(',')[1],
                                              ''.join(reserved_words_dict.get(non_terminal_symb)),
                                              token_list[location_error].split(',')[2],
                                              token_list[location_error].split(',')[3]
                                              ))
                sys.exit()
            stack.pop()

            syntactic_logger.debug(_('\nGrammar id: %s'), grammar)
            syntactic_logger.debug(_('Grammar: %s'), grammar_state_dict.get(grammar))
            syntactic_result_list.append(non_terminal_symb + ' -> ' + ' '.join(grammar_state_dict.get(grammar)))

            grammar_count = len(grammar_state_dict.get(grammar)) - 1
            while grammar_count >= 0:
                if grammar_state_dict.get(grammar)[grammar_count] != 'î':
                    stack.append(grammar_state_dict.get(grammar)[grammar_count])
                grammar_count -= 1
        elif stack[-1] == queue[0]:
            syntactic_logger.debug(_('Sentence recognized: {} -> {}').format(non_terminal_symb, queue[0]))
            del queue[0]
            location_error += 1
            stack.pop()
        elif stack[-1] != queue[0]:
            print(Fore.RED + _('SyntaxError: unexpected \'{}\', expecting \'{}\' on line {} column {}').format(
                token_list[location_error].split(',')[1],
                ''.join(reserved_words_dict.get(non_terminal_symb)),
                token_list[location_error].split(',')[2],
                token_list[location_error].split(',')[3]
            ))
            syntactic_logger.error(_('SyntaxError: unexpected \'{}\', expecting \'{}\' on line {} column {}').format(
                token_list[location_error].split(',')[1],
                ''.join(reserved_words_dict.get(non_terminal_symb)),
                token_list[location_error].split(',')[2],
                token_list[location_error].split(',')[3]
            ))
            sys.exit()

    if not queue and not stack:
        return syntactic_result_list
    else:
        print(Fore.RED + _('Error --> Stack or Queue are not empty'))
        syntactic_logger.error(_('Error --> Stack or Queue are not empty'))
        sys.exit()

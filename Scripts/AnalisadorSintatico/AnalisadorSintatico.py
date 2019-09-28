from collections import deque
import csv
import sys

# Lists
syntactic_list = []
productions_list = []
lista_tokens = []

# Dicts
syntactic_state_dict = {}
grammar_state_dict = {}

# Queue & Stack
queue = []
stack = deque()

# Count
cont = 0


def transition(non_terminal_word, terminal_word):
    print('\n(transition def) Test Transition --> Non Terminal: {}  |  Terminal: {}'.
          format(non_terminal_word, terminal_word))
    if (non_terminal_word, terminal_word) in syntactic_state_dict:
        print('(transition def) Grammar id: ', syntactic_state_dict[non_terminal_word, terminal_word])
        return syntactic_state_dict[non_terminal_word, terminal_word]
    else:
        print('Error')
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
    tokens_readed = csv.reader(token_file, delimiter=',', skipinitialspace=True)
    for line in (list(tokens_readed)[1:]):  # Starts from line 1
        queue.append(line[0])

with open('TokensResultLexical.txt', 'r', encoding='utf-8', newline='') as f:
    lista_tokens = f.readlines()

del lista_tokens[0]
queue.append('$')

# Inserting '$' in the end of stack and inserting the Sentential symbol
stack.append('$')
stack.append('<PROGRAM>')

# for keys,values in syntactic_state_dict.items():
#     print(keys,values)

# print(syntactic_state_dict['<VARIABLE_LIST>', 'int'])
# print(grammar_state_dict.get('0'))
# print(len(grammar_state_dict.get('0')))
# print(type(grammar_state_dict.get('0')))
# print(len(grammar_state_dict.get('0')) - 1)
# print(grammar_state_dict.get('0')[2])
# print(grammar_state_dict.get('0')[2] != 'tk_abre_bloco')


while queue and stack:
    print('\nUnstacking...')
    non_terminal_symb = stack[-1]
    print('NonTerminal symbol on top of stack: ', non_terminal_symb)
    print('Testing: ', queue[0])

    # if non_terminal_symb.isupper() is True:
    if non_terminal_symb.isupper():
        print('\nDequeuing...')
        terminal_symb = queue[0]
        print('Terminal symbol queued: ', terminal_symb)

        grammar = transition(non_terminal_symb, terminal_symb)  # Testing
        if grammar == 'error':
            # print('Error')
            print(f"\nERRO: {lista_tokens[cont].split(', ')[1]} linha:{lista_tokens[cont].split(', ')[2]} coluna:{lista_tokens[cont].split(', ')[3]}")
            break
        stack.pop()

        print('\nGrammar id: ', grammar)
        print('Grammar: ', grammar_state_dict.get(grammar))

        grammar_count = len(grammar_state_dict.get(grammar)) - 1
        while grammar_count >= 0:
            if grammar_state_dict.get(grammar)[grammar_count] != 'î':
                stack.append(grammar_state_dict.get(grammar)[grammar_count])
            grammar_count -= 1
    elif stack[-1] == queue[0]:
        print(f'#{non_terminal_symb} = {queue[0]}#')
        del queue[0]
        cont += 1
        stack.pop()

if not queue and not stack:
    print('\n\nSyntactic Analyzer completed!')
else:
    print("Error --> Stack or Queue ar not empty")
    sys.exit()

# print('\n\nSyntactic Analyzer completed!') if not fila and pilha.isEmpty() else print("Erro pilha ou fila nao estao vazias")


# print('Queue')
# for i in queue:
#     print(i)
#
# queue.pop(0)
# print('\n\n')
# for i in queue:
#     print(i)
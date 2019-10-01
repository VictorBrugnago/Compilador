from colorama import Fore
import colorama
import sys

# Set colorama library init
colorama.init(autoreset=True)

# Dicts
variables_dict = {}

# Strings
previous_token = ''
next_token = ''

# Counters
token_count = 0


def variable_value(line, **kwargs):
    list = ''

    while token_list[line].split(', ')[0] != 'tk_final':
        token_read = token_list[line].split(', ')[0]
        next_lexeme_read = token_list[line + 1].split(', ')[1]
        lexeme_read = token_list[line].split(', ')[1]

        if kwargs.get('atrib') is True:
            if token_read != 'integer':
                print(Fore.RED + 'TypeError: \'{}\' must be integer, not {}'.format(kwargs.get('var'), token_read))
                sys.exit()
        if lexeme_read == '/' and (next_lexeme_read == '0' or (next_lexeme_read in variables_dict.keys() and
                                                               variables_dict[next_lexeme_read] == '0')):
            print(Fore.RED + 'Math Exception: Integer division by zero')
            sys.exit()
        if token_read == 'char' and variables_dict[lexeme_read]:
            list = list + variables_dict[lexeme_read] + ' '
        else:
            list = list + lexeme_read + ' '
        line += 1

    for i in list.rstrip():
        if i.isalpha():
            return list.rstrip()
    return int(eval(list.rstrip()))


with open('TokensResultLexical.txt', 'r', encoding='utf-8') as file:
    token_list = file.readlines()
    del token_list[0]


for line in token_list:
    token = line.split(', ')[0]
    lexeme = line.split(', ')[1]

    if token == 'char':
        if token_list[token_count - 1].split(', ')[0] == 'int':
            print('\nVariable Declaration detected -> {} {}'.format(token_list[token_count - 1].split(', ')[0], lexeme))

            print('Checking if is already declared...')
            if lexeme not in variables_dict.keys():
                if token_list[token_count + 1].split(', ')[0] == 'tk_atrib':
                    variables_dict.update({lexeme: str(variable_value(token_count+2, var=lexeme, atrib=True))})

                else:
                    variables_dict.update({lexeme: None})

                print('\nVariable \'{}\' declared'.format(lexeme))
            else:
                print(Fore.RED + '\nValueError: Variable \'{}\' already declared!'.format(lexeme))
                sys.exit()

        elif lexeme in variables_dict.keys():
            if token_list[token_count + 1].split(', ')[0] == 'tk_atrib':
                variables_dict.update({lexeme: str(variable_value(token_count + 2))})
                print('Variable \'{}\' has value changed to \'{}\''.format(lexeme, variables_dict[lexeme]))
        else:
            print(Fore.RED + '\nNameError: Variable \'{}\' not declared!'.format(lexeme))
            sys.exit()
    token_count += 1

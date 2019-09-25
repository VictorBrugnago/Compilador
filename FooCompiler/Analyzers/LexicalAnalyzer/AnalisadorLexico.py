from colorama import Fore
import colorama
import logging
import csv
import sys
import os


# Set colorama library init
colorama.init(autoreset=True)

config_list = []
finish_state_dict = {}

# Reading the config file
with open(os.path.join(os.path.dirname(__file__), 'FinishStates.config'), newline='') as config:
    buff_reader_config = csv.reader(config, delimiter=',', skipinitialspace=True)
    for line in buff_reader_config:
        if line[0][0] != '#':
            config_list.append(line)
        else:
            config_list.append('#')

# Loading Initial State variable
initial_state = config_list[1][0]

# Loading Finish State's dict
for line_finish_state in range(3, len(config_list)):
    if config_list[line_finish_state][0] != '#':
        config_final_state = config_list[line_finish_state][0]
        config_token = config_list[line_finish_state][1]
        finish_state_dict[config_final_state] = config_token

    # Loading Transition's dict
    with open(os.path.join(os.path.dirname(__file__), 'tokens.config'), 'r', encoding='utf-8') as file:
        token_file = file.readlines()


def transition(states, char):
    print('\n(transition def) Test Transition --> State: {}  |  Character: {}'.format(states, char))
    for line_token in token_file:
        if states + ', ' + char in line_token:
            print('(transition def) Next State: ', line_token.split(', ')[2].rstrip())
            return line_token.split(', ')[2].rstrip()
    return 'error'


def variable(token_buffer):
    print('\n(variable def) Test Variable --> Buffer: ', token_buffer)
    for char in token_buffer:
        if transition('q63', char) == 'error':
            print('\n(variable def) Return: False')
            return False
        else:
            print('\n(variable def) Return: True')
            return True


def error_informer(level, char_error, line_error, column_error, **exits):
    if level == 'EL':
        print('\n' + Fore.RED + 'Lexicon Error')
        print(Fore.RED + 'Character \"{}\" unexpected  -->  Line: {} | Column: {}'.
              format(char_error, str(line_error), str(column_error)))
        if exits is True:
            sys.exit()


def lexical_analyser(source_code_name, **lex_param):

    if params.values() == '-val':
        print('Test -val')
    #logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    with open(source_code_name, 'r', encoding='utf-8') as code_file:
        source_code = code_file.readlines()

    token_result_list = ['TOKEN, LEXEME, LINE, COLUMN']

    new_column_word = 0
    line_counter = 0
    logging.info()

    for line_code in source_code:
        state = initial_state
        buffer_character = ''
        line_counter += 1
        column_counter = 0
        is_text = False

        if line_code[len(line_code) - 1] == '\n':  # To ignore \n
            line_code = line_code.rstrip()

        while column_counter < len(line_code):
            character = line_code[column_counter]
            column_counter += 1
            print('\nCharacter: {}  | Column: {}  |  Line: {}  |  Actual State (Before transition): {}'
                          .format(character, column_counter, line_counter, state))

            # Checking if is start of String
            if character == '"' and is_text is False:
                is_text = True
                print('Starting String...')

            # Checking if is end of String
            elif character == '"' and is_text is True:
                is_text = False
                print('Ending String...')
                if state == 'q60':
                    state = 'q61'

            # Start counting the columns from the beginning of the word
            print(state is initial_state)
            if state is initial_state:
                new_column_word = column_counter

            # Testing for String
            if is_text is True:
                last_state = state
                state = transition(state, character)
                buffer_character = buffer_character + character
                print('Character: {}  |  Actual State (After transition): {}'.format(character, state))
                print('Buffer String: %s', buffer_character)

                if state == 'error':
                    error_informer('EL', character, str(line_counter), str(new_column_word), exits=False)
                    state = last_state
                    buffer_character = buffer_character.replace(character, '')
                if buffer_character == len(line_code) and column_counter == len(line_code):
                    if variable(buffer_character) is False:
                        error_informer('EL', character, str(line_counter), str(new_column_word), exits=False)
                    else:
                        token_result_list.append(finish_state_dict.get(state) + ',' + buffer_character + ',' +
                                                 str(line_counter) + ',' + str(new_column_word))
                        state = initial_state
                        buffer_character = ''

            # In case it is not a String
            else:
                if character != ' ':
                    state = transition(state, character)
                    buffer_character = buffer_character + character  # Concatenate each char to create the complete word
                    print('Character: {}  |  Actual State (After transition): {}'.format(character, state))
                    print('Buffer: ', buffer_character)

                    if column_counter < len(line_code):
                        if transition(state, line_code[column_counter]) == 'error':  # if the char doesn't have state
                            if state in finish_state_dict.keys():  # if the actual state is a finish state
                                token_result_list.append(finish_state_dict.get(state) + ',' + buffer_character + ',' +
                                                         str(line_counter) + ',' + str(new_column_word))
                                state = initial_state
                                buffer_character = ''
                            elif variable(buffer_character) is True:
                                state = 'q63'
                                buffer_character = ''
                                column_counter = new_column_word - 1
                            else:
                                error_informer('EL', character, str(line_counter), str(new_column_word), exits=False)
                                state = initial_state
                                buffer_character = ''
                    else:
                        if state in finish_state_dict.keys():
                            token_result_list.append(finish_state_dict.get(state) + ',' + buffer_character + ',' +
                                                     str(line_counter) + ',' + str(new_column_word))
                            state = initial_state
                            buffer_character = ''
                        if state == 'error':
                            if variable(buffer_character) is False:
                                error_informer('EL', character, str(line_counter), str(new_column_word), exits=False)
                        if variable(buffer_character) is True:
                            state = 'q63'
                            buffer_character = ''
                            column_counter = new_column_word - 1

                if column_counter == len(line_code) and buffer_character == len(line_code):
                    if variable(buffer_character) is False:
                        error_informer('EL', character, str(line_counter), str(new_column_word), exits=False)
                    else:
                        token_result_list.append(finish_state_dict.get(state) + ',' + buffer_character + ',' +
                                                 str(line_counter) + ',' + str(new_column_word))
                        state = initial_state
                        buffer_character = ''

    return token_result_list


# a = lexical_analyser('C:/Users/Victor Brugnago/PycharmProjects/Compilador/FooCompiler/Fatorial.foo')
# print('List of detected Tokens\n')
# for i in a:
#     print(i.split(',')[0].center(24), i.split(',')[1].center(24), i.split(',')[2].center(8), i.split(',')[3])
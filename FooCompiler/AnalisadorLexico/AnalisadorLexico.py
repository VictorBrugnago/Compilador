import csv
import sys
import logging
import colorama
import gettext
from colorama import Fore


# Set colorama library init
colorama.init(autoreset=True)


# Lists
config_list = []
token_result_list = ['TOKEN, LEXEME, LINE, COLUMN']

# Dicts
finish_state_dict = {}

# Flags
lt_flag = False
langBR = False


def transition(states, char):
    logging.debug(_('\n(transition def) Test Transition --> State: {}  |  Character: {}').format(states, char))
    for line_token in token_file:
        if states + ', ' + char in line_token:
            logging.debug(_('(transition def) Next State: %s'), line_token.split(', ')[2].rstrip())
            return line_token.split(', ')[2].rstrip()
    return 'error'


def variable(token_buffer):
    logging.debug(_('\n(variable def) Test Variable --> Buffer: %s'), token_buffer)
    for char in token_buffer:
        if transition('q63', char) == 'error':
            logging.debug('\n(variable def) Return: False')
            return False
        else:
            logging.debug('\n(variable def) Return: True')
            return True


if langBR is False:
    _ = lambda s: s


def error_informer(level, char, line, column, **exits):
    if level == 'EL':
        print('\n' + Fore.RED + _('Lexicon Error'))
        print(Fore.RED + _('Character \"{}\" unexpected  -->  Line: {} | Column: {}').
              format(char, str(line), str(column)))
        if exits is True:
            sys.exit()


# Reading the config file
with open('FinishStates.config', newline='') as config:
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
with open('tokens.config', 'r', encoding='utf-8') as file:
    token_file = file.readlines()


def lexical_analyzer(source_code_name):

    new_column_word = 0
    line_counter = 0

    with open(source_code_name, 'r', encoding='utf-8') as file:
        source_code = file.readlines()

    for line in source_code:
        state = initial_state
        buffer_character = ''
        line_counter += 1
        column_counter = 0

        is_Text = False

        if line[len(line) - 1] == '\n':  # To ignore \n
            line = line.rstrip()

        while column_counter < len(line):
            character = line[column_counter]
            column_counter += 1
            logging.debug(_('\nCharacter: {}  | Column: {}  |  Line: {}  |  Actual State (Before transition): {}')
                          .format(character, column_counter, line_counter, state))

            # Checking if is start of String
            if character == '"' and is_Text is False:
                is_Text = True
                logging.debug(_('Starting String...'))

            # Checking if is end of String
            elif character == '"' and is_Text is True:
                is_Text = False
                logging.debug(_('Ending String...'))
                if state == 'q60':
                    state = 'q61'

            # Start counting the columns from the beginning of the word
            if state is initial_state:
                new_column_word = column_counter

            # Testing for String
            if is_Text is True:
                last_state = state
                state = transition(state, character)
                buffer_character = buffer_character + character
                logging.debug(_('Character: {}  |  Actual State (After transition): {}').format(character, state))
                logging.debug('Buffer String: %s', buffer_character)

                if state == 'error':
                    error_informer('EL', character, line_counter, new_column_word, exits=False)
                    state = last_state
                    buffer_character = buffer_character.replace(character, '')
                if buffer_character == len(line) and column_counter == len(line):
                    if variable(buffer_character) is False:
                        error_informer('EL', character, line_counter, new_column_word, exits=False)
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
                    logging.debug(_('Character: {}  |  Actual State (After transition): {}').format(character, state))
                    logging.debug('Buffer: %s', buffer_character)

                    if column_counter < len(line):
                        if transition(state, line[column_counter]) == 'error':  # if the char doesn't have state
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
                                error_informer('EL', character, line_counter, new_column_word, exits=False)
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
                                error_informer('EL', character, line_counter, new_column_word, exits=False)
                        if variable(buffer_character) is True:
                            state = 'q63'
                            buffer_character = ''
                            column_counter = new_column_word - 1

                if column_counter == len(line) and buffer_character == len(line):
                    if variable(buffer_character) is False:
                        error_informer('EL', character, line_counter, new_column_word, exits=False)
                    else:
                        token_result_list.append(finish_state_dict.get(state) + ',' + buffer_character + ',' +
                                                 str(line_counter) + ',' + str(new_column_word))
                        state = initial_state
                        buffer_character = ''

    print(_('\nCode parsed!'))
    return token_result_list

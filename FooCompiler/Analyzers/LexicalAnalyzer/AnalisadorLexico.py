from colorama import Fore
import colorama
import gettext
import logging
import csv
import sys
import os


# Set colorama library init
colorama.init(autoreset=True)

config_list = []
finish_state_dict = {}

# Setting up logger
lexical_logger = logging.getLogger(__name__)
lexical_logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(message)s'))
lexical_logger.addHandler(handler)
lexical_logger.disabled = True

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


def lexical_analyser(source_code_name, **lex_param):
    def transition(states, char):
        lexical_logger.debug(
            _('\n(transition def) Test Transition --> State: {}  |  Character: {}').format(states, char))
        for line_token in token_file:
            if states + ', ' + char in line_token:
                lexical_logger.debug(_('(transition def) Next State: %s'), line_token.split(', ')[2].rstrip())
                return line_token.split(', ')[2].rstrip()
        return 'error'

    def variable(token_buffer):
        lexical_logger.debug(_('\n(variable def) Test Variable --> Buffer: %s'), token_buffer)
        for char in token_buffer:
            if transition('q63', char) == 'error':
                lexical_logger.debug('\n(variable def) Return: False')
                return False
            else:
                lexical_logger.debug('\n(variable def) Return: True')
                return True

    def error_informer(level, char_error, line_error, column_error, **exits):
        if level == 'EL':
            print('\n' + Fore.RED + _('Lexicon Error'))
            print(Fore.RED + _('Character \"{}\" unexpected  -->  Line: {} | Column: {}').
                  format(char_error, str(line_error), str(column_error)))
            lexical_logger.error(_('Lexicon Error, Character \"{}\" unexpected  -->  Line: {} | Column: {}').
                                 format(char_error, str(line_error), str(column_error)))
            if exits is True:
                sys.exit()

    if lex_param.get('lang') is False:
        _ = lambda s: s

    if lex_param.get('lang') is True:
        br = gettext.translation('base_lexical', localedir='locales', languages=['pt'])
        br.install()
        _ = br.gettext

    if lex_param.get('vlex') is True or lex_param.get('vall') is True:
        file_handler = logging.FileHandler('logs/lexical.log', 'w+')
        file_handler.setFormatter(logging.Formatter('%(message)s'))
        lexical_logger.addHandler(file_handler)
        lexical_logger.disabled = False

    with open(source_code_name, 'r', encoding='utf-8') as code_file:
        source_code = code_file.readlines()

    token_result_list = ['TOKEN, LEXEME, LINE, COLUMN']

    new_column_word = 0
    line_counter = 0

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
            lexical_logger.debug(_('\nCharacter: {}  | Column: {}  |  Line: {}  |  Actual State (Before transition): {}').
                                 format(character, column_counter, line_counter, state))

            # Checking if is start of String
            if character == '"' and is_text is False:
                is_text = True
                lexical_logger.debug(_('Starting String...'))

            # Checking if is end of String
            elif character == '"' and is_text is True:
                is_text = False
                lexical_logger.debug(_('Ending String...'))
                if state == 'q60':
                    state = 'q61'

            # Start counting the columns from the beginning of the word
            if state is initial_state:
                new_column_word = column_counter

            # Testing for String
            if is_text is True:
                last_state = state
                state = transition(state, character)
                buffer_character = buffer_character + character
                lexical_logger.debug(_('Character: {}  |  Actual State (After transition): {}').
                                     format(character, state))
                lexical_logger.debug('Buffer String: %s', buffer_character)

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
                    lexical_logger.debug(_('Character: {}  |  Actual State (After transition): {}').
                                         format(character, state))
                    lexical_logger.debug('Buffer: %s', buffer_character)

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

    lexical_logger.debug(_('DONE!'))
    return token_result_list

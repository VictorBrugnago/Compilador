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

# Strings
buffer_character = ''
source_code_name = ''

# Counters
new_column_word = 0
line_counter = 0

# Flags
lt_flag = False
is_Text = False
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
        print('Use: \n  python3 AnalisadorLexico.py [FILENAME].foo [PARAMETERS]')
        print('\nThe FILENAME should always be BEFORE the parameters!!')
        print('PARAMETERS are optional!')
        print('\nYou can run with ONE or MORE parameters, as long as they are separated by SPACE')
        print('Example: \n  python3 AnalisadorLexico.py [FILENAME].foo -lt -BR')
        print('\n\nAvailable parameters:')
        print('  -lt\tGenerates a listing of the detected tokens, the result is shown in the terminal')
        print('  -v\tDisplays a detailed output of the script')
        print('-BR \tIt chooses the language of the outputs for Brazilian Portuguese, by default is English. -BR -> '
              'Brazilian Portuguese')
        sys.exit()
    elif str(parameters[0]).endswith('.foo'):
        source_code_name = parameters[0]
        for param in parameters[1:]:
            if param == '-lt':
                lt_flag = True
            elif param == '-BR':
                langBR = True
                br = gettext.translation('base', localedir='locales', languages=['pt'])
                br.install()
                _ = br.gettext
            elif param == '-v':
                logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    elif not str(parameters[0]).endswith('.foo'):
        print('\n' + Fore.RED + _('Nonexistent file'))
        print(Fore.RED + _('File \"{}\" Not found!').format(str(parameters[0])))
        sys.exit()


def error_informer(level, **exits):
    if level == 'EL':
        print('\n' + Fore.RED + _('Lexicon Error'))
        print(Fore.RED + _('Character \"{}\" unexpected  -->  Line: {} | Column: {}').
              format(character, str(line_counter), str(new_column_word)))
        if exits is True:
            sys.exit()
    elif level == 'PYV':
        print('\n' + Fore.RED + _('Incompatible Python version'))
        print(Fore.RED + _('This file requires version 3.6 or higher. Version detected in the system: {}')
              .format(sys.version))
        sys.exit()


if sys.version <= '3.7.0':
    error_informer('PYV')

# Reading the config file
with open('FinishStates.config', newline='') as config:
    buff_reader_config = csv.reader(config, delimiter=',', skipinitialspace=True)
    for line in buff_reader_config:
        if line[0][0] != '#':
            config_list.append(line)
        else:
            config_list.append('#')

with open(source_code_name, 'r', encoding='utf-8') as file:
    source_code = file.readlines()

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

        if character == '"' and is_Text is False:
            is_Text = True
            logging.debug(_('Starting String...'))
        elif character == '"' and is_Text is True:
            is_Text = False
            logging.debug(_('Ending String...'))
            if state == 'q60':
                state = 'q61'

        if state is initial_state:
            new_column_word = column_counter
        if is_Text is True:
            last_state = state
            state = transition(state, character)
            buffer_character = buffer_character + character
            logging.debug(_('Character: {}  |  Actual State (After transition): {}').format(character, state))
            logging.debug('Buffer String: %s', buffer_character)

            if state == 'error':
                error_informer('EL', exits=False)
                state = last_state
                buffer_character = buffer_character.replace(character, '')
            if buffer_character == len(line) and column_counter == len(line):
                if variable(buffer_character) is False:
                    error_informer('EL', exits=False)
                else:
                    token_result_list.append(finish_state_dict.get(state) + ',' + buffer_character + ',' +
                                             str(line_counter) + ',' + str(new_column_word))
                    state = initial_state
                    buffer_character = ''
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
                            error_informer('EL', exits=False)
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
                            error_informer('EL', exits=False)
                    if variable(buffer_character) is True:
                        state = 'q63'
                        buffer_character = ''
                        column_counter = new_column_word - 1

            if column_counter == len(line) and buffer_character == len(line):
                if variable(buffer_character) is False:
                    error_informer('EL', exits=False)
                else:
                    token_result_list.append(finish_state_dict.get(state) + ',' + buffer_character + ',' +
                                             str(line_counter) + ',' + str(new_column_word))
                    state = initial_state
                    buffer_character = ''

print(_('\nCode parsed!'))

if lt_flag:
    print(_('List of detected Tokens\n'))
    for i in token_result_list:
        print(i.split(',')[0].center(24), i.split(',')[1].center(24), i.split(',')[2].center(8), i.split(',')[3])

sys.exit()

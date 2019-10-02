from colorama import Fore
import colorama
import gettext
import logging
import sys

# Set colorama library init
colorama.init(autoreset=True)

# List
token_list = []

# Dicts
variables_dict = {}

# Setting up logger
semantic_logger = logging.getLogger(__name__)
semantic_logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(message)s'))
semantic_logger.addHandler(handler)
semantic_logger.disabled = True


def semantic_analyzer(token_list_param, **sem_param):
    def variable_value(line_list, **kwargs):
        buffer = ''

        while token_list[line_list].split(',')[0] != 'tk_final':
            token_read = token_list[line_list].split(',')[0]
            next_lexeme_read = token_list[line_list + 1].split(',')[1]
            lexeme_read = token_list[line_list].split(',')[1]
            line_value_error = token_list[line_list].split(',')[2]
            column_value_error = token_list[line_list].split(',')[3]

            if kwargs.get('atrib') is True:
                if token_read != 'integer':
                    print(Fore.RED + _('TypeError: \'{}\' must be integer, not {} on line {} column {}').
                          format(kwargs.get('var'), token_read, line_value_error, column_value_error))
                    semantic_logger.error(Fore.RED + _('TypeError: \'{}\' must be integer, not {} on line {} column {}').
                                          format(kwargs.get('var'), token_read, line_value_error, column_value_error))
                    sys.exit()
            if lexeme_read == '/' and (next_lexeme_read == '0' or (next_lexeme_read in variables_dict.keys() and
                                                                   variables_dict[next_lexeme_read] == '0')):
                print(Fore.RED + _('Math Exception: Integer division by zero on line {} column {}').
                      format(line_value_error, column_value_error))
                semantic_logger.error(Fore.RED + _('Math Exception: Integer division by zero on line {} column {}').
                                      format(line_value_error, column_value_error))
                sys.exit()
            if token_read == 'char' and variables_dict[lexeme_read]:
                buffer = buffer + variables_dict[lexeme_read] + ' '
            else:
                buffer = buffer + lexeme_read + ' '
            line_list += 1

        for i in buffer.rstrip():
            if i.isalpha():
                return buffer.rstrip()
        return int(eval(buffer.rstrip()))

    if sem_param.get('lang') is False:
        _ = lambda s: s

    if sem_param.get('lang') is True:
        br = gettext.translation('base_semantic', localedir='locales', languages=['pt'])
        br.install()
        _ = br.gettext

    if sem_param.get('vsem') is True or sem_param.get('vall') is True:
        file_handler = logging.FileHandler('logs/semantic.log', 'w+')
        file_handler.setFormatter(logging.Formatter('%(message)s'))
        semantic_logger.addHandler(file_handler)
        semantic_logger.disabled = False

    token_list = token_list_param.copy()

    # Counters
    token_count = 0

    for line in token_list:
        token = line.split(',')[0]
        lexeme = line.split(',')[1]
        line_error = line.split(',')[2]
        column_error = line.split(',')[3]

        if token == 'char':
            if token_list[token_count - 1].split(',')[0] == 'int':
                semantic_logger.debug(_('\nVariable Declaration detected -> {} {}').
                                      format(token_list[token_count - 1].split(',')[0], lexeme))

                semantic_logger.debug(_('Checking if is already declared...'))
                if lexeme not in variables_dict.keys():
                    if token_list[token_count + 1].split(',')[0] == 'tk_atrib':
                        variables_dict.update({lexeme: str(variable_value(token_count + 2, var=lexeme, atrib=True))})

                    else:
                        variables_dict.update({lexeme: None})

                    semantic_logger.debug(_('\nVariable \'{}\' declared').format(lexeme))
                else:
                    print(Fore.RED + _('\nValueError: Variable \'{}\' on line {} column {} is already declared!').
                          format(lexeme, line_error, column_error))
                    semantic_logger.error(
                        Fore.RED + _('\nValueError: Variable \'{}\' on line {} column {} is already declared!').
                        format(lexeme, line_error, column_error))
                    sys.exit()

            elif lexeme in variables_dict.keys():
                if token_list[token_count + 1].split(',')[0] == 'tk_atrib':
                    variables_dict.update({lexeme: str(variable_value(token_count + 2))})
                    semantic_logger.debug(_('Variable \'{}\' has value changed to \'{}\'').
                                          format(lexeme, variables_dict[lexeme]))
            else:
                print(Fore.RED + _('\nNameError: Variable \'{}\' on line {} column {} is not declared!').
                      format(lexeme, line_error, column_error))
                semantic_logger.error(Fore.RED + _('\nNameError: Variable \'{}\' on line {} column {} is not declared!').
                                      format(lexeme, line_error, column_error))
                sys.exit()
        token_count += 1
    semantic_logger.debug(_('DONE!'))

from CodeGenerator.PostfixAlgorithm import infix_2_postfix
from collections import deque
from colorama import Fore
import colorama
import os

# Set colorama library init
colorama.init(autoreset=True)


def logical_symbols(symb):
    logic_identifiers = {'>': '<=', '<': '>=', '>=': '<', '<=': '>', '<>': '==', '==': '<>'}

    return logic_identifiers[symb]


def make_expression(token_exp, line_token_exp):
    expression = []
    line_exp = line_token_exp + 1

    while not ('tk_final' in token_exp[line_exp]):
        expression.append(token_exp[line_exp].split(',')[1])
        line_exp += 1

    return ' '.join(expression)


def make_statement(expression, lexeme, pre_code):
    t = 1
    expression = expression[0].split()
    values = []
    operator = ['+', '-', '*', '/']
    for statement in range(len(expression)):
        if expression[statement] in operator:
            first_operand = values.pop()
            second_operand = values.pop()
            if statement == len(expression) - 1:
                pre_code.append(f'{lexeme} := {second_operand} {first_operand} {expression[statement]}')
                # print('Teste 1: ', f'{lexeme} := {second_operand} {first_operand} {expression[statement]}')
            else:
                pre_code.append(f't{t} := {second_operand} {first_operand} {expression[statement]}')
                values.append(f't{t}')
                # print('Teste 2: ', f't{t} := {second_operand} {first_operand} {expression[statement]}')
                # print('t: ', f't{t}')
                t += 1
        else:
            values.append(expression[statement])
            # print('Teste 3: ', expression[statement])
    if len(values) > 0:
        pre_code.append(f'{lexeme} := {values[0]}')
        # print('Teste 4: ', f'{lexeme} := {values[0]}')


def intermediate_code(tokens_list, start, loop, pre_code, *output, **flags):
    # Counters
    loop_counter = loop
    line = start
    label_stack = deque()

    # Checking Flags
    count_if = 0
    count_else = 0
    loop_flag = False
    is_multiple_If_else = False
    if_statement = flags.get('if_statement_flag')
    else_statement = flags.get('else_statement_flag')
    do_statement = flags.get('do_statement_flag')
    while_statement = flags.get('while_statement_flag')

    while line < len(tokens_list):
        token_readed = tokens_list[line].split(',')[0]
        # print(token_readed)

        if 'inputKey' == token_readed:
            pre_code.append('READ ' + tokens_list[line + 2].split(',')[1])
            # print('READ ' + tokens_list[line + 2].split(',')[1])

        elif 'outputKey' == token_readed:
            pre_code.append('WRITE ' + tokens_list[line + 2].split(',')[1])
            # print('WRITE ' + tokens_list[line + 2].split(',')[1])

        elif 'tk_atrib' == token_readed:
            reverse_polish_notation = [str(infix_2_postfix(make_expression(tokens_list, line))),
                                       infix_2_postfix(make_expression(tokens_list, line))]
            make_statement(reverse_polish_notation, tokens_list[line - 1].split(',')[1], pre_code)

        elif 'int' == token_readed:
            pre_code.append('INT ' + tokens_list[line + 1].split(',')[1])
            # print('INT ' + tokens_list[line + 1].split(',')[1])

        elif 'if' == token_readed:
            # If Controller
            if_statement = True
            count_if += 1

            # Labels Controller
            loop_counter += 1
            else_label = loop_counter

            # If Printer
            pre_code.append('IF ' + tokens_list[line + 2].split(',')[1] + ' ' +
                            logical_symbols(tokens_list[line + 3].split(',')[1]) + ' ' +
                            tokens_list[line + 4].split(',')[1] + ' GOTO _L' + str(else_label))
            # print('IF ' + tokens_list[line + 2].split(',')[1] + ' ' +
            #       logical_symbols(tokens_list[line + 3].split(',')[1]) + ' ' +
            #       tokens_list[line + 4].split(',')[1] + ' GOTO _L' + str(else_label))
            label_stack.append(else_label)

            # label_stack.append(if_exit)
            # list = []
            # line, sd = intermediate_code(tokens_list, line + 5, loop_counter, pre_code,
            #                              if_statement_flag=if_statement, else_statement_flag=else_statement,
            #                              while_statement=while_statement)
            # if sd:
            #     pre_code.append('_L' + str(sd) + ':')
            #     # print('_L' + str(sd) + ':')
            #     loop_counter = sd
            #     if_statement = False
            #     else_statement = False
            # pre_code = pre_code + list
            # loop_counter += 1

        elif 'else' == token_readed:
            # Else Controller
            # else_statement = True
            count_else += 1
            count_if -= 1

            # Label Controller
            # loop_counter += 1
            # if_exit = loop_counter
            if_exit = label_stack.pop()
            else_label = label_stack.pop()
            # if is_multiple_If_else is False:
            #     loop_counter += 1
            #     if_exit = loop_counter
            #     else_label = label_stack.popleft()

            # Label Printer
            pre_code.append('GOTO _L' + str(if_exit))
            # print('GOTO _L' + str(if_exit))
            label_stack.append(if_exit)
            pre_code.append('_L' + str(else_label) + ':')
            # print('_L' + str(else_label) + ':')
            # is_multiple_If_else = False

            # line, sd = intermediate_code(tokens_list, line + 1, (loop_counter + 2),
            #                              pre_code, if_statement_flag=if_statement, else_statement_flag=else_statement,
            #                              while_statement=while_statement)
            # return line, (loop_counter + 2)

        elif 'while' == token_readed:
            # while_statement = True
            loop_flag = True

            loop_counter += 1
            loop_back = loop_counter
            loop_counter += 1
            loop_exit = loop_counter

            pre_code.append('_L' + str(loop_back) + ': IF ' + tokens_list[line + 2].split(',')[1] + ' ' +
                            logical_symbols(tokens_list[line + 3].split(',')[1]) + ' ' +
                            tokens_list[line + 4].split(',')[1] + ' GOTO _L' + str(loop_exit))
            # print('_L' + str(loop_back) + ': IF ' + tokens_list[line + 2].split(',')[1] + ' ' +
            #                 logical_symbols(tokens_list[line + 3].split(',')[1]) + ' ' +
            #                 tokens_list[line + 4].split(',')[1] + ' GOTO _L' + str(loop_exit))
            # i, sd = intermediate_code(tokens_list, line + 5, (loop_counter + 2),
            #                           pre_code, if_statement_flag=if_statement, else_statement_flag=else_statement,
            #                           while_statement_flag=while_statement)
            label_stack.append(loop_back)
            label_stack.append(loop_exit)
            # pre_code.append('GOTO _L' + str(loop_counter + 1))
            # pre_code.append('_L' + str(loop_counter + 2) + ':')
            # loop_counter += 2
            # while_statement = False

        elif 'tk_fecha_bloco' in token_readed and label_stack:
            # if if_statement is True and tokens_list[line + 1].split(',')[1] == 'else':
            if loop_flag is True:
                loop_exit = label_stack.pop()
                loop_back = label_stack.pop()

                pre_code.append('GOTO _L' + str(loop_back))
                # print('GOTO _L' + str(loop_back))
                # label_stack.append(if_exit)
                pre_code.append('_L' + str(loop_exit) + ':')
                # print('_L' + str(loop_exit) + ':')

            elif tokens_list[line + 1].split(',')[1] == 'else':
                # if_statement = False
                # is_multiple_If_else = True
                loop_counter += 1
                if_exit = loop_counter
                label_stack.append(if_exit)
                line += 1
                # if count_else >= 1:
                #     is_multiple_If_else = True
                #     loop_counter += 1
                #     if_exit = loop_counter
                #     label_stack.appendleft(if_exit)
                continue
            elif tokens_list[line + 1].split(',')[1] != 'else':
                count_if -= 1
                if_exit = label_stack.pop()
                pre_code.append('_L' + str(if_exit) + ':')
                # print('_L' + str(if_exit) + ':')
                is_multiple_If_else = False

                # if_statement = False
                # flags['if_statement_flag'] = False
                # else_statement = False # Possible to remove
                # return line + 1, (loop_counter + 1)

        # elif 'tk_fecha_bloco' in token_readed and la is True:
        #     while_statement = False
        #     return line + 1, None

        elif 'tk_fecha_bloco' in token_readed and (label_stack):
            count_else -= 1
            if_exit = label_stack.pop()
            pre_code.append('_L' + str(if_exit) + ':')
            # print('_L' + str(if_exit) + ':')

            # else_statement = False
            # return line + 1, None
        line += 1

    if output[0] is True:
        try:
            with open(output[1] + '.ic', 'w+', encoding='utf-8') as ic_file:
                for pre_code_line in pre_code:
                    ic_file.write(pre_code_line)
                    ic_file.write('\n')
            print('\tCreating Intermediate File:\t' + Fore.LIGHTGREEN_EX + 'DONE!')
        except IOError as ioerror:
            print('\tCreating Intermediate File:\t' + Fore.LIGHTRED_EX + 'ERROR!')
            print('ERROR: ', ioerror)
    elif output[0] is False:
        print('\tCreating Intermediate File:\t' + Fore.LIGHTYELLOW_EX + 'Not Specified!')
    return pre_code


# ss = []
#
# with open('./TokensListsTesters/While.txt', 'r') as file:
#     tokens = file.readlines()
# intermediate_code(tokens, 0, 0, ss)

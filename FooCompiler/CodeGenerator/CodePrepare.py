from CodeGenerator.PostfixAlgorithm import infix_2_postfix
from colorama import Fore
import colorama
import os

# Set colorama library init
colorama.init(autoreset=True)


def logical_symbols(symb):
    logic_identifiers = {'>': '<=', '<': '>=', '>=': '<', '<=': '>', '!=': '==', '==': '!='}

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

    # Checking Flags
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
            if_statement = True
            pre_code.append('IF ' + tokens_list[line + 2].split(',')[1] + ' ' +
                            logical_symbols(tokens_list[line + 3].split(',')[1]) + ' ' +
                            tokens_list[line + 4].split(',')[1] + ' GOTO _L' + str(loop_counter + 1))
            # print('IF ' + tokens_list[line + 2].split(',')[1] + ' ' +
            #       logical_symbols(tokens_list[line + 3].split(',')[1]) + ' ' +
            #       tokens_list[line + 4].split(',')[1] + ' GOTO _L' + str(loop_counter + 1))
            list = []
            line, sd = intermediate_code(tokens_list, line + 5, loop_counter, pre_code,
                                         if_statement_flag=if_statement, else_statement_flag=else_statement,
                                         while_statement=while_statement)
            if sd:
                pre_code.append('_L' + str(sd) + ':')
                # print('_L' + str(sd) + ':')
                loop_counter = sd
                if_statement = False
                else_statement = False
            pre_code = pre_code + list
            loop_counter += 1

        elif 'else' == token_readed:
            else_statement = True
            pre_code.append('GOTO _L' + str(loop_counter + 2))
            # print('GOTO _L' + str(loop_counter + 2))
            pre_code.append('_L' + str(loop_counter + 1) + ':')
            # print('_L' + str(loop_counter + 1) + ':')
            line, sd = intermediate_code(tokens_list, line + 1, (loop_counter + 2),
                                         pre_code, if_statement_flag=if_statement, else_statement_flag=else_statement,
                                         while_statement=while_statement)
            return line, (loop_counter + 2)

        elif 'while' == token_readed:
            while_statement = True
            pre_code.append('_L' + str(loop_counter + 1) + ': IF ' + tokens_list[line + 2].split(',')[1] + ' ' +
                            logical_symbols(tokens_list[line + 3].split(',')[1]) + ' ' +
                            tokens_list[line + 4].split(',')[1] + ' GOTO _L' + str(loop_counter + 2))
            i, sd = intermediate_code(tokens_list, line + 5, (loop_counter + 2),
                                      pre_code, if_statement_flag=if_statement, else_statement_flag=else_statement,
                                      while_statement_flag=while_statement)
            pre_code.append('GOTO _L' + str(loop_counter + 1))
            pre_code.append('_L' + str(loop_counter + 2) + ':')
            loop_counter += 2
            while_statement = False

        elif 'tk_fecha_bloco' in token_readed and if_statement is True:
            # if if_statement is True and tokens_list[line + 1].split(',')[1] == 'else':
            if tokens_list[line + 1].split(',')[1] == 'else':
                if_statement = False
                continue
            if tokens_list[line + 1].split(',')[1] != 'else':
                # if_statement = False
                # flags['if_statement_flag'] = False
                # else_statement = False # Possible to remove
                return line + 1, (loop_counter + 1)

        elif 'tk_fecha_bloco' in token_readed and while_statement is True:
            while_statement = False
            return line + 1, None

        elif 'tk_fecha_bloco' in token_readed and else_statement is True:
            # else_statement = False
            return line + 1, None
        line += 1
    # for i in pre_code:
    #     print(i)
    # with open(os.path.join(os.path.dirname(__file__), 'Intermediate Code.ic'), 'w+', encoding='utf-8') as ic_file:
    #     for pre_code_line in pre_code:
    #         ic_file.write(pre_code_line)
    #         ic_file.write('\n')
    if output[0] is True:
        try:
            with open(os.path.join(os.path.dirname(__file__), output[1] + '.ic'),
                      'w+', encoding='utf-8') as ic_file:
                for pre_code_line in pre_code:
                    ic_file.write(pre_code_line)
                    ic_file.write('\n')
            print('\tCreating Intermediate File:\t' + Fore.LIGHTGREEN_EX + 'DONE!')
        except IOError:
            print('\tCreating Intermediate File:\t' + Fore.RED + 'ERROR!')
    elif output[0] is False:
        print('\tCreating Intermediate File:\t' + Fore.LIGHTYELLOW_EX + 'Not Specified!')
    return pre_code


# ss = []
#
# with open('./TokensListsTesters/TokensResultLexicalWhile.txt', 'r') as file:
#     tokens = file.readlines()
# intermediate_code(tokens, 0, 0, ss)

def logical_symbols(symb):
    logic_identifiers = {'>': '<=', '<': '>=', '>=': '<', '<=': '>', '!=': '==', '==': '!='}

    return logic_identifiers[symb]
def intermediate_code(tokens_list, start, loop, pre_code):
    line = start
    loop_counter = loop

    while line < len(tokens_list):
        token_readed = tokens_list[line].split(', ')[0]
        #print(token_readed)

        if 'inputKey' == token_readed:
            pre_code.append('READ ' + tokens_list[line+2].split(', ')[1])
            print('READ ' + tokens_list[line+2].split(', ')[1])
        elif 'outputKey' == token_readed:
            pre_code.append('WRITE ' + tokens_list[line+2].split(', ')[1])
            print('WRITE ' + tokens_list[line+2].split(', ')[1])
        elif 'int' == token_readed:
            if tokens_list[line+2].split(', ')[0] == 'tk_final':
                pre_code.append('INT ' + tokens_list[line + 1].split(', ')[1])
                print('INT ' + tokens_list[line + 1].split(', ')[1])
            elif tokens_list[line+2].split(', ')[0] == 'tk_atrib':
                pre_code.append('INT ' + tokens_list[line + 1].split(', ')[1] +
                                ' :=  ' + tokens_list[line + 3].split(', ')[1])
                print('INT ' + tokens_list[line + 1].split(', ')[1] +
                      ' :=  ' + tokens_list[line + 3].split(', ')[1])
        # elif 'if' == token_readed:
        #     pre_code.append('IF ' + tokens_list[line + 2].split(', ')[1] + ' ' +
        #                     logical_symbols(tokens_list[line + 3].split(', ')[1]) + ' ' +
        #                     tokens_list[line + 4].split(', ')[1] + ' GOTO _L' + str(loop_counter + 1))
        #     print('IF ' + tokens_list[line + 2].split(', ')[1] + ' ' +
        #                     logical_symbols(tokens_list[line + 3].split(', ')[1]) + ' ' +
        #                     tokens_list[line + 4].split(', ')[1] + ' GOTO _L' + str(loop_counter + 1))
        #     list = []
        #     line, sd = intermediate_code(tokens_list, line + 5, loop_counter, pre_code)
        #     if sd:
        #         pre_code.append('_L' + str(sd) + ':')
        #         print('_L' + str(sd) + ':')
        #         loop_counter = sd
        #     pre_code = pre_code + list
        #     loop_counter += 1
        # elif 'else' == token_readed:
        #     pre_code.append('GOTO _L' + str(loop_counter + 2))
        #     print('GOTO _L' + str(loop_counter + 2))
        #     pre_code.append('_L' + str(loop_counter + 1) + ':')
        #     print('_L' + str(loop_counter + 1) + ':')
        #     line, sd = intermediate_code(tokens_list, line + 1, (loop_counter + 2), pre_code)
        #     return line, (loop_counter + 2)
        line += 1
    # for i in pre_code:
    #     print(i)


ss = []

with open('TokensResultLexical.txt', 'r') as file:
    tokens = file.readlines()
intermediate_code(tokens, 0, 0, ss)

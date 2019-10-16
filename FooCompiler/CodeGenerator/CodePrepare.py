def intermediate_code(tokens_list, start, loop, pre_code):
    line = start
    loop_counter = loop
    logic_identifiers = {'>': '<=', '<': '>=', '>=': '<', '<=': '>', '!=': '==', '==': '!='}

    while line < len(tokens_list):
        token_readed = tokens_list[line].split(', ')[0]
        #print(token_readed)

        if 'inputKey' == token_readed:
            pre_code.append('READ ' + tokens_list[line+2].split(', ')[1])
        elif 'outputKey' == token_readed:
            pre_code.append('WRITE ' + tokens_list[line+2].split(', ')[1])
        elif 'int' == token_readed:
            if tokens_list[line+2].split(', ')[0] == 'tk_final':
                pre_code.append('INT ' + tokens_list[line + 1].split(', ')[1])
            elif tokens_list[line+2].split(', ')[0] == 'tk_atrib':
                pre_code.append('INT ' + tokens_list[line + 1].split(', ')[1] +
                                ' :=  ' + tokens_list[line + 3].split(', ')[1])
        line += 1
    for i in pre_code:
        print(i)


ss = []

with open('TokensResultLexical.txt', 'r') as file:
    tokens = file.readlines()
intermediate_code(tokens, 0, 0, ss)

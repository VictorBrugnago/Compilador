def prepare_code(tokens_list, start, loop, pre_code, output):
    line = start
    loop_counter = loop
    while line < len(tokens_list):
        token_readed = tokens_list[line].split(', ')[0]
        print(token_readed)

        if 'inputKey' == token_readed:
            pre_code.append('READ ' + tokens_list[line+2].split(', ')[1])
        elif 'outputKey' == token_readed:
            pre_code.append('WRITE' + tokens_list[line+1].split(', ')[1])
        line += 1

with open('TokensResultLexical.txt', 'r') as file:
    tokens = file.readlines()
prepare_code(tokens, 0, 0)
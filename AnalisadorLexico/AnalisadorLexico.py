import csv
from collections import defaultdict

error = False
config_list = []
token_list = []
finish_state_dict = {}
transition_dict = defaultdict(list)
line_finish_state = 0
index = 0
word = 'startCodeE'
csv_result = 'result.csv'
buffer_character = ''

is_Text = False


def transition(state, char):
    try:
        for line in token_file:
            print('State: ', state)
            print('Char: ', char)
            if state + ', ' + char in line:
                print('Return: ', line.split(', ')[2].rstrip())
                return line.split(', ')[2].rstrip()
        # return transition_dict[state, char]
    except KeyError:
        return False


def variable(token_buffer):
    for char in token_buffer:
        if transition('q63', char) is not False:
            return True
        else:
            return False


def write_result_csv(token, lexeme, position):
    """
    :param token:
    :param lexeme:
    :param position: position of the first letter of the word -> Line:column
    """
    with open('csv_test.csv', 'a+') as csv_result:
        csv_result_writer = csv.writer(csv_result, delimiter=',', dialect='excel', lineterminator='\n')
        csv_result_writer.writerow([token, lexeme, position])


# Reading the config file
with open('FinishStates.config', newline='') as config:
    buff_reader_config = csv.reader(config, delimiter=',', skipinitialspace=True)
    for line in buff_reader_config:
        if line[0][0] != '#':
            config_list.append(line)
        else:
            config_list.append('#')

# Reading the token file and loading Token's dict
with open('Tokens.config', newline='') as tokens:
    buff_reader_tokens = csv.reader(tokens, delimiter=',', skipinitialspace=True)
    for line in buff_reader_tokens:
        if line[0][0] != '#':
            token_list.append(line)


# Loading Initial State variable
initial_state = config_list[1][0]

# Loading Finish State's dict
for line_finish_state in range(3, len(config_list)):
    if config_list[line_finish_state][0] != '#':
        config_final_state = config_list[line_finish_state][0]
        config_token = config_list[line_finish_state][1]
        finish_state_dict[config_final_state] = config_token

# Loading Transition's dict
with open('tokens.config', 'r') as file:
    token_file = file.readlines()
# for line_transition in range(0, len(token_list)):
#     config_actual_state = token_list[line_transition][0]
#     config_value_input = token_list[line_transition][1]
#     config_next_state = token_list[line_transition][2]
#     transition_dict[config_actual_state, config_value_input].append(config_next_state)

# print('Initial State(s): ', initial_state)
# print('Finish State(s): ', finish_state_dict)
# print('Transitions: ', transition_dict)

state = initial_state
while index < len(word):
    character = str(word[index])

    if character == '"' and is_Text is False:
        is_Text = True
    elif character == '"' and is_Text is True:
        is_Text = False
        if state == 'q60':
            state = 'q61'

    if is_Text is True:
        pass
    else:
        state = transition(state, character)
        buffer_character = buffer_character + character  # Concatenate each char to create the complete word
        print('Buffer: ', buffer_character)

        if transition(state, character) is False:  # if the char doesn't have state
            if state in finish_state_dict.keys():  # if the actual state is a finish state
                write_result_csv(buffer_character, state, '0:0')
                state = 'q0'
                buffer_character = ''
            elif variable(buffer_character) is True:
                state = 'q63'
                buffer_character = ''
            else:
                print('Caractere {} não esperado'.format(character))
                state = 'q0'
                buffer_character = ''

# state = initial_state
# while index < len(word):
#     character = str(word[index])
#     state = transition(state, character)
#     print(state)
#     # print(variable(character))
#     # try:
#     #     state = transition(state, character)
#     #     print(state, state in finish_state_dict.keys())
#     #     #print(state)
#     # except KeyError as e:
#     #     print('Caractere não esperado: ', character)
#     #     error = True
#     index += 1

print('\nResults')
if state in finish_state_dict.keys() and error is False:
    print(word, ' accept')
else:
    print(word, ' not accept')

from collections import deque
import csv

# Queue & Stack
queue = []
stack = deque()

# Open list of Tokens and inserting '$' at the beginning of the list
with open('Tokens.txt', 'r', encoding='utf-8', newline='') as token_file:
    tokens_readed = csv.reader(token_file, delimiter=',', skipinitialspace=True)
    for line in (list(tokens_readed)[1:]):  # Starts from line 1
        queue.append(line)
    queue.append('$')

# Inserting '$' in the end of stack
stack.append('$')

print('Queue')
for i in queue:
    print(i)

queue.pop(0)
print('\n\n')
for i in queue:
    print(i)
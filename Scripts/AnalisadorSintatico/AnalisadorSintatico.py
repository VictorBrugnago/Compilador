from queue import LifoQueue
import csv

# Queue & Stack
queue = []
stack = LifoQueue()

# Open list of Tokens and inserting '$' at the beginning of the list
with open('Tokens.txt', 'r', encoding='utf-8', newline='') as token_file:
    tokens_readed = csv.reader(token_file, delimiter=',', skipinitialspace=True)
    queue.append('$')
    for line in (list(tokens_readed)[1:]):  # Starts from line 1
        queue.append(line)

# Inserting '$' in the end of stack
stack.put('$')


print('Queue')
for i in queue:
    print(i)

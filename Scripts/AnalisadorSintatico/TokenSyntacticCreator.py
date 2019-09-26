from colorama import Fore
import colorama
import sys
import os

csv_file = ''

# Set colorama library init
colorama.init(autoreset=True)

# Parameters
parameters = sys.argv[1:]

# Checking Parameters
if not parameters:
    print('No parameters detected!')
    print('Type -> python3 TokenSyntacticCreator.py [filename].csv [PATH]')
    sys.exit()
else:
    if str(parameters[0]).endswith('.csv'):
        csv_file = parameters[0]
        print(csv_file)
    elif not str(parameters[0]).endswith('.csv'):
        print('\n' + Fore.RED + 'Nonexistent file')
        print(Fore.RED + 'File \"{}\" Not found!'.format(str(parameters[0])))
        sys.exit()
    if parameters[1] is not None:
        path = parameters[1]
        print(path)
    elif parameters[1] is None:
        print('\n' + Fore.RED + 'Path not specified')
        print('Type -> python3 TokenSyntacticCreator.py [filename].csv [PATH]')

table = []
with open(csv_file, 'r') as file:
    head = file.readline().rstrip().split(',')
    for row in file:
        cont = 0
        for column in row.split(','):
            if column.isdigit():
                table.append(row.split(',')[0] + ', ' + head[cont] + ', ' + column + '\n')
            cont += 1

with open(path, 'w+') as file:
    file.writelines(table)

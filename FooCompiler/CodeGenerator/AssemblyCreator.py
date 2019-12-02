from colorama import Fore
import colorama
import logging

# Set colorama library init
colorama.init(autoreset=True)

# Setting up logger
assembly_logger = logging.getLogger(__name__)
assembly_logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(message)s'))
assembly_logger.addHandler(handler)
assembly_logger.disabled = True


def assembly_creation(pre_code, output, **asm_param):

    if asm_param.get('vasm') is True or asm_param.get('vall') is True:
        file_handler = logging.FileHandler('logs/assembly.log', 'w+')
        file_handler.setFormatter(logging.Formatter('%(message)s'))
        assembly_logger.addHandler(file_handler)
        assembly_logger.disabled = False

    msg_counter = 1
    variable = []
    data = ['section .data', '\tformatin: db "%d",0', '\tformatout: db "%d",10,0']
    text = ['section .text', '\tglobal _main', '\textern _printf', '\textern _scanf']
    main = ['\t', '_main:']

    for pc_line in pre_code:

        if 'INT' in pc_line:
            assembly_logger.debug('\n\n\nStep: {}\t\t\t\tDetected INTEGER. Creating code for: {}'.format(pc_line, pc_line.split("INT")[1].strip()))

            data.append(f'\t{pc_line.split("INT")[1].strip()}: dd 0')
            variable.append(pc_line.split("INT")[1].strip())

        elif ':=' in pc_line:
            assembly_logger.debug('Step: {}\t\tDetected ARITHMETIC')
            main.append('')

            if not pc_line.split()[0].strip() in variable:
                assembly_logger.debug('{} is not in variable list. Setting ZERO to it', pc_line.split()[0].strip())
                data.append(f'\t{pc_line.split()[0].strip()}: dd 0')
                variable.append(pc_line.split()[0].strip())

            if '+' in pc_line:
                main.append(
                    f'mov eax, {"dword[" + pc_line.split()[-3].strip() + "]" if not pc_line.split()[-3].strip().isdecimal() else pc_line.split()[-3].strip()}')
                main.append(
                    f'mov ecx, {"dword[" + pc_line.split()[-2].strip() + "]" if not pc_line.split()[-2].strip().isdecimal() else pc_line.split()[-2].strip()}')
                main.append(f'add eax, ecx')
                main.append(f'mov dword[{pc_line.split()[0].strip()}], eax')

            elif '-' in pc_line:
                main.append(
                    f'mov eax, {"dword[" + pc_line.split()[-3].strip() + "]" if not pc_line.split()[-3].strip().isdecimal() else pc_line.split()[-3].strip()}')
                main.append(
                    f'mov ecx, {"dword[" + pc_line.split()[-2].strip() + "]" if not pc_line.split()[-2].strip().isdecimal() else pc_line.split()[-2].strip()}')
                main.append(f'sub eax, ecx')
                main.append(f'mov dword[{pc_line.split()[0].strip()}], eax')

            elif '*' in pc_line:
                main.append(
                    f'mov eax, {"dword[" + pc_line.split()[-3].strip() + "]" if not pc_line.split()[-3].strip().isdecimal() else pc_line.split()[-3].strip()}')
                main.append(
                    f'mov ecx, {"dword[" + pc_line.split()[-2].strip() + "]" if not pc_line.split()[-2].strip().isdecimal() else pc_line.split()[-2].strip()}')
                main.append(f'mul ecx')
                main.append(f'mov dword[{pc_line.split()[0].strip()}], eax')

            elif '/' in pc_line:
                main.append(
                    f'mov eax, {"dword[" + pc_line.split()[-3].strip() + "]" if not pc_line.split()[-3].strip().isdecimal() else pc_line.split()[-3].strip()}')
                main.append(
                    f'mov ecx, {"dword[" + pc_line.split()[-2].strip() + "]" if not pc_line.split()[-2].strip().isdecimal() else pc_line.split()[-2].strip()}')
                main.append(f'mov edx, 0')
                main.append(f'div ecx')
                main.append(f'mov dword[{pc_line.split()[0].strip()}], eax')
            else:
                main.append(f'mov dword[{pc_line.split(":= ")[0].strip()}], {pc_line.split(":= ")[1].strip()}')

        elif 'WRITE' in pc_line.split()[0]:
            assembly_logger.debug('Step: {}\t\tDetected WRITE. Creating code for: {}'.format(pc_line, pc_line.split("WRITE")[1].strip()))

            if '"' in pc_line.split("WRITE")[1]:
                data.append(f'\tmgs{msg_counter}: db {pc_line.split("WRITE")[1].strip()},10,0')
                main.append('')
                main.append(f'push mgs{msg_counter}')
                main.append('call _printf')
                main.append('add esp,4')
                msg_counter += 1
            else:
                main.append('')
                main.append(f'mov ebx, dword[{pc_line.split("WRITE")[1].strip()}]')
                main.append('push ebx')
                main.append('push formatout')
                main.append('call _printf')
                main.append('add esp, 8')

        elif 'READ' in pc_line.split()[0]:
            assembly_logger.debug('Step: {}\t\tDetected READ. Creating code for: {}'.format(pc_line, pc_line.split("READ")[1].strip()))

            main.append('')
            main.append(f'push {pc_line.split("READ")[1].strip()}')
            main.append('push formatin')
            main.append('call _scanf')
            main.append('add esp,8')

        elif 'IF' in pc_line.split()[0]:
            assembly_logger.debug('Step: {}\t\tDetected IF. Creating statement...'.format(pc_line))

            main.append('')
            main.append(
                f'mov eax, {"dword[" + pc_line.split()[1].strip() + "]" if not pc_line.split()[1].strip().isdecimal() else pc_line.split()[1].strip()}')
            main.append(
                f'cmp eax, {"dword[" + pc_line.split()[3].strip() + "]" if not pc_line.split()[3].strip().isdecimal() else pc_line.split()[3].strip()}')

            if '<=' in pc_line:
                assembly_logger.debug('IF Statement\t\tJumping JLE to {}\n'.format(pc_line.split()[5].strip()))
                main.append(f'jle {pc_line.split()[5].strip()}')

            elif '>=' in pc_line:
                assembly_logger.debug('IF Statement\t\tJumping JGE to {}\n'.format(pc_line.split()[5].strip()))
                main.append(f'jge {pc_line.split()[5].strip()}')

            elif '<' in pc_line:
                assembly_logger.debug('IF Statement\t\tJumping JL to {}\n'.format(pc_line.split()[5].strip()))
                main.append(f'jl {pc_line.split()[5].strip()}')

            elif '>' in pc_line:
                assembly_logger.debug('IF Statement\t\tJumping JG to {}\n'.format(pc_line.split()[5].strip()))
                main.append(f'jg {pc_line.split()[5].strip()}')

            elif '==' in pc_line:
                assembly_logger.debug('IF Statement\t\tJumping JE to {}\n'.format(pc_line.split()[5].strip()))
                main.append(f'je {pc_line.split()[5].strip()}')

            elif '<>' in pc_line:
                assembly_logger.debug('IF Statement\t\tJumping JNE to {}\n'.format(pc_line.split()[5].strip()))
                main.append(f'jne {pc_line.split()[5].strip()}')

        elif 'GOTO' in pc_line.split()[0]:
            assembly_logger.debug('Step: {}\t\tIF Statement --> Jumping JMP to {}\n'.format(pc_line, pc_line.split()[1].strip()))

            main.append('')
            main.append(f'jmp {pc_line.split()[1].strip()}')

        elif '_L' in pc_line.split()[0]:
            assembly_logger.debug('\nDetected Label {}\t\tCreating Statement'.format(pc_line))

            if 'IF' in pc_line:
                assembly_logger.debug('Step: {}\t\tDetected IF. Creating statement...'.format(pc_line))
                main.append('')
                main.append(f'{pc_line.split()[0]}')
                main.append(
                    f'mov eax, {"dword[" + pc_line.split()[2].strip() + "]" if not pc_line.split()[2].strip().isdecimal() else pc_line.split()[2].strip()}')
                main.append(
                    f'cmp eax, {"dword[" + pc_line.split()[4].strip() + "]" if not pc_line.split()[4].strip().isdecimal() else pc_line.split()[4].strip()}')

                if '<=' in pc_line:
                    assembly_logger.debug('IF Statement\t\tJumping JLE to {}\n'.format(pc_line.split()[6].strip()))
                    main.append(f'jle {pc_line.split()[6].strip()}')

                elif '>=' in pc_line:
                    assembly_logger.debug('IF Statement\t\tJumping JGE to {}\n'.format(pc_line.split()[6].strip()))
                    main.append(f'jge {pc_line.split()[6].strip()}')

                elif '<' in pc_line:
                    assembly_logger.debug('IF Statement\t\tJumping JL to {}\n'.format(pc_line.split()[6].strip()))
                    main.append(f'jl {pc_line.split()[6].strip()}')

                elif '>' in pc_line:
                    assembly_logger.debug('IF Statement\t\tJumping JG to {}\n'.format(pc_line.split()[6].strip()))
                    main.append(f'jg {pc_line.split()[6].strip()}')

                elif '==' in pc_line:
                    assembly_logger.debug('IF Statement\t\tJumping JE to {}\n'.format(pc_line.split()[6].strip()))
                    main.append(f'je {pc_line.split()[6].strip()}')

                elif '<>' in pc_line:
                    assembly_logger.debug('IF Statement\t\tJumping JNE to {}\n'.format(pc_line.split()[6].strip()))
                    main.append(f'jne {pc_line.split()[6].strip()}')

            else:
                main.append('')
                main.append(f'{pc_line.strip()}')

    code = data + text + main
    assembly_logger.debug('End of Program...\n\n\n')
    code.append('ret')

    if output:
        try:
            with open(output + '.asm', 'w+', encoding='utf-8') as ic_file:
                for code_line in code:
                    ic_file.write(code_line)
                    ic_file.write('\n')
            print('\tCreating Assembly File:\t\t' + Fore.LIGHTGREEN_EX + 'DONE!')
        except IOError as ioerror:
            print('\tCreating Assembly File:\t\t' + Fore.RED + 'ERROR!')
            print('ERROR: ', ioerror)
    elif output is False:
        print('\tCreating Assembly File:\t\t' + Fore.LIGHTYELLOW_EX + 'Not Specified!')

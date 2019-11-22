section .data
	formatin: db "%d",0
	formatout: db "%d",10,0
	num: dd 0
	fatorial: dd 0
	mgs1: db "Entre com um numero: ",10,0
	mgs2: db "O numero eh 5",10,0
	mgs3: db "O numero nao eh igual a 5",10,0
	mgs4: db "O numero eh maior que 5",10,0
	mgs5: db "O numero eh menor que 5",10,0
	mgs6: db "Realizando o fatorial...",10,0
	mgs7: db "O fatorial eh: ",10,0
section .text
	global _main
	extern _printf
	extern _scanf
	
_main:

mov dword[fatorial], 1

push mgs1
call _printf
add esp,4

push num
push formatin
call _scanf
add esp,8

mov eax, dword[num]
cmp eax, 5
jne _L1

push mgs2
call _printf
add esp,4

jmp _L2

_L1:

push mgs3
call _printf
add esp,4

mov eax, dword[num]
cmp eax, 5
jle _L3

push mgs4
call _printf
add esp,4

jmp _L4

_L3:

mov eax, dword[num]
cmp eax, 5
jge _L5

push mgs5
call _printf
add esp,4

_L5:

_L4:

_L2:

push mgs6
call _printf
add esp,4

_L6:
mov eax, dword[num]
cmp eax, 1
jle _L7

mov eax, dword[num]
mov ecx, dword[fatorial]
mul ecx
mov dword[fatorial], eax

mov eax, dword[num]
mov ecx, 1
sub eax, ecx
mov dword[num], eax

jmp _L6

_L7:

push mgs7
call _printf
add esp,4

mov ebx, dword[fatorial]
push ebx
push formatout
call _printf
add esp, 8
ret

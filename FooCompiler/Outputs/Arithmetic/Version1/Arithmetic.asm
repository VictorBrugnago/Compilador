section .data
	formatin: db "%d",0
	formatout: db "%d",10,0
	num: dd 0
	fatorial: dd 0
	mgs1: db "Entre com um numero: ",10,0
	mgs2: db "Realizando conta 2 + 2 e salvando no fatorial...",10,0
	mgs3: db "O valor eh menor ou igual a 5",10,0
	mgs4: db "O resultado de fatorial eh: ",10,0
	mgs5: db "Fim do programa",10,0
section .text
	global _main
	extern _printf
	extern _scanf
	
_main:

push mgs1
call _printf
add esp,4

push num
push formatin
call _scanf
add esp,8

mov eax, dword[num]
cmp eax, 5
jle _L1

push mgs2
call _printf
add esp,4

mov eax, 2
mov ecx, 2
add eax, ecx
mov dword[fatorial], eax

jmp _L2

_L1:

push mgs3
call _printf
add esp,4

_L2:

push mgs4
call _printf
add esp,4

mov ebx, dword[fatorial]
push ebx
push formatout
call _printf
add esp, 8

push mgs5
call _printf
add esp,4
ret

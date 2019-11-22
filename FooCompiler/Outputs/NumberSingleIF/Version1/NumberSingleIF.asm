section .data
	formatin: db "%d",0
	formatout: db "%d",10,0
	num: dd 0
	fatorial: dd 0
	mgs1: db "Entre com um numero: ",10,0
	mgs2: db "O Valor eh maior que 2: ",10,0
	mgs3: db "Fim do programa",10,0
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
cmp eax, 2
jle _L1

push mgs2
call _printf
add esp,4

mov ebx, dword[num]
push ebx
push formatout
call _printf
add esp, 8

_L1:

push mgs3
call _printf
add esp,4
ret

section .data
	formatin: db "%d",0
	formatout: db "%d",10,0
	num: dd 0
	fatorial: dd 0
	mgs1: db "Entre com um numero: ",10,0
	mgs2: db "O Valor eh maior que 2: ",10,0
	mgs3: db "O valor eh menor 2",10,0
	mgs4: db "O valor eh 1",10,0
	mgs5: db "O valor eh menor que 1",10,0
	mgs6: db "Fim do programa",10,0
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

jmp _L2

_L1:

push mgs3
call _printf
add esp,4

mov eax, dword[num]
cmp eax, 1
jne _L3

push mgs4
call _printf
add esp,4

jmp _L4

_L3:

push mgs5
call _printf
add esp,4

_L4:

_L2:

push mgs6
call _printf
add esp,4
ret

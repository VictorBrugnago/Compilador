section .data
	formatin: db "%d",0
	formatout: db "%d",10,0
	num: dd 0
	mgs1: db "Entre com um numero inteiro para ser testado: ",10,0
	mgs2: db "O valor inserido eh maior ou igual a 7",10,0
	mgs3: db "O valor inserido eh menor ou igual a 7",10,0
	mgs4: db "O valor inserido igual a 7",10,0
	mgs5: db "O valor inserido eh diferente de 7",10,0
	mgs6: db "O valor inserido eh maior que 7",10,0
	mgs7: db "O valor inserido eh menor que 7",10,0
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
cmp eax, 7
jl _L1

push mgs2
call _printf
add esp,4

jmp _L2

_L1:

mov eax, dword[num]
cmp eax, 7
jg _L3

push mgs3
call _printf
add esp,4

_L3:

_L2:

mov eax, dword[num]
cmp eax, 7
jl _L4

push mgs4
call _printf
add esp,4

jmp _L5

_L4:

mov eax, dword[num]
cmp eax, 7
je _L6

push mgs5
call _printf
add esp,4

_L6:

_L5:

mov eax, dword[num]
cmp eax, 7
jle _L7

push mgs6
call _printf
add esp,4

jmp _L8

_L7:

mov eax, dword[num]
cmp eax, 7
jge _L9

push mgs7
call _printf
add esp,4

_L9:

_L8:
ret

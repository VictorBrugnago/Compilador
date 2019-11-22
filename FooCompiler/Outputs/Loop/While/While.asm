section .data
	formatin: db "%d",0
	formatout: db "%d",10,0
	num: dd 0
	mgs1: db "Entre com um valor: ",10,0
	mgs2: db "Olar",10,0
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

_L1:
mov eax, dword[num]
cmp eax, 0
jle _L2

push mgs2
call _printf
add esp,4

mov ebx, dword[num]
push ebx
push formatout
call _printf
add esp, 8

mov eax, dword[num]
mov ecx, 1
sub eax, ecx
mov dword[num], eax

jmp _L1

_L2:

push mgs3
call _printf
add esp,4
ret

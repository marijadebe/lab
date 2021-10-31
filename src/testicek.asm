bits 64
default rel
segment .bss
segment .data
format_result db "%d", 0
zetko db "hello", 0xd, 0xa, 0
x dd 5
y dd 0
segment .text
global main
extern ExitProcess
extern printf
main:
push rbp
mov rbp, rsp
sub rsp, 32
mov rbx, [x]
mov rax, 5

mul rbx
mov [y], rax
lea rcx, [format_result]
mov rdx, [y]
call printf
lea rcx, [zetko]
call printf
xor rax, rax
leave
call ExitProcess

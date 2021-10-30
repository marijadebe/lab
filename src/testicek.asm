bits 64
default rel
segment .data
format_result db "%d", 0xa, 0
ZISSTMcZDKELUbda db "hello friend", 0xd, 0xa, 0
x dd 5
segment .text
global main
extern ExitProcess
extern printf
main:
push rbp
mov rbp, rsp
sub rsp, 32
lea rcx, [ZISSTMcZDKELUbda]
call printf
lea rcx, [format_result]
mov rdx, [x]
call printf
xor rax, rax
leave
call ExitProcess

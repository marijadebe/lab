bits 64
default rel
segment .data
pHSHBqUvbJXbpund db "ahoj svete", 0xd, 0xa, 0
lKJRviUIFwbtUtXz db "enco jinehojdajsajsd", 0xd, 0xa, 0
segment .text
global main
extern _CRT_INIT
extern ExitProcess
extern printf
main:
push rbp
mov rbp, rsp
sub rsp, 32
lea rcx, [pHSHBqUvbJXbpund]
call printf
lea rcx, [lKJRviUIFwbtUtXz]
call printf
xor rax, rax
leave
call ExitProcess

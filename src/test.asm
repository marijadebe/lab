bits 64
default rel

segment .data
    msg db "Hello World! %d", 0
    dat dq 12

segment .text

global main
extern ExitProcess
extern printf

main:
    push rbp
    mov rbp, rsp
    sub rsp, 32

    lea rcx, [msg]
    mov rdx, [dat]
    call printf
    
    xor rax, rax
    leave
    call ExitProcess
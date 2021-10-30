from enum import Enum
import sys
import re
import random, string
import subprocess
import os

from models.token import Token
from models.tree import Tree
from models.types import Types
from controllers.lexer import lexer
from controllers.ast import ast

#Compiler
def compile(astree, file):
    file = os.path.splitext(file)[0]+'.asm'
    string_dict = {}
    var_dict = {}
    with open(file, 'w') as asm:
        asm.write('bits 64\n')
        asm.write('default rel\n')
        asm.write('segment .data\n')
        for x in range(len(astree)):
            for y in range(len(astree[x].children)):
                if astree[x].getChild(y).getToken().getType() == Types.STRING:
                    string_dict[astree[x].getChild(y).getToken().getValue()] = ''.join(random.choices(string.ascii_letters, k=16))
        for key in string_dict:
            asm.write(string_dict[key]+' db "'+key+'", 0xd, 0xa, 0\n')
        asm.write('segment .text\n')
        asm.write('global main\n')
        asm.write('extern _CRT_INIT\n')
        asm.write('extern ExitProcess\n')
        asm.write('extern printf\n')
        asm.write('main:\n')
        asm.write('push rbp\n')
        asm.write('mov rbp, rsp\n')
        asm.write('sub rsp, 32\n')
        for x in range(len(astree)):
            if(astree[x].getToken().getType() == Types.FUNCTION and astree[x].getToken().getValue() == "out"):
                for y in range(len(astree[x].children)):
                    if(astree[x].getChild(y).getToken().getType() == Types.STRING):
                        promenna = string_dict[astree[x].getChild(y).getToken().getValue()]
                        asm.write('lea rcx, ['+promenna+']\n')
                        asm.write('call printf\n')
        asm.write('xor rax, rax\n')
        asm.write('leave\n')
        asm.write('call ExitProcess\n')

    subprocess.run(['nasm', '-f','win64',file,'-o','objectfile.o'])
    subprocess.run(['gcc','objectfile.o','-o',os.path.splitext(file)[0]+'.exe'])

def main():
    source = sys.argv[1]
    output = sys.argv[2]
    tokens = lexer(source)
    astree = ast(tokens)
    compile(astree, output)

main()
#Global imports
import sys
import subprocess
import os

#Imports for interpreter & compiler
from models.token import Token
from models.tree import Tree
from models.types import Types
from controllers.lexer import lexer
from controllers.ast import ast

#Imports for compiler
from controllers.com_initstrdict import initStringDict
from controllers.com_initvardict import initVariableDict

def handleDataBSS(asm, string_dict, var_dict):
    asm.write('bits 64\n')
    asm.write('default rel\n')
    asm.write('segment .bss\n')
    asm.write('segment .data\n')
    asm.write('format_result db "%d", 0\n')
    for key in string_dict:
        asm.write(string_dict[key]+' db "'+key+'", 0xd, 0xa, 0\n')
    for key in var_dict:
        #if variable name is integer
        if(var_dict[key].find('~') != 0):
            asm.write(key+' db "'+var_dict[key]+'", 0xd, 0xa, 0\n')
    for key in var_dict:
        if(var_dict[key].find('~') == 0):
            asm.write(key+' dd '+var_dict[key][1:]+'\n')

#Compiler
def compile(astree, file):
    file = os.path.splitext(file)[0]+'.asm'
    string_dict = {}
    var_dict = {}
    initStringDict(astree, string_dict)
    initVariableDict(astree, var_dict)
    with open(file, 'w') as asm:
        handleDataBSS(asm, string_dict, var_dict)
        asm.write('segment .text\n')
        asm.write('global main\n')
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
                    if(astree[x].getChild(y).getToken().getType() == Types.IDENTIFIER):
                        promenna = astree[x].getChild(y).getToken().getValue()
                        if(var_dict[promenna].find('~') == 0):
                            asm.write('lea rcx, [format_result]\n')
                            asm.write('mov rdx, ['+promenna+"]\n")
                            asm.write('call printf\n')
                        else:
                            asm.write('lea rcx, ['+promenna+']\n')
                            asm.write('call printf\n')
            if (astree[x].getToken().getType() == Types.IDENTIFIER and len(astree[x].children) > 1):
                promenna = astree[x].getToken().getValue()
                y = 0
                while y < len(astree[x].children):
                    if (astree[x].getChild(y).getToken().getValue() == "*"):
                        promenna = astree[x].getChild(y-1).getToken()
                        if(promenna.getType() == Types.IDENTIFIER):
                            asm.write('mov rbx, ['+promenna.getValue()+']\n')
                        if(promenna.getType() == Types.INTEGER):
                            asm.write('mov rbx, '+promenna.getValue()+'\n')
                        promenna = astree[x].getChild(y+1).getToken()
                        if(promenna.getType() == Types.IDENTIFIER):
                            asm.write('mov rax, ['+promenna.getValue()+']\n')
                        if(promenna.getType() == Types.INTEGER):
                            asm.write('mov rax, '+promenna.getValue()+'\n')
                        asm.write('mul rbx\n')
                    y+=1
                asm.write('mov ['+astree[x].getToken().getValue()+'], rax\n')
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
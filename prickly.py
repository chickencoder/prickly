#!/usr/bin/env python

# Prickly 0.1
# gitub.com/chickencoder/prickly
# a tiny python implementation of a
# forth-inspired language.

# Word operators to implement:
# negate
# abs
# max
# min
# dup
# swap
# rot
# drop
# wipe

import re

OPERS = ["+", "-", "*", "/", ".", ".s", "="]

def tokenize(code):
    # Tokenize splits code
    # into tokens (by whitespace)
    return code.split()

def lex(AST):
    # Lex determines the
    # types of tokens and returns
    # a simple AST
    LEXED_AST = []
    for token in AST:
        # Ignore Comments
        if token[0] != "#":
            # Is token INT
            if re.match("^[-]?\d+$", token):
                LEXED_AST.append(("INT", int(token)))

            # Is token OPER
            elif token in OPERS:
                LEXED_AST.append(("OPER", token))

            # Is token WORD
            elif re.match("^\w+$", token):
                LEXED_AST.append(("WORD", token))

    return LEXED_AST

class Stack:
    def __init__(self):
        self.stack = []

    def pop(self):
        if len(self.stack) > 0:
            return self.stack.pop()
        else:
            print("Stack Underflow Error")

    def push(self, val):
        self.stack.append(val)

class Interpreter:
    def __init__(self):
        self.stack = Stack()

    def displayStack(self):
        if self.stack != []:
            stck = ", ".join([ str(x) for x in self.stack.stack])
            return "(Top) %s <%d>" % (stck, len(self.stack.stack[:: -1]))
        else:
            return "EMPTY"

    def evaluate(self, code):
        tokens = tokenize(code)
        AST = lex(tokens)

        for token in AST:
            if token[0] == "INT":
                self.stack.push(token[1])

            elif token[0] == "OPER":
                if token[1] == "+":
                    a = self.stack.pop()
                    b = self.stack.pop()
                    if a and b:
                        self.stack.push(a + b)

                elif token[1] == "-":
                    a = self.stack.pop()
                    b = self.stack.pop()
                    if a and b:
                        self.stack.push(b - a)

                elif token[1] == "*":
                    a = self.stack.pop()
                    b = self.stack.pop()
                    if a and b:
                        self.stack.push(a * b)

                elif token[1] == "/":
                    a = self.stack.pop()
                    b = self.stack.pop()
                    if a and b:
                        self.stack.push(b / a)

                elif token[1] == ".":
                    return self.stack.pop()

                elif token[1] == ".s":
                    return self.displayStack()

                elif token[1] == "=":
                    a = self.stack.pop()
                    b = self.stack.pop()
                    if a and b:
                        if a == b:
                            return -1
                        else:
                            return 0

            elif token[0] == "WORD":
                if token[1] == "negate":
                    a = self.stack.pop()
                    if a:
                        self.stack.push(a*-1)

                elif token[1] == "abs":
                    a = self.stack.pop()
                    if a:
                        self.stack.push(abs(a))

                elif token[1] == "max":
                    a = self.stack.pop()
                    b = self.stack.pop()
                    if a and b:
                        self.stack.push(max(a, b))

                elif token[1] == "min":
                    a = self.stack.pop()
                    b = self.stack.pop()
                    if a and b:
                        self.stack.push(min(a, b))

                elif token[1] == "dup":
                    a = self.stack.pop()
                    if a:
                        self.stack.push(a)
                        self.stack.push(a)

                elif token[1] == "swap":
                    a = self.stack.pop()
                    b = self.stack.pop()
                    if a and b:
                        self.stack.push(a)
                        self.stack.push(b)

                elif token[1] == "rot":
                    a = self.stack.pop()
                    b = self.stack.pop()
                    c = self.stack.pop()
                    if a and b and c:
                        self.stack.push(a)
                        self.stack.push(b)
                        self.stack.push(c)

                elif token[1] == "drop":
                    self.stack.pop()

                elif token[1] == "wipe":
                    self.stack = Stack()

                else:
                    print("UNRECOGNIED WORD ", token[1])



    def interactive_mode(self):
        print("Prickly 0.1.2")
        running = True

        while running:
            user_inp = input("@ ")
            if user_inp != "exit":
                val = self.evaluate(user_inp)
                if val:
                    print(val)
                else:
                    print("OK")
            else:
                running = False

        print("Goodbye")

if __name__ == "__main__":
    i = Interpreter()
    i.interactive_mode()

import sys

from prompt_toolkit import print_formatted_text as printf

class Interpreter:
    def __init__(self, strict=False):
        self.strict = strict
        self.memory = [0] * 30_000
        self.pointer = 0

    def run(self, code: str):
        if not code:
            return

        current = 0
        while current < len(code):
            command = code[current]
            if command in "><+-.,":
                try:
                    self.process_command(command)
                except IndexError as error:
                    printf(f"Error at character {current}: {error}")
            if command == "[":
                if self.memory[self.pointer] == 0:
                    end = find_matching_bracket(code, current, close=True)
                    if end != -1:
                        current = end
                    else:
                        printf(f"Error at charater {current}: no matching bracket found")
            if command == "]":
                if self.memory[self.pointer] != 0:
                    start = find_matching_bracket(code, current, close=False)
                    if start != -1:
                        current = start
                    else:
                        printf(f"Error at charater {current}: no matching bracket found")
            current += 1


    def process_command(self, command):
        if command == ">":
            if self.strict and self.pointer >= 30_000:
                raise IndexError("Pointer too big")
            self.pointer += 1
            return
        if command == "<":
            if self.strict and self.pointer <= 0:
                raise IndexError("Pointer can't be negative")
            self.pointer -= 1
            return
        if command == "+":
            self.memory[self.pointer] += 1
            return
        if command == "-":
            self.memory[self.pointer] -= 1
            return
        if command == ".":
            printf(chr(self.memory[self.pointer]), end="")
            return
        if command == ",":
            self.read_byte()

    def read_byte(self):
        byte = sys.stdin.buffer.read()
        self.memory[self.pointer] = byte


def find_matching_bracket(code, start, close):
    if close:
        if start < len(code) - 1:
            found = 1
            current = start + 1
            while found and current < len(code):
                if code[current] == "[":
                    found += 1
                if code[current] == "]":
                    found -= 1
                current += 1
            return current - 1
    elif start > 1:
        found = 1
        current = start - 1
        while found and current > -1:
            if code[current] == "]":
                found += 1
            if code[current] == "[":
                found -= 1
            current -= 1
        return current + 1
    return -1

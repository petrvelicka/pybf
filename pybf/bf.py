import sys

class Interpreter:
    def __init__(self):
        self.memory = [0] * 30_000
        self.pointer = 0
    
    def run(self, code: str):
        if not code:
            return
        
        current = 0
        while current < len(code):
            command = code[current]
            if command in "><+-.,":
                self.process_command(command)
            if command == "[":
                if self.memory[self.pointer] == 0:
                    end = find_matching_bracket(code, current, close=True)
                    current = end            
            if command == "]":
                if self.memory[self.pointer] != 0:
                    start = find_matching_bracket(code, current, close=False)
                    current = start
            current += 1


    def process_command(self, command):
        if command == ">":
            self.pointer += 1
            return
        if command == "<":
            self.pointer -= 1
            return
        if command == "+":
            self.memory[self.pointer] += 1
            return
        if command == "-":
            self.memory[self.pointer] -= 1
            return
        if command == ".":
            print(chr(self.memory[self.pointer]), end="")
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
        return -1
    if start > 1:
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

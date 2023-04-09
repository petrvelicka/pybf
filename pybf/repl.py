import argparse
import sys
from pathlib import Path

import bf

from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit import PromptSession
from prompt_toolkit import print_formatted_text as print

def setup_args():
    parser = argparse.ArgumentParser(prog="pybf", description="Yet another BrainFuck interpreter")
    parser.add_argument("-c", "--check", action="store_true", help="only checks code for correctness, doesn't execute anything")
    parser.add_argument("-s", "--strict", action="store_true", help="check bounds while executing")
    parser.add_argument("path", nargs='?', help="input file for interpreting")
    
    return parser.parse_args()

def check_parentheses(string):
    for index, character in enumerate(string):
        if character == "[":
            close = bf.find_matching_bracket(string, index, close = True)
            if close == -1:
                return False, index
        if character == "]":
            start = bf.find_matching_bracket(string, index, close = False)
            if close == -1:
                return False, index
    return True, -1

def repl(strict_mode):
    interpreter = bf.Interpreter(strict=strict_mode)
    session = PromptSession()
    patch_stdout()
    while True:
        try:
            _in = session.prompt("> ").strip()
            if _in == "exit":
                return
            if _in == "reset":
                print("Resetting the interpreter...")
                interpreter = bf.Interpreter()
                continue
            while not check_parentheses(_in)[0]:
                _in += session.prompt(". ").strip()
            interpreter.run(_in)
            print()
        except KeyboardInterrupt:
            print("^C pressed...")
        except EOFError:
            print("^D pressed...")
            return


if __name__ == "__main__":
    args = setup_args()
    strict_mode = args.strict
    if strict_mode:
        print("Warning, strict mode enabled..")
    if args.path:
        path = Path(args.path)
        if not path.exists() and not path.is_dir():
            print(f"Error: {path}: file not found")
            sys.exit(-1)
        file = open(path, "r").read()
        if args.check:
            print("Check only mode...")
            result = check_parentheses(file)
            if result[0] == False:
                print(f"Error: mismatched parenthesis found at character {result[1]}")
            sys.exit(0)
        interpreter = bf.Interpreter(strict_mode)
        interpreter.run(file)
        print()
    else:
        if not args.check:
            print("Starting REPL, type exit or ^D to exit")
            repl(strict_mode)
        else:
            print("Unexpected parameter -c, only applies to file mode")

import argparse
import sys
from pathlib import Path

from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit import PromptSession
from prompt_toolkit import print_formatted_text as printf

import bf

def setup_args():
    parser = argparse.ArgumentParser(prog="pybf", description="Yet another BrainFuck interpreter")
    parser.add_argument("-c", "--check", action="store_true",
                        help="only checks code for correctness, doesn't execute anything")
    parser.add_argument("-s", "--strict", action="store_true", help="check bounds while executing")
    parser.add_argument("-o", "--output", help="file for outputting, only in file interpret mode")
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
            if start == -1:
                return False, index
    return True, -1

def repl(strict_mode):
    repl_interpreter = bf.Interpreter(strict=strict_mode)
    session = PromptSession()
    patch_stdout()
    while True:
        try:
            _in = session.prompt("> ").strip()
            if _in == "exit":
                return
            if _in == "reset":
                printf("Resetting the interpreter...")
                repl_interpreter = bf.Interpreter()
                continue
            while not check_parentheses(_in)[0]:
                printf(check_parentheses(_in))
                _in += session.prompt(". ").strip()
            repl_interpreter.run(_in)
            printf()
        except KeyboardInterrupt:
            printf("^C pressed...")
        except EOFError:
            printf("^D pressed...")
            return


if __name__ == "__main__":
    args = setup_args()
    strict = args.strict
    if strict:
        printf("Warning, strict mode enabled..")
    if args.path:
        path = Path(args.path)
        if not path.exists() and not path.is_dir():
            printf(f"Error: {path}: file not found")
            sys.exit(-1)
        with open(path, "r", encoding="utf-8") as file_handler:
            file = file_handler.read()
            if args.check:
                printf("Check only mode...")
                result = check_parentheses(file)
                if not result[0]:
                    printf(f"Error: mismatched parenthesis found at character {result[1]}")
                sys.exit(0)
            output_file = args.output
            interpreter = bf.Interpreter(strict, output=output_file)
            interpreter.run(file)
            printf()
    else:
        if not args.check:
            printf("Starting REPL, type exit or ^D to exit")
            repl(strict)
        else:
            printf("Unexpected parameter -c, only applies to file mode")

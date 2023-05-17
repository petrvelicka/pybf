import bf
import pytest

def test_hello_world(capsys):
    code = """
    >++++++++[<+++++++++>-]<.>++++[<+++++++>-]<+.+++++++..+++.>>++++++[<+++++++>-]<+
    +.------------.>++++++[<+++++++++>-]<+.<.+++.------.--------.>>>++++[<++++++++>-
    ]<+.
    """
    interpreter = bf.Interpreter(strict=True)
    interpreter.run(code)
    captured = capsys.readouterr()
    assert captured.out == "Hello, World!"

def test_strict(capsys):
    code = "<"
    interpreter = bf.Interpreter(strict=True)
    interpreter.run(code)
    captured = capsys.readouterr()
    expected = "Error at character 0: Pointer can't be negative\r\n"
    assert captured.err == expected

def test_unmatched_parenthesis(capsys):
    code = ">>[++--"
    interpreter = bf.Interpreter(strict=True)
    interpreter.run(code)
    captured = capsys.readouterr()
    expected = "Error at charater 2: no matching bracket found\n"
    assert captured.err == expected


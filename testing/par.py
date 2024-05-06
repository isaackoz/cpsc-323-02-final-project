from collections import defaultdict
from typing import List, Type
from typing import Set

# Define all the terminal values
reserve = ["program", "var", "begin", "end.", "integer", "write"]
terminals = [":", ";", "=", "+", "-", "*", "/", "(", ")", ",", '"value="', "$"]
letter = "pqrs"

# Define the transition table
predParse = defaultdict(lambda: defaultdict(lambda: Type[list[str]]))
predParse["<prog>"]["program"] = ["program", "<identifier>", ";", "var", "<dec-list>", "begin", "<stat-list>", "end."]
predParse["<dec-list>"]["<identifier>"] = ["<dec>", ":", "<type>", ";"]
predParse["<dec>"]["<identifier>"] = ["<identifier>", "<dec-tail>"]
predParse["<dec-tail>"][","] = [",", "<dec>"]
predParse["<dec-tail>"][":"] = ["lambda"]
predParse["<type>"]["integer"] = ["integer"]
predParse["<stat-list>"]["write"] = ["<stat-action>", "<stat-list-tail>"]
predParse["<stat-list>"]["<identifier>"] = ["<stat-action>", "<stat-list-tail>"]
predParse["<stat-list-tail>"]["end."] = ["lambda"]
predParse["<stat-list-tail>"]["write"] = ["<stat-list>"]
predParse["<stat-list-tail>"]["<identifier>"] = ["<stat-list>"]
predParse["<stat-action>"]["write"] = ["<write>"]
predParse["<stat-action>"]["<identifier>"] = ["<assign>"]
predParse["<write>"]["write"] = ["write", "(", "<str>", "<identifier>", ")", ";"]
predParse["<str>"]["<identifier>"] = ["lambda"]
predParse["<str>"]['"value="'] = ['"value="', ","]
predParse["<assign>"]["<identifier>"] = ["<identifier>", "=", "<expr>", ";"]
predParse["<expr>"]["<identifier>"] = ["<term>", "<expr-tail>"]
predParse["<expr>"]["<number>"] = ["<term>", "<expr-tail>"]
predParse["<expr>"]["("] = ["<term>", "<expr-tail>"]
predParse["<expr-tail>"][")"] = ["lambda"]
predParse["<expr-tail>"]["+"] = ["+", "<term>", "<expr-tail>"]
predParse["<expr-tail>"]["-"] = ["-", "<term>", "<expr-tail>"]
predParse["<expr-tail>"][";"] = ["lambda"]
predParse["<term>"]["<identifier>"] = ["<factor>", "<term-tail>"]
predParse["<term>"]["<number>"] = ["<factor>", "<term-tail>"]
predParse["<term>"]["("] = ["<factor>", "<term-tail>"]
predParse["<term-tail>"][")"] = ["lambda"]
predParse["<term-tail>"]["+"] = ["lambda"]
predParse["<term-tail>"]["-"] = ["lambda"]
predParse["<term-tail>"]["*"] = ["*", "<factor>", "<term-tail>"]
predParse["<term-tail>"]["/"] = ["/", "<factor>", "<term-tail>"]
predParse["<term-tail>"][";"] = ["lambda"]
predParse["<factor>"]["<identifier>"] = ["<identifier>"]
predParse["<factor>"]["<number>"] = ["<number>"]
predParse["<factor>"]["("] = ["(", "<expr>", ")"]


def parseIdNums(tokens: List[str]):
    identifiers = set()  # set of identifiers
    numbers = set()  # set of numbers
    valid = True  # whether the tokens are valid
    for token in tokens:
        if token not in reserve and token not in terminals:
            firstChar = token[0]
            if firstChar in letter:
                # Do identifier checks
                validTok = True
                for char in token[1:]:  # check if the rest of the chars are allowed
                    if not (char.isnumeric() or char in letter):
                        print(f"Char {char} is not allowed in identifier {token}")
                        validTok = False
                if validTok:
                    identifiers.add(token)
                else:
                    print(f"Invalid token: {token}")
                    valid = False
            elif firstChar.isdigit() or firstChar == "-" or firstChar == "+":
                # Do number checks
                validTok = True
                for char in token[1:]:  # check if the rest of the chars are allowed
                    if not char.isnumeric():
                        print(f"Char {char} is not allowed in number {token}")
                        validTok = False
                if validTok:
                    numbers.add(token)
                else:
                    print(f"Invalid token: {token}")
                    valid = False
            else:
                print(f"Invalid token: {token}")
                valid = False
    return valid, identifiers, numbers


def debug_print(stack: List[str], input: List[str], currentTok: str):
    print(f"Stack:            {stack}")
    print(f"Remaining Tokens: {input}")
    print(f"Current Token:    {currentTok}")
    print("")



def parseTok(tokens: List[str], identifiers: Set[str], numbers: Set[str], debug: bool = False):
    progName = ""
    decVars = []
    operations = []
    decMode = False
    declared = False

    if "end." not in tokens:
        print("'end.' is missing")
        return False, decVars, operations, progName

    stack = ["$", "<prog>"]
    input = tokens.copy()
    input.append("$")
    currentTok = None
    currentOp = []
    inOp = False
    if debug:
        debug_print(stack, input, currentTok)
    while len(stack) > 0 or len(input) > 0:
        state = stack.pop()
        if state == "<write>" or state == "<assign>":  # if we are in a write or an assign statement
            inOp = True  # we are in an operation
            currentOp = [currentTok]
        if not currentTok:
            currentTok = input.pop(0)
            if inOp and currentTok == ";":  # if we are in an operation and the current token is a semicolon
                inOp = False  # we are not in an operation
                operations.append(currentOp)
            elif inOp:
                currentOp.append(currentTok)

        if state == "<identifier>":
            if currentTok in identifiers:
                if decMode:
                    decVars.append(currentTok)
                elif declared:
                    if currentTok not in decVars:
                        print(f"Variable '{currentTok}' not declared")
                        break
                else:
                    progName = currentTok
                currentTok = None
            else:
                print(f"Expected identifier, got {currentTok}")
                break
        elif state == "<number>":
            if currentTok in numbers:
                currentTok = None
            else:
                print(f"Expected number, got {currentTok}")
                break
        elif state in terminals:
            if state == currentTok:
                currentTok = None
            else:
                print(f"Expected '{state}', got {currentTok}")
                break
        elif state in reserve:
            if state == currentTok:
                currentTok = None
            else:
                print(f"Expected '{state}', got {currentTok}")
                break
            if state == "var":
                decMode = True
            elif state == "begin":
                decMode = False
                declared = True
        elif state == "lambda":
            continue
        else:
            if currentTok in identifiers:
                parseTok = "<identifier>"
            elif currentTok in numbers:
                parseTok = "<number>"
            else:
                parseTok = currentTok
            result = predParse[state][parseTok]
            if result is None:
                expected = list(predParse[state])
                expected.remove(parseTok)
                expected = " or ".join(expected)
                print(f"Expected {expected}, got {currentTok}")
                break
            elif isinstance(result, list):
                stack += reversed(result)
            else:
                print(f"Unknown Result from predParse: {result}")
                break
        if debug:
            if currentTok is None:
                print("MATCH")
            debug_print(stack, input, currentTok)
    accepted = len(stack) == 0 and len(input) == 0 and not currentTok
    return accepted, decVars, operations, progName

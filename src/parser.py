from parseTable import parse_table
from translator import CodeGenerator
import re
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Lexer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.tokens = []
        self.current_token_index = 0
        self.tokenize()

    def tokenize(self):
        with open(self.filepath, 'r') as file:
            content = file.read()

        words = content.split()
        reserve_words = {'program', 'var', 'begin', 'end.', 'write', 'integer'}
        symbols = {';', '=', '+', '*', '(', ')', ',', ':', '.'}

        for word in words:
            if word in reserve_words:
                self.tokens.append(Token('KEYWORD', word))
            elif word in symbols:
                self.tokens.append(Token('SYMBOL', word))
            elif word.isdigit():
                # Here, instead of adding the whole number, add each digit as a separate token
                for digit in word:
                    self.tokens.append(Token('NUMBER', digit))
            elif word.startswith('"') and word.endswith('"'):
                self.tokens.append(Token('STRING', word))
            else:
                # Non-reserved words are split into individual character tokens, digits treated separately
                for char in word:
                    if char.isdigit():
                        self.tokens.append(Token('NUMBER', char))
                    else:
                        self.tokens.append(Token('IDENTIFIER', char))

    def next_token(self):
        if self.current_token_index < len(self.tokens):
            token = self.tokens[self.current_token_index]
            self.current_token_index += 1
            return token
        else:
            return Token('EOF', None)

    def reset(self):
        self.current_token_index = 0
class Parser:
    def __init__(self, lexer, code_gen):
        self.lexer = lexer
        self.current_token = None
        self.code_generator = code_gen
        self.parse_table = parse_table
        self.stack = ['EOF', 'S']
        self.token_buffer = []
        self.inVar = False
        self.inMain = False
        self.inWrite = False

    def parse(self):
        self.current_token = self.lexer.next_token()
        while self.stack:
            top = self.stack.pop()
            if isinstance(top, str) and (top == self.current_token.value or top == self.current_token.type):
                if top == 'EOF':
                    return
                self.execute_actions(top, self.current_token)
                self.current_token = self.lexer.next_token()
            elif self.is_non_terminal(top):
                self.handle_non_terminal(top)
            else:
                raise Exception(
                    f"Syntax error: unexpected token {self.current_token.type} ({self.current_token.value}). Expected {top}")

    def execute_actions(self, top, token):
        # Example: Add variable declaration to code generator
        if token.type == "KEYWORD":
            if token.value == "var":
                self.inVar = True
                return
            elif token.value == "integer":
                pass
            elif token.value == "begin":
                # If we are in the main code block, set isMain to true
                self.inMain = True
                return
        if self.inVar:
            if token.value == ':':
                self.inVar = False
                var_names = '='.join(''.join(self.token_buffer).split(','))
                self.code_generator.add_code(f"{var_names} = 0")
                self.token_buffer = []
            else:
                # If we're declaring variable, build the var buffer
                self.token_buffer.append(top)
        elif self.inMain:
            if token.value == ';':
                if self.inWrite:
                    self.inWrite = False
                statement = ''.join(self.token_buffer)
                self.code_generator.add_code(statement)
                self.token_buffer = []
            elif token.value == 'write':
                self.inWrite = True
                self.token_buffer.append("print")
            else:
                self.token_buffer.append(token.value)

    def handle_non_terminal(self, non_terminal):
        key = (non_terminal, self.current_token.value)
        if key in self.parse_table:
            rule = self.parse_table[key]
            if rule == []:
                return  # Handle λ production
            for symbol in reversed(rule):
                self.stack.append(symbol)
        else:
            # Gather expected tokens for the current non-terminal from the parse table
            expected_tokens = []
            for k, v in self.parse_table.items():
                if k[0] == non_terminal:
                    expected_tokens.append(k[1])

            # If there are expected tokens, format them into a readable string
            if expected_tokens:
                expected_str = ", ".join(expected_tokens)
                raise Exception(
                    f"Syntax error: No rule for {non_terminal} with lookahead {self.current_token.value}. Expected: {expected_str}")
            else:
                raise Exception(
                    f"Syntax error: No rule for {non_terminal} with lookahead {self.current_token.value}. No expected tokens found.")

    def is_non_terminal(self, symbol):
        return any(symbol == key[0] for key in self.parse_table.keys())


if __name__ == "__main__":
    my_lexer = Lexer('./output/formatted.txt')
    code_gen = CodeGenerator()
    parser = Parser(my_lexer, code_gen)
    try:
        parser.parse()
        print("Parsing completed successfully!")
        code_gen.generate_code()
    except Exception as e:
        print(f"An error occurred during parsing: {e}")
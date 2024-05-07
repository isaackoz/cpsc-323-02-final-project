from parseTable import parse_table
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
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None
        self.parse_table = parse_table
        self.stack = ['EOF', 'S']

    def parse(self):
        self.current_token = self.lexer.next_token()
        while self.stack:
            top = self.stack.pop()
            if isinstance(top, str) and (top == self.current_token.value or top == self.current_token.type):
                if top == 'EOF':
                    print("Parsing successful!")
                    return
                self.current_token = self.lexer.next_token()
            elif self.is_non_terminal(top):
                self.handle_non_terminal(top)
            else:
                raise Exception(
                    f"Syntax error: unexpected token {self.current_token.type} ({self.current_token.value}). Expected {top}")

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
                if k[0] == non_terminal:  # Filter by the non-terminal part of the key
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
    lexer = Lexer('./output/formatted.txt')
    for token in lexer.tokens:  # Print all tokens to inspect them
        print(token)
    parser = Parser(lexer)
    try:
        parser.parse()
        print("Parsing completed successfully!")
    except Exception as e:
        print(f"An error occurred during parsing: {e}")
from parseTable import parse_table

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
        for word in words:
            if word in {'program', 'var', 'begin', 'end', 'write', 'integer'}:
                self.tokens.append(Token('KEYWORD', word))
            elif word in {';', '=', '+', '*', '(', ')', ',', ':', '.'}:
                self.tokens.append(Token('SYMBOL', word))
            elif word.isdigit():
                self.tokens.append(Token('NUMBER', word))
            elif word.startswith('"') and word.endswith('"'):
                self.tokens.append(Token('STRING', word))
            else:
                self.tokens.append(Token('IDENTIFIER', word))

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
            if top == self.current_token.type or top == self.current_token.value:
                if top == 'EOF':
                    print("Parsing successful!")
                    return
                self.current_token = self.lexer.next_token()
            elif self.is_non_terminal(top):
                self.handle_non_terminal(top)
            else:
                raise Exception(f"Syntax error: unexpected token {self.current_token.type}.")

    def handle_non_terminal(self, non_terminal):
        key = (non_terminal, self.current_token.type)
        if key in self.parse_table:
            rule = self.parse_table[key]
            if rule == []:
                return  # Handle λ production
            for symbol in reversed(rule):
                self.stack.append(symbol)
        else:
            raise Exception(f"Syntax error: No rule for {non_terminal} with lookahead {self.current_token.type}.")

    def is_non_terminal(self, symbol):
        # This method should return True if the symbol is a non-terminal
        return symbol in self.parse_table  # This might need adjustment to check keys correctly.



if __name__ == "__main__":
    lexer = Lexer('./output/formatted.txt')
    parser = Parser(lexer)
    try:
        parser.parse()
        print("Parsing completed successfully!")
    except Exception as e:
        print(f"An error occurred during parsing: {e}")
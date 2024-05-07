class CodeGenerator:
    def __init__(self):
        self.output_code = []

    def add_code(self, code_line):
        self.output_code.append(code_line)

    def generate_code(self):
        # Here you might add additional processing before writing to file
        with open('./output/output.py', 'w') as f:
            for line in self.output_code:
                f.write(f"{line}\n")

    def print_code(self):
        for line in self.output_code:
            print(line)

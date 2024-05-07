
from formatter import FormatProgram
from parser import Parser, Lexer
from translator import CodeGenerator


# Main -- This file runs all 3 steps in order to produce the final output
# There are 3 steps to complete our compiler
# 1. Format the file to remove comments, extra lines, and add spaces between terminals
#   -> formatter.py
# 2. Use a predictive parsing table to ensure our program has the correct grammar
#   -> parser.py
# 3. Translate the program into a .py file
#   -> translator.py
#

def main():
    # The file name for the original program
    og_program_filename = "./input/finalv1.txt"

    # Step 1 - Format file
    try:
        print("Formatting file: ", og_program_filename)
        formatter = FormatProgram(og_program_filename)
        # This will output a file formatted.txt under ./output
        formatter.save_formatted_file()
        print("Formatted file and saved it to ./output/final24.txt")
        print("---")
    except Exception as e:
        print(f"There was an error during formatting: {e}")

    # Step 2 & 3 - Parse and generate the code
    my_lexer = Lexer('./output/final24.txt')
    code_gen = CodeGenerator()
    parser = Parser(my_lexer, code_gen)
    try:
        print("Parsing...")
        parser.parse()
        print("Parsing completed successfully with no errors!")
        print("---")
        print("Generating code...")
        code_gen.generate_code()
        print("Code generated and saved to ./output/output.py")
    except Exception as e:
        print(f"An error occurred during parsing: {e}")



if __name__ == '__main__':
    main()
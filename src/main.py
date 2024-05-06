
from formatter import FormatProgram
from parser import Parser
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
    og_program_filename = "finalv1.txt"

    # Step 1
    formatter = FormatProgram(og_program_filename)
    # This will output a file formatted.txt under ./output
    formatter.save_formatted_file()

    # Step 2
    lr_parser = Parser('./output/formatted.txt')




if __name__ == '__main__':
    main()
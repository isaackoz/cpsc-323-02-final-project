import re

#
# This class will take in a .txt file and format it with the following rules
# 1. Any line that begins with // and ends at // are considered as a comment line(s)
#     remove them all.
# 2. Remove all blank line(s)
# 3. Extra spaces in each line must be removed, leave one space before and one after
#     each token to make tokenization easier.
class FormatProgram:
    def __init__(self, filepath):
        self.filepath = filepath

    def format_file(self):
        formatted_text = ""
        in_comment = False
        in_quotes = False
        quote_char = ''
        previous_char = ''

        with open(self.filepath, 'r', encoding='utf-8') as file:
            while True:
                char = file.read(1)
                if not char:
                    break  # End of file

                # Check if entering or exiting quotes
                if char in "\"'“”" and not in_comment:
                    if in_quotes:
                        if char == quote_char:
                            in_quotes = False  # Closing quote
                    else:
                        in_quotes = True
                        quote_char = char
                    formatted_text += char
                    continue

                # Handle comments
                if char == '/' and not in_quotes:
                    next_char = file.read(1)
                    if next_char == '/':
                        if not in_comment:
                            in_comment = True
                            # Skip until end of line or end comment sequence
                            while True:
                                temp_char = file.read(1)
                                if temp_char == '\n':
                                    in_comment = False
                                    formatted_text += ' '  # To ensure newline is processed if needed
                                    break
                                if not temp_char:
                                    break  # End of file
                        continue
                    else:
                        formatted_text += char + next_char
                        continue
                elif in_comment:
                    continue

                # Normalize spaces
                if char.isspace():
                    if previous_char != ' ' and formatted_text and not formatted_text[-1].isspace():
                        formatted_text += ' '
                else:
                    formatted_text += char

                previous_char = char

        return formatted_text

    def save_formatted_file(self):
        formatted_text = self.format_file()
        with open(self.filepath.replace('.txt', '_formatted.txt'), 'w', encoding='utf-8') as file:
            file.write(formatted_text)


# Example usage
formatter = FormatProgram('finalv1.txt')
formatter.save_formatted_file()

# Todo: Create a class that will read the formatted file from FormatProgram and LL parse it (predictive parsing)

# Todo: Create a class that will convert the formatted file to a .py file

# Todo: Test the file and ensure it runs
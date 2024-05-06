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
        processed_content = ''

        with open(self.filepath, 'r', encoding='utf-8') as file:
            content = file.read()

        i = 0
        terminals = {';', ':', '*', '+', '-', '/', '=', '(', ')', ','}
        while i < len(content):
            char = content[i]

            # Handle entering and exiting quotes
            if char in "\"'“”":
                if in_quotes:
                    if char == quote_char:
                        in_quotes = False  # Closing quote
                    processed_content += char  # Add the closing quote character
                else:
                    in_quotes = True
                    quote_char = char  # Set the type of quote we're in
                    processed_content += char  # Add the opening quote character
                i += 1
                continue

            if in_quotes:
                processed_content += char  # Continue adding text inside quotes
                i += 1
                continue

            # Detect and manage comments
            if char == '/' and not in_quotes and i + 1 < len(content) and content[i + 1] == '/':
                if not in_comment:
                    in_comment = True
                else:
                    in_comment = False
                i += 2  # Skip both slashes
                continue

            if not in_comment:
                if char in terminals:
                    # Add space before and after the terminal if not at start or end of the line
                    if processed_content and not processed_content.endswith(' '):
                        processed_content += ' '
                    processed_content += char
                    if i + 1 < len(content) and content[i + 1] not in terminals and content[i + 1] != ' ':
                        processed_content += ' '
                else:
                    processed_content += char

            i += 1

        # Split the processed content into lines and remove any empty lines
        lines = processed_content.split('\n')
        for line in lines:
            if line.strip():  # Only add non-empty lines
                formatted_text += line.strip() + '\n'

        return formatted_text.strip()

    def save_formatted_file(self):
        formatted_text = self.format_file()
        with open('./output/' + 'formatted.txt', 'w', encoding='utf-8') as file:
            file.write(formatted_text)


def main():
    # Example usage
    print("Formatting file...")
    formatter = FormatProgram('./finalv1.txt')
    formatter.save_formatted_file()
    print("File successfully formatted and saved.")


if __name__ == '__main__':
    main()
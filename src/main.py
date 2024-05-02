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
        formatted_lines = []
        in_comment = False  # Flag to track whether we're inside a multi-line comment block

        with open(self.filepath, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for line in lines:
            original_line = line.strip()
            if not original_line:
                continue

            if '//' in original_line:
                parts = original_line.split('//')
                if in_comment:
                    if original_line.endswith('//'):
                        in_comment = False
                        if len(parts) > 1 and not original_line.endswith('//'):
                            after_comment = parts[-1]
                            if after_comment:
                                formatted_lines.append(self.format_line(after_comment))
                    continue
                else:
                    start_comment_index = original_line.find('//')
                    end_comment_index = original_line.rfind('//') + 2
                    if end_comment_index > start_comment_index + 2:
                        before_comment = original_line[:start_comment_index].strip()
                        after_comment = original_line[end_comment_index:].strip()
                        if before_comment:
                            formatted_lines.append(self.format_line(before_comment))
                        if after_comment:
                            formatted_lines.append(self.format_line(after_comment))
                        continue
                    else:
                        in_comment = True
                        before_comment = original_line[:start_comment_index].strip()
                        if before_comment:
                            formatted_lines.append(self.format_line(before_comment))
                        continue

            if in_comment:
                continue

            formatted_lines.append(self.format_line(original_line))

        return formatted_lines

    def format_line(self, line):
        # Process the line to correctly format it except within quotes
        parts = re.split(r'("[^"]*"|\'[^\']*\')', line)  # Split by quoted text
        new_line = []
        for part in parts:
            if part.startswith('"') or part.startswith("'"):  # Maintain quoted text as is
                new_line.append(part)
            else:
                # Replace multiple spaces with a single space and space around operators/characters
                part = re.sub(r'\s+', ' ', part)
                part = re.sub(r'(\S)([,:;(){}])', r'\1 \2', part)
                part = re.sub(r'([,:;(){}])(\S)', r'\1 \2', part)
                new_line.append(part)
        return ''.join(new_line).strip()

    def save_formatted_file(self):
        formatted_lines = self.format_file()
        with open(self.filepath.replace('.txt', '_formatted.txt'), 'w', encoding='utf-8') as file:
            file.write("\n".join(formatted_lines))

# Example usage
formatter = FormatProgram('finalv1.txt')
formatter.save_formatted_file()

# Todo: Create a class that will read the formatted file from FormatProgram and LL parse it (predictive parsing)

# Todo: Create a class that will convert the formatted file to a .py file

# Todo: Test the file and ensure it runs

from makepy import makePy
from par import parseIdNums
from par import parseTok
from typing import List

DEBUG = False

# fix file function
def fixFile(lines: List[str]) -> List[List[str]]:

    cleaned = []
    inComment = False
    for line in lines:
        lineParts = line.strip().split(" ")  # Remove whitespace and split by spaces
        cleanedLine = []
        for part in lineParts:
            if not inComment and "//" in part:  # If we're not in a comment and we find a comment start
                inComment = True  # We're now in a comment
                continue
            if inComment and "//" in part:  # If we're in a comment and we find a comment end
                inComment = False  # We're no longer in a comment
                continue
            if inComment:
                continue
            if len(part) == 0 or part.isspace():  # If the part is empty or whitespace continue
                continue
            cleanedLine.append(part)
        if len(cleanedLine) > 0:
            cleaned.append(cleanedLine)

    charSeperate = ["(", ")", ";", ",", ":"]

    verified = False

    while not verified:
        verified = True
        for line in cleaned:
            spaced = []
            for token in line:
                modified = False
                if len(token) > 1:
                    for char in charSeperate:
                        if not modified and char in token:
                            verified = False
                            modified = True
                            token = token.replace(char, " " + char + " ")  # Add whitespace around the char
                            seperated = token.split()  # Separate the token
                            seperated = [x.strip() for x in seperated]  # Remove whitespace
                            while "" in seperated:
                                seperated.remove("")
                            spaced += seperated
                if not modified:
                    spaced.append(token)
            line[:] = spaced  # Replace the old line with the new line

    return cleaned


def main():

    # Change directory as needed
    # Get the filename
    filename = "C:\\Users\\baldo\\Desktop\\PyProjects\\comp3\\finalv1.txt"

    # Read the file
    try:
        file = open(filename)
        lines = file.read().splitlines()
        file.close()
    except FileNotFoundError:
        print(f"File {filename} not found")
        return

    # fix the file
    cleaned = fixFile(lines)

    # Save the cleaned input
    with open("finalf24.txt", "w") as file:
        file.write("\n".join([" ".join(line) for line in cleaned]))


    # Turn the 2D list into a 1D list of tokens
    tokens = []
    for line in cleaned:
        tokens += line
    
    # output to check for proper tokens
    print(tokens)

    # Get the identifiers and numbers from the tokens
    valid, identifiers, numbers = parseIdNums(tokens)

    if DEBUG:
        print("Tokens:", tokens)
        print("Identifiers:", identifiers)
        print("Numbers", numbers)

    # If any of the identifiers or numbers are invalid, print an error message
    if not valid:
        print("REJECTED: Invalid input")
        return

    # Parse the whole program
    valid, variables, operations, progName = parseTok(tokens, identifiers, numbers, DEBUG)

    if DEBUG:
        print("Variables:", variables)
        print("Stats:", operations)

    # If the program is invalid, print an error message
    if not valid:
        print("REJECTED: Invalid input")
        return

    # Generate the python program
    makePy("finalf24.py", variables, operations, progName)


if __name__ == "__main__":
    main()

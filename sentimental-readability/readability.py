import re

#get user input
def main():
    userInput = input("Text: ")
    output = readability(userInput)
    output = round(output)
    if output < 1:
        print("Before Grade 1")
    elif output >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {output}")


def readability(string):
    regexSentence = "\.|\?|\!"
    numberOfSentences = len(re.findall(regexSentence, string))
    regexWords = "\S+"
    regexLetters = "\w"
    numberOfWords = len(re.findall(regexWords, string))
    numberOfLetters = len(re.findall(regexLetters, string))

    #coleman-liau formula
    output = (0.0588 * (numberOfLetters / numberOfWords) * 100) - 0.296 * (numberOfSentences / (numberOfWords) * 100) - 15.8
    return output


main()
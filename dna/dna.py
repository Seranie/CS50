import csv
import sys


def main():

    # TODO: Check for command-line usage
    if(len(sys.argv) == 3):
        argv = sys.argv
    else:
        print("Invalid argument")
        return
    # TODO: Read database file into a variable
    file_database = argv[1]
    database = open(file_database, "r")
    databaseDict = csv.DictReader(database)
    # TODO: Read DNA sequence file into a variable
    file_sequence = argv[2]
    sequence = open(file_sequence, "r")
    sequenceString = sequence.read()
    # TODO: Find longest match of each STR in DNA sequence
    fieldnames = databaseDict.fieldnames
    longestStr = {}
    numberOfFields = len(fieldnames)
    for k in range(1, numberOfFields):
        longest = longest_match(sequenceString, fieldnames[k])
        fieldname = fieldnames[k]
        longestStr[fieldname] = str(longest)


    # TODO: Check database for matching profiles
    for reader in databaseDict:
        counter = 0
        for i in range(1, numberOfFields):
            if reader[fieldnames[i]] == longestStr[fieldnames[i]]:
                counter += 1
        if counter == numberOfFields - 1:
            name = reader['name']
            print(f"{name}")
            return

    print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()

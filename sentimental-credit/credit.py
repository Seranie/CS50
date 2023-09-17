def main():
    userInput = input("What is your credit card number? ")
    splitInput = list(userInput)
    sum = creditCheck(splitInput)
    length = len(userInput)
    if (sum % 10) == 0:
        match length:
            case 15:
                if splitInput[0:2] == ['3','4'] or splitInput[0:2] == ['3','7']:
                    print("AMEX")
                else:
                    print("INVALID")
            case 13:
                print("VISA")
            case 16:
                if splitInput[0] == '4':
                    print("VISA")
                elif splitInput[0] == '5' and (int(splitInput[1]) <=5 and int(splitInput[1]) >= 1):
                    print("MASTERCARD")
                else:
                    print("INVALID")
            case _:
                print("INVALID")
    else:
        print("INVALID")


def creditCheck(splitInput):
    length = len(splitInput)
    splitInput = splitInput[::-1]
    for k in range(length):
        splitInput[k] = int(splitInput[k])
    for i in range(0, length, 2):
        if (i + 1) <= length - 1:
            splitInput[i + 1] = splitInput[i + 1] * 2
            if splitInput[i + 1] >= 10:
                tempInput = str(splitInput[i + 1])
                tempList = list(tempInput)
                splitInput[i + 1] = int(tempList[0]) + int(tempList[1])
    return sum(splitInput)


main()
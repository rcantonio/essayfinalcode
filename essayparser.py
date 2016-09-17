'''
Essay Parser
Version 1.00
Authors: Antonio, Davila, Greene
Last updated: 09/17/16

Note: Code must be executed on python 3.5.xx only
'''

# for clear screen function
import os
# to determine the user's OS
from sys import platform
def main():
    active = True
    punctuations = [".", ",", ";", ":", "?", "!"]
	# default wordlength for valid words is 3
    wordLength = 3 
    f = None 
    while active:
        choice = menu()
        clearScreen()
		# exit program
        if choice == 8:
            active = False
		# specify inpuy file
        elif choice == 1:
            f = openFile()
		# compute for average length
        elif choice == 2:
            if verifyInputFile(f):
                computeAverage(f, punctuations, wordLength)
		# change valid word length
        elif choice == 3:
            wordLength = modifyWordLength(wordLength)
		# disable certain punctuations from being used as sentence delimiters
        elif choice == 4:
            punctuations = excludePunctuations(punctuations)
		# export sentences of certain length into an external file
        elif choice == 5:
            if verifyInputFile(f):
                exportLongSentences(f, punctuations, wordLength)
		# save computed sentence length into an external file
        elif choice == 6:
            if verifyInputFile(f):
                generateReport(f, punctuations, wordLength)
		# easter egg
        elif choice == 7:
            batch()
            pause()
def clearScreen():
	# function to clear the contents of the screen
	# need to identify OS first cause diff OS has diff commands
    # if linux or osx
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        os.system('clear')
    # if windows
    elif platform == "win32":
        os.system('cls')
def pause():
	# function to pause the screen so that user has time to see any error message
    input("\nPress the [enter] key to continue . . .")
    clearScreen()
def generateReport(f, punctuations, wordLength):
    sentences = []
    sentences = parseSentences(f, punctuations)
    w = open("report-" + f.name, "w")
    sentences = []
    sentences = parseSentences(f, punctuations)
    w.write ("Sentences parsed: \n")
    w.write ("---------------------\n")
    i = 1
    totalWords = 0
    for sentence in sentences:
        words = parseWords(sentence, wordLength, punctuations)
        totalWords += len(words)
        w.write ("\n" + str(i) + ". " + str(sentence) + "\nValid word(s) in this sentence: " + str(words) + "\n")
        i += 1
    w.write ("\nSTATISTICS\n===========")
    w.write ("\nNote: Non-alphabetical characters were dropped when counting words.")
    w.write ("\nPunctuations used to delimit sentences: " + str(punctuations))
    w.write ("\nValid word length: " + str(wordLength) + " letters")
    w.write ("\nTotal number of sentences in this file: " + str(len(sentences)))
    w.write ("\nTotal number of valid words in this file: " + str(totalWords))
    if len(sentences) > 0:
        w.write ("\nAverage sentence length: " + str(round(totalWords/len(sentences), 2)) + " words per sentence")
    else:
        w.write ("\nAverage sentence length: 0 words per sentence")
    w.close()    
    print ("\nReport generated and stored in:", w.name)
    # launch generated file on windows
    if platform == "win32":
        try:
            os.system(w.name)
        except:
            pass
    pause()
def exportLongSentences(f, punctuations, wordLength):
    sentences = parseSentences(f, punctuations)
    while True:
        try:
            sentenceLength = int(input("Enter length (based on number of words) of the sentences you want to export:\n> "))
            if sentenceLength >= 1:
                w = open("sentences-" + f.name, "w")
                w.write("The following sentences are composed of " + str(sentenceLength) + " or more valid words.\nSentences are delimited with these punctuations: " + str(punctuations) + "\nA valid word is configured to have " + str(wordLength) + " letters.\n\n")
                i = 1
                for sentence in sentences:
                    words = parseWords(sentence, wordLength, punctuations)
                    if len(words) >= sentenceLength:
                        w.write(str(i) + ". " + sentence + " -> " + str(len(words)) + " valid word(s)\n\n")
                        i += 1
                w.close()
                print ("Sentences have been exported to: \"" + w.name + "\"")
                # launch generated file on windows
                if platform == "win32":
                    try:
                        os.system(w.name)
                    except:
                        pass
                pause()
                return
            else:
                print ("Invalid value.")
                pause()
        except:
            print("Invalid input.")
            pause()
def excludePunctuations(punctuations):
    done = False
    while not done:
        print ("The following punctuations delimit a sentence: ")
        i = 1
        for symbol in punctuations:
            print (str(i) + " =", symbol)
            i += 1
        try:
            exclude = int(input("Enter the number that corresponds to the punctuation you want to exclude from this list.\nNote that \".\" cannot be excluded.\nTo reset the list to its default value, enter 0\n> "))
            exclude -= 1
            if exclude == 0:
                print ("Periods cannot be excluded.")
                pause()
            elif exclude == -1:
                print ("\nPunctuation list is now reset.")
                pause()
                return [".", ",", ";", ":", "?", "!"]
            elif exclude in range(0, len(punctuations)):
                punctuations.pop(exclude)
                done = True
            else:
                print ("Invalid choice.")
                pause()
        except:
            print ("Invalid input.")
            pause()
    print ("\nNew punctuation list:", punctuations)
    pause()
    return punctuations
def modifyWordLength(wordLength):
    while True:
        print ("Current length of valid words:", wordLength)
        try:
            length = int(input("New length: "))
            if length < 1:
                print ("Word length cannot be less than 1.")
                pause()
            else:
                wordLength = length
                print ("Current length of valid words:", wordLength)
                pause()
                return wordLength
        except:
            print ("Invalid input.")
            pause()
def verifyInputFile(f):
    if f == None:
        print ("No input file specified.")
        pause();
        return False
    return True
def computeAverage(f, punctuations, wordLength):
    sentences = []
    sentences = parseSentences(f, punctuations)
    print ("Sentences parsed: ")
    print ("----------------------")
    i = 1
    totalWords = 0
    for sentence in sentences:
        words = parseWords(sentence, wordLength, punctuations)
        totalWords += len(words)
        print ( str(i) + ".", sentence, "\nValid word(s):", words)
        print ("\n")
        i += 1
    print ("STATISTICS\n===========")
    print ("Note: Non-alphabetical characters were dropped when counting words.")
    print ("Punctuations used to delimit sentences:", punctuations)
    print ("Valid word length:", wordLength, "letters")
    print ("Total number of sentences in this file:", len(sentences))
    print ("Total number of valid words in this file:", totalWords)
    #try catch if len of sentences == 0 or which means sentece list is empty. to prevent division by zero
    if len(sentences) > 0:
        print ("Average sentence length:", round(totalWords/len(sentences), 2), "words per sentence")
    else:
        print ("Average sentence length: 0 words per sentence")
    pause()
def openFile():
    validFile = False
    while not validFile:
        inputFile = input ("Ensure that the input file is stored in the same directory as Essay Parser.\nEnter file name or \"q\" to cancel: ")
        if inputFile == "q":
            return
		# check if user entered nothing
        elif inputFile == "":
            print ("You did not specify a file name.")
            pause()
        # check for valid extension
        elif inputFile.endswith(".txt"):
            try:
                f = open (inputFile, "r")
                validFile = True
            except FileNotFoundError:
                print ("The file does not exist.")
                pause()
            except PermissionError:
                print ("Permission denied. Check permission settings to access the file.")
                pause()
        else:
            print ("Invalid file type.")
            pause()
    print("File loaded successfully.")
    pause()
    return f
def parseSentences(f, punctuations):
    sentenceList = []
    line = ""
    endOfFile = False
    f.seek(0)
    while not endOfFile:
        character = f.read(1)
        if not character:
            endOfFile = True
        # split sentences into a list using a set of punctuations as delimeter
        elif character == "\n":
            line += " "
        elif character in punctuations:
            line += character
            # strip leading and trailing extra spaces and line break before appending to list
            sentenceList.append(line.strip())
            line = ""
        else:
            line += character
    # append the last read line in case it didnt have a punctuation
    # also check if it's a letter not symbol
    line = line.strip()
    if line != "":
        if (line[0].isalpha()):
            sentenceList.append(line)
    return sentenceList
def batch():
    # batch processing to be implemented in the future
    print("      .=""=.")
    print("    / _  _ \\")
    print("   |  d  b  |")
    print("   \   /\   /")
    print("  ,/'-=\/=-'\,")
    print(" / /        \\ \\")
    print("| /          \\ |")
    print("\/ \        / \\/")
    print("    '.    .'")
    print("    _|`~~`|_")
    print("    /|\\  /|\\")
    print("This feature will be implemented in our future release.")
    print("In the meantime, try to catch this pokemon.")
def parseWords(sentence, wordLength, punctuations):
    # a word is any set of characters separated by space or punctuation
    # any characters that is not A-z or a-z will be dropped
    words = []
    word = ""
    # drop characters other than letters
    for character in sentence:
        if character.isalpha() or character == " ":
            word += character
        elif character in punctuations:
            word += " " 
    sentence = word    
    # remove and leading/trailing spaces
    sentence = " ".join(sentence.split())
    #save it to a list
    words = sentence.split()
    # remove words that are less than the required number of characters
    newList = []
    for word in words:
        if len(word) >= wordLength:
            newList.append(word)
    return newList
def menu():
    while True:
        clearScreen()
        print("*************************************************")
        print("* Essay Parser\t\t\t\t\t*")
        print("* Version 1.00\t\t\t\t\t*")
        print("* Authors: Antonio | Davila | Greene\t\t*")
        print("* Disclaimer: Any bugs encountered while\t*")
        print("* using this software is intentional\t\t*")
        print("* since this software was developed for\t\t*")
        print("* use in a software testing class. >:p\t\t*")
        print("*************************************************\n")
        print("[1] Specify input file")
        print("[2] Compute average sentence length")
        print("[3] Modify valid word length")
        print("[4] Exclude punctuations")
        print("[5] Export long sentences")
        print("[6] Generate report")
        print("[7] Batch processing (beta)")
        print("[8] Exit")
        try:
            return int(input("> "))
        except:
            pass
main()

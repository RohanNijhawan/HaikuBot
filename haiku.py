import operator
import random
import math
import string
import sys
import wikipedia
from string import digits

# Example file only, not for real use


def getWikiText(query):
    results = wikipedia.search(query)
    try:
        page = wikipedia.page(title=results[0], auto_suggest=False)
    except wikipedia.DisambiguationError as e:
        page = wikipedia.page(e.options[0])
    text = page.content.encode('ascii', 'ignore')
    cleanedText = text.translate(None, string.punctuation + digits).lower()
    allWords = cleanedText.split()
    return allWords


def readFile(filename):
    allWords = []
    f = open(filename, 'r')
    for line in f:
        if (type(line) is not str):
            continue
        line = line.translate(None, string.punctuation).lower()
        allWords += line.split()
    return allWords


def generateLists(allWords):
    allNodes = {}
    i = 0
    while i < len(allWords) - 1:
        currentWord = allWords[i]
        nextWord = allWords[i + 1]

        if not currentWord in allNodes:
            allNodes[currentWord] = {}
        if not nextWord in allNodes[currentWord]:
            allNodes[currentWord][nextWord] = 1
        allNodes[currentWord][nextWord] += 1
        i += 1
    return allNodes


def wordByProbability(allNodes, word):
    wordList = allNodes[word]
    totalWords = 0
    for key in wordList:
        totalWords += wordList[key]
    for key in wordList:
        wordList[key] = wordList[key] / float(totalWords)
    randomElement = random.random()
    for key in wordList:
        randomElement -= wordList[key]
        if randomElement <= 0:
            return key


def chain(allNodes, startingWord, syllables):
    if syllables <= 0:
        return ''
    else:
        nextWord = wordByProbability(allNodes, startingWord)
        return startingWord + ' ' + chain(allNodes, nextWord, syllables - countSyllables(nextWord))

# Assumes word has no punctuation


def countSyllables(word):
    numberOfSyllables = 0
    vowels = 'aeiouy'
    for char in range(0, len(word)):
        if word[char] in vowels and word[char - 1] not in vowels:
            numberOfSyllables += 1
    if word.endswith('e'):
        numberOfSyllables -= 1
    if word.endswith('le'):
        numberOfSyllables += 1
    return max(numberOfSyllables, 1)

allWords = readFile("sherlock.txt")
# allWords = calculateSyllables(allWords)
# for i in range(0, 10):
#     print(random.choice(allWords))
allNodes = generateLists(allWords)
# print(chain(allNodes, 'these', 10))

# numberOfWordsToTest = 10
# while numberOfWordsToTest > 0:
#     word = random.choice(allWords)
#     numberOfWordsToTest -= 1
#     print(word + " has %d" % countSyllables(word) + " syllables.")


def haiku(allNodes, startingWord, attempts, debug=False):
    lineOneData = haikuLine(allNodes, startingWord, 5, attempts)
    lineOne = lineOneData[0]
    lineTwoStart = lineOneData[1]
    lineOneSyllables = lineOneData[2]
    lineTwoData = haikuLine(allNodes, wordByProbability(
        allNodes, lineTwoStart), 7, attempts)
    lineTwo = lineTwoData[0]
    lineThreeStart = lineTwoData[1]
    lineTwoSyllables = lineTwoData[2]
    lineThreeData = haikuLine(allNodes, wordByProbability(
        allNodes, lineThreeStart), 5, attempts)
    lineThree = lineThreeData[0]
    lineThreeSyllables = lineThreeData[2]
    if debug:
        return lineOne + ' ' + str(lineOneSyllables) + '\n' + lineTwo + ' ' + str(lineTwoSyllables) + '\n' + lineThree + ' ' + str(lineThreeSyllables) + '\n'
    else:
        return lineOne + '\n' + lineTwo + '\n' + lineThree + '\n'


def haikuLine(allNodes, startingWord, syllables, attempts):
    for i in range(0, attempts):
        syllableSum = 0
        line = chain(allNodes, startingWord, syllables)
        lineList = line.split()
        for word in lineList:
            syllableSum += countSyllables(word)
        if syllableSum == syllables:
            break
    return (line, lineList.pop(), syllableSum)


def wikiHaiku(word, attempts):
    text = getWikiText(word)
    nodes = generateLists(text)
    return haiku(nodes, word, attempts, True)

print(wikiHaiku("gemini", 1000))

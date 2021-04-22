# from nltk.probability import sum_logs
# from summarizer import TransformerSummarizer
from transformers import pipeline
import enchant
import re

summarizer = pipeline("summarization")
usDict = enchant.Dict('en_US')
ukDict = enchant.Dict('en_UK')

REDUCEFACTOR = 5

# PATH TO INPUT FILE
filePath = 'pathToFile.txt'

# Open an LPA .txt file, and read it into a variable
f = open(filePath)
LPA_text = f.read()

# will contain most of the random weird strings in the input OCR file
gibberishWords = set()

# split text into lines
lines = LPA_text.split('\n')
for line in lines:
    # split line into words
    lineWords = line.split(' ')
    shouldRemoveLine = []
    # if a short line (these ones contain gibberish)
    if len(lineWords) in [i for i in range(1, 10)]:
        for originalword in lineWords:
            word = originalword
            # remove special characters at beginning and end
            word = re.sub(r'(:|;|,|\.)\Z', '', word)
            word = re.sub(r'(\]|\)|"|\')|(\[|\(|"|\')', '', word)

            if len(word) > 1:

                # at least five digits (larger than a year)
                containsWeirdNumber = re.search(r'\d\d\d\d\d', word) != None

                # check if valid dictionary word
                if containsWeirdNumber or not (usDict.check(word) or ukDict.check(word)):
                    # check if chapter number e.g. 1.4 or 14.19
                    isChapterNumber = re.search(
                        r'\A[1-9]?[0-9]\.[1-9]?[0.9]\Z', word) != None

                    isTimeWordOrPercentage = re.search(
                        r'(am|pm|AM|PM|%)\Z', word) != None

                    isMoney = re.search(
                        r'^(\$|€|£)?(\d|\d\d|\d\d\d)(,\d{3})*(\.\d*)?(\$|€|£)?$', word)

                    # gibberish we are filtering out contians a mix of letters and special characters
                    # also inclusing '&' character as passable
                    hasJustLetters = re.search(r'[^a-zA-Z\&]', word) == None

                    # found gibberish word
                    if not hasJustLetters \
                            and not isChapterNumber \
                            and not isTimeWordOrPercentage \
                            and not isMoney:
                        gibberishWords.add(originalword)
                        shouldRemoveLine.append(True)
                    else:
                        shouldRemoveLine.append(False)
                else:
                    shouldRemoveLine.append(False)
        if all(shouldRemoveLine):
            lines.remove(line)

mergedText = '\n'.join(lines)
print(gibberishWords)
for gibberishWord in gibberishWords:
    mergedText = mergedText.replace(gibberishWord, '')

mergedText = re.sub('\n\n', '\n', mergedText)  # remove empty lines
# use ||| as a splitting marker for paragraphs
mergedText = re.sub(r'\.\n', '.|||', mergedText)
mergedText = re.sub(r'ARTICLE', '|||ARTICLE', mergedText)

paragraphs = mergedText.split('|||')

sections = ['TABLE OF CONTENTS:\n']
index = 0

for paragraph in paragraphs:
    isArticleStart = re.search('^article', paragraph, re.IGNORECASE) != None
    if isArticleStart:
        sections.append('\n' + paragraph)
        index += 1
    else:
        sections[index] += '\n' + paragraph

formattedFile = open("formattedText.txt", 'w')
mergedSections = '\n'.join(sections)
formattedFile.write(mergedSections)
formattedFile.close()


def summariseListOfTexts(listOfTexts, fileName):
    summarisedTexts = []
    articleIndex = 0
    for index, text in enumerate(listOfTexts):
        isArticleStart = re.search('^article', text, re.IGNORECASE) != None
        if isArticleStart:
            summarisedTexts.append('Article: ' + str(articleIndex))
            articleIndex += 1
            continue
        summary = summarizer(text)
        summarisedTexts.append(summary[0]['summary_text'])

    summary_file = open(fileName+'.txt', 'w')
    finalOutput = '\n\n'.join(summarisedTexts)
    summary_file.write(finalOutput)
    summary_file.close()


summariseListOfTexts(paragraphs, 'KnightsbridgeSectionSummmary')

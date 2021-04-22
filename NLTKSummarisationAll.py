"""
Created Dec 2020

@author: Danny Rice

Version of Summary Tool that loops through every file in the LPA directory
"""

# Libraries we need for summarisation (nltk), reformatting (re), getting a givien number of top summary sentences (heapq), and looping through directory (os)
import nltk
import re
import heapq
import os

# Downlaod resources needed from nltk (probably redundant)
nltk.download('punkt')
nltk.download('stopwords')

# PATH TO OUTPUT FILE
filePath = 'pathToFile.txt'

# Create/open file to write summaries to
summary_file = open(filePath, 'w')

# Go through and summarise each file (txt format only), and write summary to a file
for filename in os.listdir("LPAs"):
    if filename.endswith(".txt"):

        # Open an LPA .txt file, and read it into a variable
        LPA_file = open("LPAs\\" + filename)
        LPA_text = LPA_file.read()
        print("Summarising: " + LPA_file.name)

        # Reformatting text to replace white space (multiple spaces) with a single space
        LPA_text = re.sub(r'\s+', ' ', LPA_text)

        # Copy of LPA, formatted with all special characters and digits removed
        LPA_text_chars = re.sub('[^a-zA-Z]', ' ', LPA_text)
        LPA_text_chars = re.sub(r'\s+', ' ', LPA_text_chars)

        # Split original text into sentences
        sentences = nltk.sent_tokenize(LPA_text)

        # Gets "stopwords" to ignore from English language (i.e. I, you, it, and, the...)
        stopwords = nltk.corpus.stopwords.words('english')

        # Count occurences of each word in formatted LPA text
        word_counts = {}
        for word in nltk.word_tokenize(LPA_text_chars):
            # Not counted if it is a "stopword"
            if word not in stopwords:
                # If first occurance set count to 1
                if word not in word_counts.keys():
                    word_counts[word] = 1
                # Else add 1 to the count
                else:
                    word_counts[word] += 1

        # Get max number of occurences of any word, then get frequency of each word by deviding its count by the max count
        max_count = max(word_counts.values())
        word_frequency = {}
        for word in word_counts.keys():
            word_frequency[word] = (word_counts[word] / max_count)

        # Gives each sentence a score based on the frequency of the words it contains
        sentence_scores = {}
        for sentence in sentences:
            for word in nltk.word_tokenize(sentence.lower()):
                if word in word_frequency.keys():
                    if len(sentence.split(' ')) < 25:
                        if sentence not in sentence_scores.keys():
                            sentence_scores[sentence] = word_frequency[word]
                        else:
                            sentence_scores[sentence] += word_frequency[word]

        # Retrieve top 5 sentences to be a summary for the LPA
        sum_sents = heapq.nlargest(5, sentence_scores, key=sentence_scores.get)

        # Join together and write summary to file
        summary = '\n'.join(sum_sents)
        summary_file.write(LPA_file.name + ":\n" + summary + "\n\n")
        LPA_file.close()

summary_file.close()

from summarizer import Summarizer
import re

# PATH TO INPUT FILE
filePath = 'pathToFile.txt'

# Open an LPA .txt file, and read it into a variable
f = open(filePath)
LPA_text = f.read()

# Reformatting text to replace white space (multiple spaces) with a single space
LPA_text = re.sub(r'\s+', ' ', LPA_text)

# Copy of LPA, formatted with all special characters and digits removed
LPA_text_chars = re.sub('[^a-zA-Z.\-,!?0-9]', ' ', LPA_text)
body = re.sub(r'\s+', ' ', LPA_text_chars)

# Pass sanitised text to summarisation tool
model = Summarizer()
result = model(LPA_text)

# See output
print(result)

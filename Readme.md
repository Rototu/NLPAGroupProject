# nlpa-cslaw

CS and Law Project 2020-2021

## Purpose

Summarisation of NLPAs

## Installation

For BertSummarisation.py (requires a few gigs of free disk space!):

```[bash]
pip install torch==1.7.1+cpu torchvision==0.8.2+cpu torchaudio===0.7.2 -f https://download.pytorch.org/whl/torch_stable.html
pip install bert-extractive-summariser 
```

For GPT2 and XLNET do in addition:

```[bash]
pip install transformers==2.2.0
pip install spacy==2.0.12
```

For BART model (we ran thin on Google Colab, where an additional exclamation mark is needed at the beginning of each line):

```[bash]
pip install transformers
pip install torch
pip install pyenchant
apt install enchant
```

Note: apt command above might differ based on OS used

## Contents of project

In the "docs" folder you can find our website, which is also available at <https://rototu.github.io/NLPAGroupProject>.

In the root foler, there are several python scripts that we have worked on for the different models.

The files are named based on the model that they used. The simple/advanced keywords in the name indicate whether we perform additional text cleanup in the script.

The "SummaryToolAll" script summarises all LPAs found in the folder "LPAs" (must be added by user first).

In each of the other files, there is a line near the beginning with a variable indicating the path of the file to be summarized (should be a plain txt file). These lines have a comment indicating its role above it. In all files these lines should look like this:

```[python]
# PATH TO INPUT FILE
filePath = 'pathToFile.txt'
```

Change the file path accordingly in those lines before running the scripts.

Team:

- Daniel Rice
- Eirini Papoutsi
- Eleni Nerantzi
- Emanuel Farauanu
- Felix Jaeger
- Munib Mesinovic

import json
import os
import math
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer

swl = []
docid = []
wordList = []
pindex = {}
tfidf = {}
magnitude = []

# initializing lemmatizer
lemmatizer = WordNetLemmatizer()

# Read stop word from file and split them
# and store each word in swl list
def readStopWord():
    try:
        global swl
        swl = open('Stopword-List.txt', 'r').read().split()
    except Exception as e:
        print(e)

# Find the all file name in the directory, extract docid and store it in docid variable
def AllFileInDir():
    global docid
    # list of file name in the ShortStories dir
    file_names = os.listdir("ShortStories/")
    # split the name of file to get docid
    docid = [int(fn.split('.')[0]) for fn in file_names]

    try:
        docid.sort()     # sort the docids
    except Exception as e:
        print(e)

# Remove punctuation from stories
def removePunctuation(words):
    words = words.replace("n’t", " not").replace("’ll", " will").replace("’m", " am").replace(
        "’ve", " have").replace("’re", " are").replace("’d", " had").replace("it’s", "it is").replace(
        "he’s", "he is").replace("she’s", "she is").replace("that’s", "that is").replace("who’s", "who is").replace(
        "to-morrow", "tomorrow").replace("(", "").replace(")", "").replace("[", "").replace("]", "").replace(
        "’", "").replace("—", " ").replace("“", "").replace("”", "").replace("‘", "").replace(
        "'", "").replace(",", "").replace("!", "").replace(".", "").replace(":", "").replace(
        ";", "").replace("?", "").replace("-", " ").replace("*", "")

    # .replace("¯", "").replace(
    # "ã", "a").replace("ª", "a").replace("©", "c").replace("§", "s").replace("¨", "")
    return words

# Reads all stories from files one by one and stemm the tokens
def readFilesAndLemmatize():
    dic = {}
    for x in docid:
        f = open("ShortStories/"+str(x)+".txt", 'r',
                encoding='utf8')    # read file one by one

        f = f.read()
        # casefolding and removing punctuations and tokenize (words list)
        f = removePunctuation(f.lower()).split()
        # Stemming words and storing list of words in a dictionary agains their doc id

        dic[x] = [lemmatizer.lemmatize(word) if word not in swl else word for word in f]

    # making inverted index and positional index
    creatPositionalIndex(dic)
    

# Positional index creation
def creatPositionalIndex(dic):
    for docid in dic.keys():
        for position, word in enumerate(dic[docid]):
            if word in swl:
                continue
            # positionIndex(word, docid, position)
            if word not in pindex:  # if word is not in the positional index then add it also add its doc id
                pindex[word] = {}
                pindex[word][docid] = []

            else:  # if doc id is not in the list then append it againt the given word/key
                if docid not in pindex[word]:
                    pindex[word][docid] = []
                    
            # append position
            pindex[word][docid].append(position)


def creattfidf():
    global tfidf
    totalDoc = len(docid)

    for word in pindex.keys():
        idf = math.log10(len(pindex[word]))/totalDoc
        for i in docid:
            if i not in tfidf.keys():
                tfidf[i] = []

            if i in pindex[word].keys():
                tfidf[i].append(len(pindex[word][i])*idf)
            else:
                tfidf[i].append(0)


# Write positional indexes to file
def WriteIndexesToFile():
    piFile = open('PositionalIndex.json', 'w', encoding='utf8')
    piFile.write(json.dumps(pindex))
    piFile.close()

    tfidfFile = open('TfIdf.json', 'w', encoding='utf8')
    tfidfFile.write(json.dumps(tfidf))
    tfidfFile.close()

# Reading indexes from their respective file and saving them in global dictionaries
def ReadIndexesFromFile():
    global pindex
    global tfidf

    try:
        piFile = open('PositionalIndex.json', 'r', encoding='utf8')
        tfidfFile = open('TfIdf.json', 'r', encoding='utf8')
        
        pindex = json.loads(piFile.read())
        tfidf = json.loads(tfidfFile.read())
        
        piFile.close()
        tfidfFile.close()

        if (not pindex) or (not tfidf):
            readFilesAndLemmatize()
            creattfidf()
            WriteIndexesToFile()

    except Exception as e:
        print(e)
        readFilesAndLemmatize()
        creattfidf()
        WriteIndexesToFile()
        

def main():
    global wordList
    readStopWord()
    AllFileInDir()
    ReadIndexesFromFile()
    
    wordList = list(pindex.keys())

    # calculating magnitude
    for vec in tfidf.keys():
        magnitude.append(np.linalg.norm(tfidf[vec]))




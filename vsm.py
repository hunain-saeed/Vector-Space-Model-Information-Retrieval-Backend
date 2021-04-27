import json
import os
import math
import nltk
from nltk.stem import WordNetLemmatizer

swl = []
docid = []
dic = {}
pindex = {}
tf = {}
tfidf = {}

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

# Find the all file name in the directory, extract docid and store it on docid variable
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
    for x in docid:
        f = open("ShortStories/"+str(x)+".txt", 'r',
                encoding='utf8')    # read file one by one
        
        # title is used to read the first line of doc
        # title[x] = f.readline().replace(" \n", "").replace("\n", "")

        f = f.read()
        # casefolding and removing punctuations and tokenize (words list)
        f = removePunctuation(f.lower()).split()
        # Stemming words and storing list of words in a dictionary agains their doc id

        dic[x] = [lemmatizer.lemmatize(word) if word not in swl else word for word in f]

    # making inverted index and positional index
    creatPositionalIndex()
    # print(dic)

# Positional index creation
def creatPositionalIndex():
    for docid in dic.keys():
        for position, word in enumerate(dic[docid]):
            if word in swl:
                continue
            # positionIndex(word, docid, position)
            if word not in pindex:  # if word is not in the positional index then add it also add its doc id
                pindex[word] = {}
                pindex[word][docid] = []
                tf[word] = {}
                tf[word]["df"] = 1
                tf[word][docid] = 1

            else:  # if doc id is not in the list then append it againt the given word/key
                if docid not in pindex[word]:
                    pindex[word][docid] = []
                    tf[word][docid] = 1
                    tf[word]["df"] += 1
                    
            # append position
            pindex[word][docid].append(position)
            tf[word][docid] += 1
    
    func()

def creattfidf():
    totalDoc = len(docid)
    for word in tf.keys():
        idf = math.log10(tf[word]["df"])/totalDoc
        for i in docid:
            if i not in tfidf.keys():
                tfidf[i] = []

            if i in tf[word].keys():
                tfidf[i].append(tf[word][i]*idf)
            else:
                tfidf[i].append(0)



readStopWord()
AllFileInDir()
readFilesAndLemmatize()
    

def d():
    return json.dumps(tfidf)

def p():
    return json.dumps(pindex)

def t():
    return json.dumps(tf)
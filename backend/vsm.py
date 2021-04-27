import json
import os
import nltk
from nltk.stem import WordNetLemmatizer

swl = []
docid = []

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












def hello_world():
    return json.dumps({"hello": "hello world"})
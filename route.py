import vsm
import json
import math

# ROUTE
def d():
    return json.dumps(vsm.tfidf)

#  ROUTE
def p():
    return json.dumps(vsm.pindex)

# ROUTE
def w():
    return json.dumps(vsm.wordList)

# ROUTE
def queryType(query):
    result = {}
    # result = {"result": [], "error": ""}
    result["result"] = preProcessQuery(query)
    # return json.dumps({"result": [], "error": "Invalid Query"})
    return json.dumps(result)

# Remove punctuation and convert into list
# Lemmatize query
# Calculate tf of query
# Calculate tf-idf of query vector
def preProcessQuery(query):
    query = vsm.removePunctuation(query).split()
    query = [vsm.lemmatizer.lemmatize(word) if word not in vsm.swl else word for word in query]
    queryVec, windex = queryToVector(query)

    totalDoc = len(vsm.docid)
    # Calculating tf-idf for queryVec
    for word in windex.keys():
        try:
            idf = math.log10(len(vsm.pindex[word]))/totalDoc
            queryVec[windex[word]] *= idf
        except Exception as e:
            print(e)
    
    return queryVec


def queryToVector(query):
    qVector = [0] * len(vsm.wordList)
    windex = {}
    for word in query:
        try:
            index = vsm.wordList.index(word)
            qVector[index] +=1
            windex[word] = index
        except Exception as e:
            print(e)
    return qVector, windex




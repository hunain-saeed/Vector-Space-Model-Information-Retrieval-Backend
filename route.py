import vsm
import json
import math
import numpy as np
from flask import request




# ROUTE
def d():
    return json.dumps(vsm.tfidf)

#  ROUTE
def p():
    return json.dumps(vsm.pindex)

# ROUTE
def w():
    return json.dumps(vsm.magnitude)


# ROUTE
def queryType():
    data = json.loads(request.data)
    query = data["query"]
    alpha = data["alpha"]

    # result = {"result": [], "error": ""}
    result = {}
    queryVec = preProcessQuery(query)
    
    result["result"] = cosineSim(queryVec, alpha)


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

# Convert query into vector
# Calculate tf of words
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


def cosineSim(queryVec, alpha):
    resultDoc = []
    qmeg = np.linalg.norm(queryVec)

    
    for docid in vsm.tfidf.keys():
        ans = 0.0
        # dot1 = np.dot(vsm.tfidf[docid], queryVec)
        # print(type(dot1))

        mg = float((vsm.magnitude[int(docid)-1] * qmeg))
        
        for i in range(len(queryVec)):
            ans += queryVec[i] * vsm.tfidf[docid][i]
        

        resultDoc.append(ans/mg)

    return resultDoc

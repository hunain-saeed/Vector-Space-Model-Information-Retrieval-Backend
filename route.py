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
    try:
        data = json.loads(request.data)
        query = data["query"]
        alpha = float(data["alpha"])

        result = {}

        queryVec = preProcessQuery(query)
        
        result["result"], result["score"] = ranked(queryVec, alpha)
        result["len"] = len(result["result"])

        if result["len"] == 0:
            result["error"] = "No Document Found"
            return json.dumps(result)
        
        return json.dumps(result)
    except Exception as e:
        print(e)
        return json.dumps({"result": [], "error": "Invalid Query"})

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
            queryVec[windex[word]] = round( queryVec[windex[word]] * idf, 6 )
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

def ranked(queryVec, alpha):
    sim = cosineSim(queryVec, alpha)
    z = sorted(zip(list(sim.values()), list(sim.keys())), reverse=True)
    rank = [i for _,i in z]
    score = [_ for _, i in z]
    return rank, score

def cosineSim(queryVec, alpha):
    simDocQ = {}
    qmeg = np.linalg.norm(queryVec)
    
    for docid in vsm.tfidf.keys():
        ans = 0.0

        mg = float((vsm.magnitude[int(docid)-1] * qmeg))
        # Replace with numpy multiplication
        for i in range(len(queryVec)):
            ans += queryVec[i] * vsm.tfidf[docid][i]
        
        cos = round(ans/mg, 6)

        if cos > alpha:
            simDocQ[docid] = cos

    return simDocQ

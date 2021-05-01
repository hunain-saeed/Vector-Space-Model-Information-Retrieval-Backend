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
    return json.dumps(vsm.wdf)

# ROUTE
def w():
    return json.dumps(vsm.magnitude)


# ROUTE
def queryType():
    try:
        alpha = 0.005
        data = json.loads(request.data)
        if(data["alpha"] != ''):
            alpha = float(data["alpha"])

        query = data["query"]
        
        result = {"result": [], "score": [], "len": 0, "error": ""}

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
    return queryToVector(query)

# Convert query into vector
# Calculate tf of words
def queryToVector(query):
    qVector = []
    totalDoc = len(vsm.docid)
    for word in vsm.wdf.keys():
        tfidf = (math.log10(vsm.wdf[word]["df"])/totalDoc) * query.count(word)
        qVector.append(round( tfidf, 6 ))
    
    return qVector

def ranked(queryVec, alpha):
    sim = cosineSim(queryVec, alpha)
    z = sorted(zip(list(sim.values()), list(sim.keys())), reverse=True)
    rank = [i for _,i in z]
    # rank.sort(key=int)
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

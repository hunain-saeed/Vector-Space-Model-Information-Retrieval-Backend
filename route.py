import vsm
import json

def d():
    return json.dumps(vsm.tfidf)

def p():
    return json.dumps(vsm.pindex)

def w():
    return json.dumps(vsm.wordList)

def queryToVector(query):
    lst = [0] * len(vsm.wordList)
    query = query.split()
    for word in query:
        try:
            lst[vsm.wordList.index(word)] +=1
        except Exception as e:
            print(e)
    return lst


def queryType(query):
    result = {}
    # result = {"result": [], "error": ""}
    result["result"] = queryToVector(query)
    # return json.dumps({"result": [], "error": "Invalid Query"})
    return json.dumps(result)
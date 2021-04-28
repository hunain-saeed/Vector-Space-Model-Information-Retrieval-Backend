import vsm
import json

def d():
    return json.dumps(vsm.tfidf)

def p():
    return json.dumps(vsm.pindex)

def queryType(query):
    result = {"result": [], "error": ""}

    return json.dumps({"result": [], "error": "Invalid Query"})
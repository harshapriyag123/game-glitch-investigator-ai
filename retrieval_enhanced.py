"""Dependency-free BM25 retrieval across curated documentation sources."""
import math
import re
from collections import Counter
from knowledge_docs import DOCUMENTS
def words(value):
    return re.findall(r"[a-z0-9]+", value.lower())
def search_documents(query, limit=3, category=None):
    if not isinstance(query,str) or not query.strip(): return []
    docs=[d for d in DOCUMENTS if category is None or d["bug_id"]==category]
    terms=set(words(query))
    if not terms or not docs:return []
    tokens=[words(d["title"]+" "+d["text"]) for d in docs]
    avg_len=sum(map(len,tokens))/len(tokens)
    result=[]
    for doc,t in zip(docs,tokens):
        counts=Counter(t)
        score=0.0
        for term in terms:
            df=sum(term in x for x in tokens)
            idf=math.log(1+(len(docs)-df+0.5)/(df+0.5))
            freq=counts[term]
            if freq:
                score+=idf*(freq*2.2)/(freq+1.2*(0.25+0.75*len(t)/max(1,avg_len)))
        if score>0: result.append({**doc,"score":round(score,4)})
    return sorted(result,key=lambda item:(-item["score"],item["id"]))[:limit]

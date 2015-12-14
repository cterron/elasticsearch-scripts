#!/usr/bin/python
import sys
import requests
import json

url="http://localhost:9200"

queryinit="""{"size": 1000, "query": { "match_all": {}}}"""
querynext="""{ "scroll": "1m", "scroll_id": "%s"}"""
def getresults(result):
    if result.status_code != 200:
        print "Error loading from ElasticSearch"
        print result.text
        sys.exit(-1)
    data = result.json()
    dataarray = data['hits'].get('hits')
    if dataarray is None:
        sys.exit(0)
    for source in dataarray:
        print json.dumps(source['_source']) 
    return data['_scroll_id']

# Use sessions to interact
s = requests.Session()
index = 0
# Use the scroll API 
# Scroll API start
result = s.get(url + "/_search?scroll=1m", data=queryinit)
scroll_id = getresults(result)

while  True:
    q = querynext % scroll_id
    result = s.get(url + "/_search/scroll?scroll=1m", data=scroll_id)
    scroll_id = getresults(result)
    



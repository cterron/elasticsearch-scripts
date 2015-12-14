#!/usr/bin/python
import sys
import requests
import json

url="http://localhost:9200"
ninx = int(sys.argv[2])
data="""{"index": {"_inint(sys.argv[2])dex": "%s", "_type": "message"}}\n"""
bulksize =  500 
with open(sys.argv[1],"r") as f:
    s = requests.Session()
    # Dump old test indexes
    index = 0
    while True:
        bulkdata = []
        inx = index + 1
        for i in range (0,bulksize-1):
            line = f.readline()	
            if line == '':
               break
            bulkdata = bulkdata +  [data % ("test%d" % inx )] + [line]
       	if bulkdata == []:
            break
        r = s.post(url + "/_bulk", data = "".join(bulkdata))
        if r.status_code != 200:
            print "Can't insert data"
            print r.text
            print bulkdata
            sys.exit(-1)
        print r.json()['took']
        index = (index + 1) % ninx
    
    

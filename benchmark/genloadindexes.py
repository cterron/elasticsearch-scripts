#!/usr/bin/python
import sys
import requests
import json

url=sys.argv[1]
ninx = int(sys.argv[3])
data="""{"index": {"_index": "%s", "_type": "message"}}\n"""
bulksize=500
with open(sys.argv[2],"r") as f:
    s = requests.Session()
    # Dump old test indexes
    s.delete(url + "/test*")
    # Create the test indexes
    for i in range(1,ninx + 1 ):
        print "Creating test%d" % i
        r = s.post(url + "/test%d" % i)
        if r.status_code != 200:
            print "Can't create index"
            print r.text
            sys.exit(-1)
    #
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
    
    
    

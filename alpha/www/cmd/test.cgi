
import json

def put_json(jso):
    s = json.dumps(jso)
    print "Content-type: application/javascript"
    print
    print s

put_json('test2')




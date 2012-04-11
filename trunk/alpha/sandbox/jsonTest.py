
from json import loads as jl

a = jl('["foo", {"bar":["baz", null, 1.0, 2]}]')

print a



b = jl('{"a.b.c" : 2}')

print b[u'a.b.c']

c = """
mainwindow.title = "test"
mainwindow.position.z = 100
mainwindow.position.y = 200"""

d = '[{' + c.replace('=', '":').replace('\n', '\n"').strip().replace('\n', ',') + '}]'

print d
print jl(d)





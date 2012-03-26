
import sys

if not len(sys.argv) == 2:
    print 'usage: python rename.py <filename>'
    sys.exit()

fn = sys.argv[1]
#fn0 = fn.split('/')[0]
#fn = fn.split('/')[1]

fn1 = fn[:7]
fn2 = int(fn.split('.')[0][7:])

print '%s_%08d.fpf' % (fn1,fn2)

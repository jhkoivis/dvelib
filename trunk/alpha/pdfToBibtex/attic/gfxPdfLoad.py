
import sys
sys.path.append('C:\Program Files (x86)\SWFTools\python26')

import gfx

doc = gfx.open('pdf', '../test_prl.pdf')

a = 'title', 'subject', 'keywords', 'author', 'creator', 'producer', 'creationdate', 'moddate', 'linearized', 'tagged', 'encrypted', 'oktoprint', 'oktocopy', 'oktochange', 'oktoaddnotes', 'version'

for key in a:
    print doc.getInfo(key)

text = gfx.PlainText()
page = doc.getPage(1)
text.startpage(page.width, page.height)
page.render(text)
text.endpage()
#text.save("test.txt")
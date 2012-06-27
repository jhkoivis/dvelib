import sys
sys.path.append('C:\Program Files (x86)\SWFTools\python26')
import gfx
#
#doc = gfx.open('pdf', 'test_prl.pdf')
#text = gfx.PlainText()
#page = doc.getPage(1)
#text.startpage(page.width, page.height)
#page.render(text)
#text.endpage()
#text.save("test.txt")

class GetDoiFromPdf:
    
    def __init__(self, pdfFn):

        self.pdfFn = pdfFn
        self.doi = None
        self.tmpFN = "tmpFile.txt"
        
        if self.doi == None: self.doi = self.tryTxt(pdfFn)
        #if self.doi == None: self.tryOcr(pdfFn)
        
        
    def getDoi(self):
        return self.doi    
        
    def tryTxt(self, pdfFn):
        
        doc = gfx.open('pdf', pdfFn)
        method = gfx.PlainText()

        txt = self.txtFromDoc(doc, method)
        return self.getDoiFromTxt(txt)

    def tryOcr(self, pdfFn):
        doc = gfx.open('pdf', pdfFn)
        gfx.setparameter('zoom', '160')
        method = gfx.OCR()

        txt = self.txtFromDoc(doc, method)
        return self.getDoiFromTxt(txt)

    def getDoiFromTxt(self, txt):
        for line in txt:
            #print line
            line2 = line.lower()
            index = line2.find('doi')
            if index >= 0:
                #print line
                splitted = line[index+3:].split()
                for i in splitted:
                    if i.find('/') >= 0: 
                        #self.doi = i
                        return i
                        #print self.doi          

    def txtFromDoc(self, gfxDoc, method):
        for pagenr in range(1,gfxDoc.pages+1):
            page = gfxDoc.getPage(pagenr)
            method.startpage(page.width, page.height)
            page.render(method)
            method.endpage()
        method.save(self.tmpFN)
        
        file = open(self.tmpFN)
        txt = file.readlines()
        file.close()

        return txt
    
a = GetDoiFromPdf('test_prl.pdf')
print a.getDoi()
        
        
        
        
        
        
        
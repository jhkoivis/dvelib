#import pyPdf
#import time
#import os
#import codecs
import re
import Pdfminer.binding as Pdf2Txt

'''Here is the definition of the pattern to search the References in the article.
Here can provide more pattern like I{Bibliography}'''

_references = " ?R ?e ?f ?e ?r ?e ?n ?c ?e ?s? ?"

def getText(filepath):
    '''Here is the conversion from pdf to text using
    pdfminer extractor. Then all the text that does not
    concern the References is filtered out using regular expression.
    
    @param filepath: the filepath of the pdf
    @return: the references in a text format. If thery are not found return None.
    '''
    
    text = Pdf2Txt.getTextFromPdf(filepath)
    
    r = re.compile(_references)
    listaRef = r.findall(text)
    if len(listaRef) == 0:
        return None
    else:
        '''Filtering out the "non-reference" text'''
        lastRef = listaRef[ len(listaRef) - 1 ]
        index = text.rfind(lastRef)
        text = text[index+len(lastRef):]
        return text


########### OLD CODE ############
#def convertToText(filename):
#    '''
#    This function return the Reference plain text from a pdf using 
#    pyPdf Lib
#    '''
#    
#    text = " "
#    
#    try:
#        input = pyPdf.PdfFileReader(file(filename,"rb"))
#    except IOError:
#        print "Specify a PDF file with exact name"
#        import sys
#        sys.exit(2)
#
#    n = input.getNumPages()
#    
#    for i in range(n):
#        try:
#            text += input.getPage(i).extractText()
#        
#        except pyPdf.utils.PdfReadError:
#            print "Probably a PDF done with images"
#            import sys
#            sys.exit(2)
#    #text = unicode(text,'utf8')
#    text = text.encode('ascii','ignore')
#    text = text.decode('ascii','ignore')
#    text = getTextReferences(text,n,0)
#    return (text,n)
#
#def getTextReferences(text, numPages, offSet):
#    #TODO: Insert if in cascade to take some other case like "References" or "Bibliography"
#    #text = text.encode('utf8','ignore')
#    nChars4Page = len(text)/numPages
#    offSet = int(nChars4Page * offSet)
#    
#    index = text.rfind(_references)
#    text = text[index-offSet:]
#    #text = text[len(_references):]
#    
#    
#    return text
#
#def execPdfToText(filepath):
#        #FIXME: This is a fix because the pdfhtml does not open the file
#        
#        #FIXME: try to search a better smart way to execute pdf to html
#        filepathCorrect = filepath.replace(" ","\ ")
#        
#        execResult = os.popen("pdftotext "+filepathCorrect, "r")
#        if execResult.readline() == "":
#            time.sleep(1)
#            
#            fileNameTxt = filepath[:len(filepath)-4]+".txt"
#            
#            fileTxt = open(fileNameTxt,"r").read()
#            
#            fileNameTxt = fileNameTxt.replace(" ","\ ")
#            
#            if os.popen("rm "+fileNameTxt, "r").readline() <> "":
#                return (fileTxt,False)
#            else:
#                return (fileTxt,True)
#        else:
#            return ("", False)
#    
#
#def execPdfToHtml(filepath):
#        
#        #FIXME: This is a fix beacuse the pdfhtml does not open the file
#        #FIXME: try to search a better smarto way to execute pdf to html
#        filepathCorrect = filepath.replace(" ","\ ")
#        execResult = os.popen("pdftohtml "+filepathCorrect, "r")
#        if execResult.readline().find("Page-")<> -1:
#            time.sleep(1)
#            
#            filehtml_s = filepath[:len(filepath)-4]+"s.html"
#            filehtml_ind = filepath[:len(filepath)-4]+"_ind.html"
#            filehtml = filepath[:len(filepath)-4]+".html"
#            
#            html = open(filehtml_s,"r")
#            #html =codecs.open( filehtml_s, "r", "utf-8" )
#
#            
#            filehtml_s = filehtml_s.replace(" ","\ ")
#            filehtml_ind = filehtml_ind.replace(" ","\ ")
#            filehtml = filehtml.replace(" ","\ ")
#            
#            
#            if os.popen("rm "+filehtml_s +" "+filehtml_ind + " " + filehtml, "r").readline().find('') <> 0:
#                return (html,False)
#            else:
#                return (html,True)
#        else:
#            return ("", False)
#
#def clearFromHtml(stringa):
#    return stringa.replace('<br>','').replace('<b>','').replace('</b>','').replace('<i>','').replace('</i>','').replace('&amp;','&').replace('</BODY>','').replace('</HTML>','')
#
#
#def compareString(s1,s2):
#    a = 0
#    if len(s1) > len(s2):
#        a = 1
#    if len(s1) < len(s2):
#        a= -1
#    if len(s1) == len(s2):
#        a = 0
#    return a
#
#
#def escapeMetachar(stringa):
#    stringa = stringa.replace('\\', '\\\\').replace('.','\.').replace('^','\^').replace('$','\$').replace('*','\*')
#    stringa = stringa.replace('+','\+').replace('?','\?').replace('{','\{').replace('}','\}')
#    stringa = stringa.replace('[','\[').replace(']','\]')
#    stringa = stringa.replace('|','\|').replace('(','\(').replace(')','\)').replace("\x0c","\\n")
#    return stringa
#
#
#def addSpaces(originalText,filepath,nPages):
#    '''
#    This function add space to a text
#    '''
#    
#    numOfSpaces = originalText.count(" ")
#    if numOfSpaces > 0:
#        return originalText
#    else:
#        print "A block Text without spaces. Need pdfToText"
#        (withSpaceText,result) =  execPdfToText(filepath)
#        withSpaceText = withSpaceText.decode('ascii','ignore')
#        #withSpaceText = withSpaceText.encode('ascii','ignore')
#        if result:
#            withSpaceText = getTextReferences(withSpaceText,nPages,0.5)
#            withSpaceText = withSpaceText.replace("\n"," ")
#            withSpaceWordsList = withSpaceText.split(" ")
#            
#            #withSpaceWordsList.sort()
#            withSpaceWordsList.sort(compareString)
#            withSpaceWordsList.reverse()
#            
#            for i in range(len(withSpaceWordsList)):
#                tmpList = []
#                #tmpList.append(escapeMetachar(withSpaceWordsList[i]))
#                tmpList.append(withSpaceWordsList[i])
#                tmpList.append(False)
#                withSpaceWordsList[i] = tmpList
#                
#            k = 0
#            clearText = ""
#            
#            print originalText[355:]
#            while k < len(originalText):
#                for i in range(len(withSpaceWordsList)):
#                    eachWord = withSpaceWordsList[i]
#                    #index = originalText.find(withSpaceWordsList[i][0])
#                    if eachWord[0] == "Coasnon\\." and k==355:
#                        pass
#                    r = re.compile(eachWord[0])
#                    match = r.match(originalText,k)
#
#                    if match and eachWord[1] <> True :
#                        (start,end) = match.span()
#                        clearText+=" "+originalText[start:][:end]
#                        eachWord[1] = True
#                        k=end
#                        break
#                print k
##                    if index <> -1 and withSpaceWordsList[i][1] <> True:
##                       clearText += " "+originalText[:index+len(withSpaceWordsList[i][0])]
##                       withSpaceWordsList[i][1] = True
##                       k = k + len(withSpaceWordsList[i][0])
#                        
#        else:
#            print "Error nell' eseguire pdftotext"
#            return ""
#    return clearText    
#    
#    
#    
#
#    
#def addSpaceHtml(text,filepath,br=False):
#    '''
#    This function add spaces from text.
#    
#    @author: marto
#    
#    '''
#
#    numOfSpace = text.count(' ')
#    
#    #TODO: Think to a better discriminant value. Maybe This too restricted.
#    if numOfSpace > 0:
#        return text
#    else:
#        print "A block Text without spaces. Need pdfToText"
#        (textWithSpace, done) = execPdfToHtml(filepath)
#        
#        '''If the pdfhtml command is ok '''
#        if done:
#            '''If I do not want to print html '''
#            if not br:
#                htmltext = html.read()
#                lenght = len(htmltext)
#                
#                #TODO: Si potrebbe prendere da references in giu' + un pagina su in termini di rapporto #caratteri/pagina
#                #numCharForPage = lenght/2*n 
#                index = htmltext.rfind(_references)
#                htmltextRef = htmltext[index+len(_references):]
#                htmltextRef = htmltextRef.replace("\n"," ")
#                #htmltextRef = htmltextRef.decode("utf8","ignore")
#                htmltextRef = clearFromHtml(htmltextRef)
#    
#                
#    
#    
#                listOfSeparatedWord = htmltextRef.split(" ")
#    
#                
#                listOfAllWord = []
#                for each in listOfSeparatedWord:
#                    index = text.find(each)
#                    if (index <> -1):
#                        listOfAllWord.append(each)
#                        #text =  text[:index]+text[index+len(each):]
#    
#                #FIXME: Togliere gli spazio vuoti '' da listOfAllWord
#                clearText = ''
#                for each in listOfAllWord:
#                    clearText+=" " + each
#                return clearText
#            else:
#                htmltext = html.read()
#                lenght = len(htmltext)
#                
#                #TODO: Si potrebbe prendere da references in giu' + un pagina su in termini di rapporto #caratteri/pagina
#                #numCharForPage = lenght/2*n 
#                index = htmltext.rfind(_references)
#                htmltextRef = htmltext[index+len(_references):]
#                htmltextRef = htmltextRef.replace("\n"," ")
#                htmltextRef = htmltextRef.decode("utf8","ignore")
#                #htmltextRef = clearFromHtml(htmltextRef)
#    
#                
#    
#    
#                listOfSeparatedWord = htmltextRef.split(" ")
#    
#                
#                listOfAllWord = []
#                for each in listOfSeparatedWord:
#                    word = clearFromHtml(each)
#                    index = text.find(word)
#                    if (index <> -1):
#                        listOfAllWord.append(each)
#                        #text =  text[:index]+text[index+len(word):]
#    
#                #FIXME: Togliere gli spazio vuoti '' da listOfAllWord
#                clearText = ''
#                for each in listOfAllWord:
#                    clearText+=" " + each
#                return clearText
#                
#        else:
#            print "errore nell'eseguire pdftotml"
#            return ""

            
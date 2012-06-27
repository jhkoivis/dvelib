import re
import sys
import StringIO
import xml.dom.minidom
from Exception import ReferencesNotFoundError
'''
Here is the defitions of all regular expression used by the extractor for
entries and titles. Thera are also some statistical constants for the average of the 
minimum/maximum value of the lenght of entry, estimated from a samples of articles
'''
_reQuadre = re.compile('\[[0-9]?[0-9]\]')
_reElencoPuntato = re.compile('[0-9]?[0-9]\.')
_rePunto = re.compile("\.")
_reVirgola = re.compile(",")
_minLenghtEntryRef = 70#150
_maxLenghtEntryRef = 1200#600
_references = "R ?e ?f ?e ?r ?e ?n ?c ?e ?s?"

def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

def getValueX(bbox):
    l = bbox.split(",")
    return float(l[0])


def getPlainText(document):
    '''
    Here the function that convert a list of references without a specific rule 
    for the index in a list of References with a index made by number between 
    square parentesis
    
    @param document: the pdf in XML form
    @return: a string wellformed
    '''
    
    dom = xml.dom.minidom.parseString(document)
    textListReverse = dom.getElementsByTagName("text")
    textList = dom.getElementsByTagName("text")
    lenght = len(textList)
    textListReverse.reverse()
    
    tmpTxt=''
    first = -1
    
    '''
    Here look for the Dom text nodes that contains "References" keyword
    '''
    for i in range(lenght):
        reverseText = getText( textListReverse[i].childNodes )
        tmpTxt=  reverseText+ ' ' + tmpTxt
        r = re.compile(_references)
        m = r.search(tmpTxt)
        if m:
            ref = m.group()
            spaces=ref.count(" ")
            first = lenght - i  + spaces
            break
    '''
    Here we get "References" in the text if first is different from -1
    '''
    if first == -1:
        #print "Unable to find ref"
        raise ReferencesNotFoundError
        return None
    else:
        plaintxt = ""
        txt = getText(textList[first].childNodes )
        bboxAttr = textList[first].attributes["bbox"].value
        #print textList[first].toxml()
        if (txt.find("[1]"))<>-1:
            plaintxt+=txt
            for i in range(first+1,lenght):
                txt = getText( textList[i].childNodes )
                if len(txt) > 0:
                        plaintxt+= " " + txt
            return plaintxt.encode('ascii','ignore')
        else:
            if (txt.find("1.") <> -1):
                txt = txt.replace("1.","[1]")
                plaintxt+=txt
                j=2
                r = re.compile(" ?[0-9]?[0-9]\.")
                for i in range(first+1,lenght):
                    txt = getText( textList[i].childNodes )
                    #swapping
                    bboxAttr_p = bboxAttr
                    txt_p = txt
                    x_p = getValueX(bboxAttr_p)
                    
                    bboxAttr = textList[i].attributes["bbox"].value
                    txt = getText( textList[i].childNodes )
                    x = getValueX(bboxAttr)
                    
                    m = r.match(txt)
                    
                    if (m):
                        s = m.group()
                        s = s.replace(".","")
                        s = s.replace(" ","")
                                        
                    if len(txt) > 0 and (x - x_p < 0) and (m <> None) and int(s)>=j:
                        j=int(s)
                        txt = txt.replace(str(j)+".", "[" + str(j) +"]")
                        plaintxt+=" "+txt
                        j+=1
                    else:
                        plaintxt+=" " + txt
                return plaintxt.encode('ascii','ignore')
            else:
                plaintxt+="[1] "+txt
                j=2
                r = re.compile("[A-Z]")
                for i in range(first+1,lenght):
                    #swapping
                    bboxAttr_p = bboxAttr
                    txt_p = txt
                    x_p = getValueX(bboxAttr_p)
                    
                    bboxAttr = textList[i].attributes["bbox"].value
                    txt = getText( textList[i].childNodes )
                    x = getValueX(bboxAttr)
                    
                    if (len(txt) > 0) and (x - x_p) < 0 and ( txt_p.endswith('.') ) and ( r.match(txt) <> None ):
                                plaintxt+="["+str(j)+"] " +txt
                                j+=1
                    else:
                        plaintxt= plaintxt+" "+ txt
                return plaintxt.encode('ascii','ignore')
                    
                    
def estimateCharsForEntry(textRef):
    '''Here the function that estimate the stats from a samples of articles
    like average of  the lenght of a entry, minimum and maximum
    
    @param textRef: the text with the references
    @return the min and max of the average of the ref
    '''
    
    listaRef = _reQuadre.split(textRef)
    
    lenght = len(listaRef)
    listaRef.sort(PdfToText.compareString)
    max = len(listaRef[lenght -1 ])
    min = len(listaRef[0])

    
    return (min,max)
        


def entriesExtractor(plaintext):
    '''An important function of the application. It takes the text with the references
    and try to classify the refences with the three type:
        1. B{[1]} N.Surname, N2.Surname2. Title. Conference. Year 2008. Pages 98-100
        2. B{1.}  N.Surname, N2.Surname2. Title. Conference. Year 2008. Pages 98-100
        3.        N.Surname, N2.Surname2. Title. Conference. Year 2008. Pages 98-100
    Once that the type is classified the refernces are splitted into a lista one by one
    through the regular expressions.
    
    @param textRef: the text with the references
    @return the list of all entries of references
    '''
    
    #type = classifier(textRef)
    listaRef = []
    
    
    '''Switching on the kind suggested by the classifier'''
#   if type  == "[X]":
    listaRef = _reQuadre.split(plaintext)
#    elif type == "X.":
#        listaRef = _reElencoPuntato.split(textRef)
#    elif type == "Y":
#        textRef = getWellFormedTxt(document)
#        listaRef = _reQuadre(textRef)
                                           
    '''Clearing the list'''
    listaClearRef = []
    for i in range(len(listaRef)):
        if listaRef[i] <> " ":
            listaClearRef.append(listaRef[i])
    return listaClearRef
        


def titleExtractor(listOfEntries):

    mediaLista = []
    entry = []
    subentry = [] 
    
    for i in range(len(listOfEntries)):
        #print (str(i)+"***--->"+listaRegexp[i].replace('.<br>','')+lista[i])
        entry = _rePunto.split(listOfEntries[i])
        count = 0
        j = 0
        media = 0
        for each in entry:
            #print ">>>: "+str(len(each)) +" "+ each
            subentry = _reVirgola.split(each)
    
            for eacSub in subentry:
                j+=1
                count+= len(eacSub)
                #print str(len(each2))+  " *"+each2+"*"
                #print ">>> " + each2
            
        media = count / j
        mediaLista.append(media)
    
    titleList = []
    #print mediaLista
    found = False
    for i in range(len(listOfEntries)):
        entry = _rePunto.split(listOfEntries[i])
        for each in entry:
            if (not found):
                subentry = _reVirgola.split(each)
                for eachSub in subentry:
                    if mediaLista[i] <> 0:
                        if ( (len(eachSub)/mediaLista[i] ) > 1 ):
                            titleList.append(eachSub)
                            found=True
                            break
            else:
                found = False
                break

    return titleList

def classifier(textRef):
    '''Here is the classifier mantioned in the extractor of entries.
    The classification is done through the values min and max computed
    in the statistic way from the collection of articles.
    We check if the ratio of numbers of char on entries is considerable a reasonable value.
    In this case it means that the current regular expression has worked well.
    
    @param textRef: the text with the references
    @return the kind of the references
    '''
    

    listaRefQuadre =  _reQuadre.findall(textRef)
    listaRefElencoPuntato =  _reElencoPuntato.findall(textRef)
    
    
    
    if len(listaRefQuadre) <> 0:
        nCharsForEntry_Q = len(textRef) / len(listaRefQuadre)
    
    if len(listaRefElencoPuntato) <> 0:
        nCharsForEntry_P = len(textRef) / len(listaRefElencoPuntato)

    
    if (len(listaRefQuadre) <> 0  and nCharsForEntry_Q > _minLenghtEntryRef): 
        #print "Applying the heuristic with regular expressions based on [X]"
        return "[X]"
    
    elif ( len(listaRefElencoPuntato) <> 0  and nCharsForEntry_P > _minLenghtEntryRef):# and nCharsForEntry_P < _maxLenghtEntryRef  ): 
        #print "Applying the heuristic with regular expressions based on X."
        return "X."
    else:
        return "Y"
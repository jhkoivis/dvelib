#!/usr/bin/python
# -*- coding: utf-8 -*-

import pdf2txt
import sys
import StringIO
import xml.dom.minidom


def getTextFromPdf(filepath):
    '''
    It is the binding from the Pdfminer application and Pdftoref one.
    It returns the text extract from the PDF using the Pdfminer application.
    Witouth parameter is return the text. With the xml parameter return text in xml format.
    
    @param resultInXml: the param to switch to text from xml
    @return: the text or xml of the pdf
    '''
    debug=0
    pages=set()
    codec = 'ascii'
    password = ''
    cmapdir = 'CMap'
    cdbcmapdir = 'CDBCMap'
    outfp = StringIO.StringIO()
    
    pdf2txt.CMapDB.initialize(cmapdir, cdbcmapdir, debug=debug)
    rsrc = pdf2txt.PDFResourceManager(debug=debug)
    
    pdf2txt.pdf2txt(outfp, rsrc, filepath, pages, codec, password=password, debug=debug)
    
    document = outfp.getvalue()
    outfp.close()
    
    dom = xml.dom.minidom.parseString(document)
    textList = dom.getElementsByTagName("text")   
    
    txt = " "
    for text in textList:
        childs = text.childNodes
        for child in childs:
            txt += ' ' + child.toxml().encode('ascii','ignore')
        #print text.toxml().encode('ascii','ignore')
    
    return document


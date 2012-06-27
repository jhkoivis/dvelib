from SOAPpy import SOAPProxy
from SOAPpy import Types
import urllib2
import socket

# CONSTANTS
_url = 'http://api.google.com/search/beta2'
_namespace = 'urn:GoogleSearch'


# need to marshall into SOAP types
SOAP_FALSE = Types.booleanType(0)
SOAP_TRUE = Types.booleanType(1)

# Google search options
_license_key = 'Cu7YX75QFHLS3WD/7/4CO+GsI/jC69eb' 
_query = ""
_start = 0
_maxResults = 10
_filter = SOAP_FALSE
_restrict = ''
_safeSearch = SOAP_FALSE
_lang_restrict = ''

def googleSearch(title):
    '''
    It is the function of the application that make the request at google WS using
    getting the first url of response.
    
    @param title: the title of the article to serach for
    @return: the first url
    '''
    
    _query=title

    
    # create SOAP proxy object
    google = SOAPProxy(_url, _namespace)
    

    
    # call search method over SOAP proxy
    results = google.doGoogleSearch( _license_key, _query, 
                                     _start, _maxResults, 
                                     _filter, _restrict,
                                     _safeSearch, _lang_restrict, '', '' )
               
    # display results
#    print 'google search for  " ' + _query + ' "\n'
#    print 'estimated result count: ' + str(results.estimatedTotalResultsCount)
#    print '           search time: ' + str(results.searchTime) + '\n'
#    print 'results ' + str(_start + 1) + ' - ' + str(_start + _maxResults) +':\n'
                                                           
    numresults = len(results.resultElements)
    if numresults:
        url = results.resultElements[0].URL
    else:
        url= "#"
    return url
    

    
#    for i in range(numresults):
#        title = results.resultElements[i].title
#        noh_title = title.replace('<b>', '').replace('</b>', '')
#        print 'title: ' + noh_title
#        print '  url: ' + results.resultElements[i].URL + '\n'


def getBibTex(url):
    '''
    It is the function of the application that serach the bibxtex entry in the url 
    provided by Google WS. 
    The function switch on each site and for each site it makes a particular search.
    
    @param url: the url where start to serach
    @return: the string with the bibtex entry
    '''
       
    # timeout in seconds
    timeout = 5
    socket.setdefaulttimeout(timeout)
    html = openUrl(url)
    if html:
        #FIXME: finish the retreival
        #FIXME: Insert the timeout
        if url <> "#":
            if url.find("citeseer.ist.psu.edu") <> -1:
                bibtex = "BibTeX"
                index = html.find(bibtex)
                if index <> -1:
                    html = html[index:]
                    index = html.find("@")
                    html = html[index:]
                    index = html.find("}</pre>")
                    html = html[:index+1]
                    return html
                else:
                     return None
            elif url.find("doi.ieeecomputersociety") <> -1:
                index = html.find("Popup.document.write(\'@")
                if index <> -1:
                    html = html[index+len("Popup.document.write(\'"):]
                    index = html.find("}')")
                    html = html[:index+1]
                    return html.replace("&nbsp;"," ").replace("<xsl:text>","").replace("<br/>","\n")
                else:
                    return None
            elif url.find("portal.acm.org") <> -1:
                index = html.find("window.open('popBibTex")
                if index <> -1:
                    html = html[index+len("window.open('"):]
                    index = html.find(",'BibTex',")
                    html = html[:index]
                    html = openUrl("http://portal.acm.org/"+html)
                    html = html[html.find('@')-1:]
                    html = html[:html.find('}\r\n</pre>')-1:]
                    return html
                else:
                    return None
            
            
            
            
    return None


def openUrl(url):
    '''
    It is the function that get the html from the specific url 
    using urllib2 python library.
    
    @param url: the url to connect to
    @return: the html of the page in the url
    '''
    
    html=''
    try:
            if url <> "#":
                website = urllib2.urlopen(url)
                html = website.read()
                return html
            else:
                return None
    except (urllib2.URLError, socket.timeout):
        print "\n\n\t~ The url "+url+" is in timeout. Skipping it.\n"
        return None
        


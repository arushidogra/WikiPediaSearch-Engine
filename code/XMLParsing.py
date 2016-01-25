#!/usr/bin/env python
# -*- coding: utf-8 -*-

###IMPORTS######
import sys
from datetime import datetime
import xml.sax
import re, string, timeit
import tokenise_stem
import Indexer

#####Global Declarations########

count=0
startTime=datetime.now()
final = {}
output = []

####Regex####
info_box = "\{\{Infobox (.*?\n)*? *?\}\}"
category1 = "\[ *\[ *[cC]ategory *: *(.*?) *\] *\]"
references = "== *[Rr]eferences *==(.*?\n)+?\n"
ext_links = "== *[eE]xternal [lL]inks *== *(.*?\n)+?\n"


class WikiHandler( xml.sax.ContentHandler ):

    def __init__(self):
        self.CurrentData = ""
        self.title = ""
        self.id = ""
	self.text = ""
	self.rtitle = ""
	self.t=""
	self.rt=""
	self.c=""
	self.i=""
	self.e=""
	self.r=""
	self.idd=""
	self.ans=[]

   
    def field(self,text,id):

	#print self.title
        ####INFOBOX####
	global output	
        try :
            self.i = re.search(info_box,text).group(0)
        except AttributeError:
	    self.i = ""
	#print self.i,

        ####CATEGORY####
	category=re.findall(category1,text)#list
        if len(category)!=0:
	    self.c = ""
            for j in category :
		text = text.replace(j," ")
                self.c = self.c+" "+j
        else:
            self.c = ""
	#print self.c
        
        ##REFERENCES##
        try:
	    self.r = re.search(references,text).group(0)
        except AttributeError:
            self.r = ""
	#print self.r
	
        ##EXTERNAL LINKS##
        try:
            self.e = re.search(ext_links,text).group(0)    
	except AttributeError:
	    self.e = ""

        ##BODY##
        text = text.replace(self.i," ").replace(self.r," ").replace(self.e," ").replace("Category","")
        self.b = text
	#print self.b	
	
	
	self.b = tokenise_stem.token(self.b,self.idd,'b')
	self.i = tokenise_stem.token(self.i,self.idd,'i')
        self.r = tokenise_stem.token(self.r,self.idd,'r')
	self.c = tokenise_stem.token(self.c,self.idd,'c')
	self.t = tokenise_stem.token(self.t,self.idd,'t')
	self.rt = tokenise_stem.token(self.rt,self.idd,'rt')
	self.e = tokenise_stem.token(self.e,self.idd,'e')	
	self.ans.extend(self.b)
	self.ans.extend(self.i)
	self.ans.extend(self.r)
	self.ans.extend(self.c)
	self.ans.extend(self.t)
	self.ans.extend(self.rt)
	self.ans.extend(self.e)
	self.ans.sort()
	#print self.ans
	output = self.ans
	self.ans= []
	new=[]

	for i in range(0,len(output)-1):
	    if output[i][0] != output[i+1][0]:
	        if isinstance(output[i][1] ,list):
		    pass	    
		else:
		    output[i][3] = [output[i][3]]
		    output[i][1] = [output[i][1]]

	    else:
                output[i+1][1] = [output[i+1][1]]
                output[i+1][3] = [output[i+1][3]]
	        if isinstance(output[i][1],list):
		    output[i+1][1].extend(output[i][1])
                    output[i+1][3].extend(output[i][3])

		else:
		    output[i][1] = [output[i][1]]
                    output[i][3] = [output[i][3]]
                    output[i+1][1].extend(output[i][1])
                    output[i+1][3].extend(output[i][3])

		output[i] = []  		
	
	output = filter(lambda a: a != [], output)

	if isinstance(output[-1][1],list):
	    pass
	else:
	    output[-1][1] = [output[-1][1]]
	    output[-1][3] = [output[-1][3]]	
		
	for i in output:
	    a = ""
	    for j in xrange(len(i[1])):
	         a = a + str(i[1][j]) +"(" + str(i[3][j]) + ") "
            try:
	        final[i[0]] = final[i[0]] + " | " + i[2] + "(d)" + a
	    except KeyError:
	    	final[i[0]] = i[2] + ":(d)" + a
	del output
	print "time taken for script to run is " ,datetime.now() - startTime    #time taken by the script
	self.CurrentData = ""
        self.title = ""
        self.idd = ""
	self.text = ""
	self.rtitle = ""
	self.t=""
	self.rt=""
	self.c=""
	self.i=""
	self.e=""
	self.r=""
	self.idd=""
	self.ans=[]

    def startElement(self, tag, attributes):
            self.CurrentData = tag
	    if tag == "redirect":
                self.rtitle = attributes["title"].encode('utf8')
		
    
    def endElement(self, tag):
            if self.CurrentData == "text":
		self.idd=str(self.id.encode('utf-8'))                
                self.t = self.title.encode('utf-8')
		self.rt = self.rtitle
		text1 = self.text.encode('utf-8')
                self.field(text1,self.idd)
            self.CurrentData = ""
    
    def characters(self, content):
            if self.CurrentData == "title":
                self.title = content
           
	    elif self.CurrentData == "id":
		global count                
		if count%3 == 0:
                    self.id = content
		    count = 0
                    
                count = count + 1
            
            elif self.CurrentData == "text":
                self.text += content

# SAX Parser : As the xml file size is large
def Parse(xmlFileName):
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    Handler = WikiHandler()
    parser.setContentHandler( Handler )
    parser.parse(xmlFileName)


if ( __name__ == "__main__"):
    if len(sys.argv) < 3:
		sys.stderr.write("Usage: " + sys.argv[0] + " <test_dump.xml> <test_index>\n")
		sys.exit(2)
    xmlFileName = sys.argv[1]
    Parse(xmlFileName)
    #print final
    Indexer.indexing(final,sys.argv[2])
    print "time taken for script to run is " ,datetime.now() - startTime    #time taken by the script

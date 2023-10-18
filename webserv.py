import http.server
import common
import post
#from sys import exit
import myfunc


class Handler(http.server.BaseHTTPRequestHandler):

    def setnewport(self,newPORT,querystr):
        self.newPORT = newPORT
        self.querystr = querystr       
    #

    def processing(self,queryobj):
        try:        
            postlist = queryobj._POST()
            print(postlist)

            if('request' in postlist.keys()):
                thisrequest = postlist['request']

                if thisrequest == 'close':
                    common.close = True
                    print('request to close')
                    #exit()
                #
                elif "uiportcodeword" in thisrequest:
                    print("requesting codeword")

                    if thisrequest.removeprefix("uiportcodeword=") == myfunc.CODESTR:
                        common.replyed = 1
                        returnstr = '{"port":' + str(self.newPORT) + ', "args":' + self.querystr + '}'
                        return returnstr.encode()
                    #
                    else:
                        common.replyed = 0
                        returnstr = '{"port":-1}'
                        return returnstr.encode()
                    #
                #
            #

            return myfunc.myfunc(queryobj)
        #
        except Exception as e:
            common.errormsg(title=__name__ + "_processing",message=e)
        #
    #

    def set_headers(self):
        self.send_response(200) 
        self.send_header('Content-Type', 'text/html')
        
        self.send_header('Access-Control-Allow-Origin',self.headers['Origin']) #local file sends origin header 'null'. 
        
        self.send_header('Vary','Origin')
        self.end_headers()
    #

    def do_POST(self):

        if self.client_address[0] != '127.0.0.1': #check that request comes from local computer
            return
        #

        queryobj = post.POST(self)

        replymsg = self.processing(queryobj) #,self.custmethod)

        self.set_headers() #set headers of response
        
        self.wfile.write(replymsg) #send bytes = write to socket

        return
    #
#

class HttpServer(http.server.HTTPServer):
    def __init__(self,address_tuple,useHandler,newPORT,querystr):
        
        self.address_tuple = address_tuple
        self.useHandler = useHandler

        super().__init__(self.address_tuple,self.useHandler)
        
        useHandler.setnewport(useHandler,newPORT,querystr)
    #

    def run_once(self):      
        try:
            self.handle_request()
        #
        except Exception as e:
            common.errormsg(title=__name__ + "_HttpServer",message=e)
        #
    #
    
    def close(self):
        self.server_close()
    #

    def run_continuously(self):
        self.serve_forever()
    #
#

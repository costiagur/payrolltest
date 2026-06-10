import http.server
import common
import post
#from sys import exit
import myfunc
import ctypes
from platform import system
import os
from pathlib import Path


class Handler(http.server.BaseHTTPRequestHandler):

    def setnewport(self,newPORT,querystr):
        self.newPORT = newPORT
        self.querystr = querystr       
    #

    def processing(self,queryobj):
        #try:        
            postlist = queryobj._POST()
            print(postlist)

            if('request' in postlist.keys()):
                thisrequest = postlist['request']

                if thisrequest == 'close':
                    common.close = True
                    print('request to close')
                    return b''
                else:
                    return myfunc.myfunc(queryobj)
                #
            #
        #
        #except Exception as e:
        #    common.errormsg(title=__name__ + "_processing",message=e)
        #
    #

    def set_headers(self):
        self.send_response(200) 
        self.send_header('Content-Type', 'text/html')
        
        self.send_header('Access-Control-Allow-Origin',self.headers['Origin']) #local file sends origin header 'null'. 
        
        self.send_header('Vary','Origin')
        self.end_headers()
    #

    def do_GET(self):
        if self.client_address[0] != '127.0.0.1': #check that request comes from local computer
            return
        #

        # Handle root path
        if self.path == '/' or self.path == '':
            filepath = 'index.html'
        else:
            filepath = self.path.lstrip('/')
        #

        # Prevent directory traversal attacks
        base_dir = Path(self.server.base_dir)
        full_path = (base_dir / filepath).resolve()
        
        if not str(full_path).startswith(str(base_dir)):
            self.send_error(403)  # Forbidden
            return
        #

        if full_path.is_file():
            try:
                with open(full_path, 'rb') as f:
                    content = f.read()
                #

                self.send_response(200)
                
                # Determine content type based on file extension
                ext = full_path.suffix.lower()
                content_types = {
                    '.html': 'text/html',
                    '.js': 'application/javascript',
                    '.css': 'text/css',
                    '.json': 'application/json',
                    '.png': 'image/png',
                    '.jpg': 'image/jpeg',
                    '.jpeg': 'image/jpeg',
                    '.gif': 'image/gif',
                    '.svg': 'image/svg+xml',
                    '.ico': 'image/x-icon',
                }
                content_type = content_types.get(ext, 'application/octet-stream')
                self.send_header('Content-Type', content_type)
                self.send_header('Content-Length', len(content))
                self.end_headers()
                self.wfile.write(content)
            #
            except Exception as e:
                common.errormsg(title=__name__ + "_do_GET", message=e)
                self.send_error(500)
            #
        else:
            self.send_error(404)  # Not Found
        #
    #

    def do_POST(self):

        if self.client_address[0] != '127.0.0.1': #check that request comes from local computer
            return
        #

        queryobj = post.POST(self)

        replymsg = self.processing(queryobj)
        if replymsg is None:
            replymsg = b''   # guard against None

        self.set_headers() #set headers of response
        
        self.wfile.write(replymsg) #send bytes = write to socket

        return
    #
#

class HttpServer(http.server.HTTPServer):
    def __init__(self,address_tuple,useHandler,newPORT,querystr,base_dir):
        
        self.address_tuple = address_tuple
        self.useHandler = useHandler
        self.base_dir = base_dir

        super().__init__(self.address_tuple,self.useHandler)
        
        useHandler.setnewport(useHandler,newPORT,querystr)
    #

    def run_once(self):      
        try:
            self.handle_request()
            if system() == 'Windows':
                ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
            #
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

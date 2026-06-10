import webserv
import webbrowser
import os
from sys import argv
import ctypes
import common
from platform import system
import socket
import uiclientjs

def main():

    common.intiate()
    HOST = '127.0.0.1'


    def find_free_port(): #Find a random free TCP port
    
        for newport in range(50000,59999,1):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind((HOST, newport))  
                    return s.getsockname()[1]

            except PermissionError as e:
                pass
            #
            except OSError as e:
                if e.errno == 98:
                    pass
            #
        #
        raise RuntimeError("No free port found in range 50000-59999")
    #

    newPORT = find_free_port()


    print(argv)

    try:
        if len(argv) == 1:
            querystr = 'null'
        else:
            arglist = []

            for eacharg in argv[1:]:
                if ":" in eacharg:
                    argarr = eacharg.split(":")
                    arglist.append('"' + str(argarr[0]) + '":"' + str(argarr[1]) + '"')
            #
            if len (arglist) != 0:
                querystr = "{" + ",".join(arglist) + "}"
            else:
                raise RuntimeError("Argument string is malwritten. No :")
            #
        #

        currentfolder =  os.path.dirname(os.path.realpath(__file__))

        if system() == 'Windows':
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        #

        serv = webserv.HttpServer((HOST,newPORT),webserv.Handler,newPORT,querystr,currentfolder)
        
        uiclientjs.uiclientjs(newPORT,currentfolder)

        htmlfilepath = f"http://{HOST}:{newPORT}"

        webbrowser.open(htmlfilepath) #open html file of the UI

        while common.close == False:
            serv.run_once()
        #
        print("Closing")
        serv.close()
    #
    except Exception as e:
        common.errormsg(title=__name__,message=e)
    #

    finally:
        common.root.destroy()
    #

    common.root.mainloop()
#

if __name__ == "__main__":
    main()
#


import webserv
import webbrowser
import os
from sys import argv
import random
import ctypes
import common
from platform import system
9
def main():

    common.intiate()

    HOST = '127.0.0.1'
    iniPORT = 50000
    newPORT = random.randint(50000,60000)

    print(argv)

    try:
        if len(argv) == 1:
            querystr = 'null'
        else:
            arglist = []

            for eacharg in argv[1:]:
                argarr = eacharg.split(":")
                arglist.append('"' + str(argarr[0]) + '":"' + str(argarr[1]) + '"')
            #

            querystr = "{" + ",".join(arglist) + "}"
        #

        currentfolder =  os.path.dirname(os.path.realpath(__file__))

        if system() == 'Windows':
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        #

        htmlfilepath = "file://" + currentfolder + "/index.html"

        webbrowser.open(htmlfilepath) #open html file of the UI

        serv = webserv.HttpServer((HOST,iniPORT),webserv.Handler,newPORT,querystr)

        while common.replyed == 0:
            if common.close == False:
                print("trying connection")
                serv.run_once()
            
            elif common.close == True: #in case connection wasn't established and browser was closed
                serv.close()
                return
            #
        #

        serv.close()
        serv = webserv.HttpServer((HOST,newPORT),webserv.Handler,newPORT,querystr)
        
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

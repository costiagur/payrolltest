import base64
import json
import common
import pandas as pd
import numpy as np
from io import BytesIO
from os import unlink
import concurrent.futures
from openpyxl import Workbook
from totalrep import totalrep
from pubtrasport_nowork import pubtrasport_nowork
from semel_ratio import semel_ratio
from BasisvsCalculated import BasisvsCalculated
from semel_payhours import semel_payhours
from semel_konenut import semel_konenut
from semel_hourdeduct import semel_hourdeduct
from semel6666 import semel6666
from hightax import hightax
from semelonce import semelonce
from grosscur import grosscur
from grossretro import grossretro
from fundsprovision import fundsprovision
from licinsveh import licinsveh
from hoursWithoutYesod import hoursWithoutYesod
from manyhours import manyhours
from highgrossbtl import highgrossbtl
from semeltwice import semeltwice
from before9months import before9months
from fundsreplace import fundsreplace
from NonreasonableNett import NonreasonableNett
import custom
from loaddf import loaddf

CODESTR = "hazuticheck"

def myfunc(queryobj):
#    try:
        postdict = queryobj._POST()
        filesdict = queryobj._FILES()      

        request = postdict["request"]
        
        if request == "fileupload":
            res = loaddf(filesdict)
            replymsg = json.dumps(["uploadedrows",res]).encode('UTF-8')
                
        elif request == "salarycheck":
            
            custom.xlresfile = ".\\drafts\\" + custom.REFMONTH.strftime("%Y-%m") + ".xlsx"
            wb = Workbook()
            wb.save(custom.xlresfile)

            reqtest = postdict["reqtest"]
            reqlevel = postdict["reqlevel"]
                        
            checkpool = {}

            checkpool["semel_konenut"] = [semel_konenut,"מספר עובדים בחוזה אישי שקיבלו כוננות"]
            checkpool["semel_payhours"] = [semel_payhours, "מספר עובדים שכמות שעות עבודה לפי שעות מעל חודש מלא"]
            checkpool["semel_hourdeduct"] = [semel_hourdeduct, "מספר עובדים עם הפחתות שעות גדולות"]
            checkpool["pubtrasport_nowork"] = [pubtrasport_nowork, "עובדים עם נסיעות ללא שכר"]
            checkpool["semel6666"] = [semel6666, "מספר מקרים של אי שוויון בין סמל 6666 לסמל 6667"]
            checkpool["semel_ratio"] = [semel_ratio, "מספר עובדים עם חלקיות מעל 100%"]
            checkpool["BasisvsCalculated"] = [BasisvsCalculated,"מספר עובדים עם בסיס פנסיה לא סביר ביחס לערך שעה וחלקיות"]
            checkpool["licinsveh"] = [licinsveh, "מקרים של ביטוח רכב בסכום חורג"]
            checkpool["semelonce"] = [semelonce,"מספר מקרים של סמל שמופיע פעם אחת"]
            #checkpool["grosscur"] = [grosscur,"מספר עובדים עם הפרשי ברוטו גדולים"]
            checkpool["hightax"] = [hightax,"מספר עובדים עם שיעור מס וביטוח לאומי חריגים"]
            #checkpool["grossretro"] = [grossretro,"מספר מקרים של הפרשי רטרו גבוהים"]
            checkpool["fundsprovision"] = [fundsprovision,"מספר עובדים עם קופות חריגות"]
            checkpool["hoursWithoutYesod"] = [hoursWithoutYesod,"מספר עובדים שיש נוכחות אך אין שכר יסוד"]
            checkpool["manyhours"] = [manyhours,"מספר עובדים עם כמות שעות גבוהה מדי"]
            checkpool["highgrossbtl"] = [highgrossbtl,"מספר עובדים עם ברוטו ביטוח לאומי מעל לתקרה"]
            #checkpool["semeltwice"] = [semeltwice,"סמל שמופיע מספר פעמים באותו תאריך ערך - {}"]
            checkpool["before9months"] = [before9months,"מספר עובדים עם ממשק שלילי להפרשות או ניכויים בדיעבד מעל 9 חודשים"]
            checkpool["totalrep"] = [totalrep,"דוח השוואה כולל"]
            checkpool["NonreasonableNett"] = [NonreasonableNett,"סכומי נטו לא סבירים ביחס רוחבי"]


            if reqtest == "grosscur" or reqtest == "grossretro":
                pass
            else:
                res = [reqtest,checkpool[reqtest][0](reqlevel),checkpool[reqtest][1]]
            #

            if res[0] == "totalrep": 
                replymsg = json.dumps([res[0],res[1]]).encode('UTF-8')
            #
            else:
                replymsg = json.dumps([res[0],res[1],res[2]]).encode('UTF-8')
            #

        elif request == "testfile":
                        
            with open(custom.xlresfile,"rb") as f:
                file64enc = base64.b64encode(f.read())
                file64dec = file64enc.decode()
                replymsg = json.dumps(["testfile",f.name,file64dec]).encode('UTF-8')
            #
                
            unlink(custom.xlresfile)

        #

        elif request == "fundscheck":   

            buff = BytesIO(filesdict['fundsfile'][1])

            resfile = fundsreplace(buff)
                        
            with open(resfile,"rb") as f:
                file64enc = base64.b64encode(f.read())
                file64dec = file64enc.decode()
                replymsg = json.dumps([f.name,file64dec]).encode('UTF-8')
            #
                
            unlink(resfile)
        #
        
        return replymsg
 
            # reply message should be encoded to be sent back to browser ----------------------------------------------
            # encoding to base64 is used to send ansi hebrew data. it is decoded to become string and put into json.
            # json is encoded to be sent to browser.
            #    file64enc = base64.b64encode(filesdict['doc1'][1])
            #    file64dec = file64enc.decode()
  

    #
    
#    except Exception as e:
#        common.errormsg(title=__name__,message=e)
#        replymsg = json.dumps(["Error","myfunc -" + str(e)]).encode('UTF-8')
#        return replymsg
    #
#
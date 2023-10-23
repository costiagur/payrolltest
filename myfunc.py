import base64
import json
import common
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
from io import BytesIO
from os import unlink
import concurrent.futures
from semel1616 import semel1616
from semel90148 import semel90148
from semel91025 import semel91025
from semel100 import semel100
from semel65 import semel65
from semel119 import semel119
from semel6666 import semel6666
from semeltax import semeltax
from semelonce import semelonce
from grosscur import grosscur
from grossretro import grossretro
from fundsdeduct import fundsdeduct
from semel149150 import semel149150

CODESTR = "hazuticheck"

def myfunc(queryobj):
#    try:
        postdict = queryobj._POST()

        requestlist = json.loads(postdict["requestlist"])
        reqlevel = json.loads(postdict["reqlevel"])

        filesdict = queryobj._FILES()       

        buff = BytesIO(filesdict['hazuti'][1])

        cols = list(range(5,21,1))
        cols.append(3)
        cols.remove(12)
        cols.remove(13)
        cols.remove(14)
        df = pd.read_csv(buff,sep='\t',header=3,encoding="cp1255",na_filter=True,skip_blank_lines=True,skiprows=[5],usecols=cols,parse_dates=['Reference date','Start date'],dayfirst=True)
        df.dropna(axis=0,subset=['Amount','Quantity','Amount.1','Quantity.1'],inplace=True)
        df.rename(columns={"Employee #":"Empid","M.N.":"mn","Type of component":"Elemtype","Name of component":"Elem","Amount":"PrevAmount","Quantity":"PrevQuantity","Amount.1":"CurAmount","Quantity.1":"CurQuantity","Reference date":"Refdate"},inplace=True)
        df["Rank"] = df["Rank"].str.extract('(\d+)')
        
        refmonth = df["Refdate"].max()
        prevmonth = refmonth.replace(year = refmonth.year -1) if refmonth.month == 12 else refmonth.replace(month=refmonth.month-1)

        xlwriter = pd.ExcelWriter("{}{}{}".format("drafts\\",refmonth.strftime("%Y-%m"),".xlsx"))

        print(df.head(10))

        infoobj = common.infopopup() #common.root
       
        checkpool = {}

        checkpool["semel65"] = [semel65,"מספר עובדים בחוזה אישי שקיבלו כוננות -{}"]
        checkpool["semel100"] = [semel100, "מספר עובדים שכמור סמל 100 מעל חודש מלא - {}"]
        checkpool["semel119"] = [semel119, "מספר עובדים עם הפחתות שעות גדולות - {}"]
        checkpool["semel1616"] = [semel1616, "עובדים עם נסיעות ללא שכר -{}"]
        checkpool["semel6666"] = [semel6666, "מספר מקרים של אי שוויון בין סמל 6666 לסמל 6667 - {}"]
        checkpool["semel90148"] = [semel90148, "מספר עובדים עם חלקיות מעל 100% -{}"]
        checkpool["semel91025"] = [semel91025,"מספר עובדים עם בסיס פנסיה לא סביר ביחס לערך שעה וחלקיות -{}"]
        checkpool["semel149150"] = [semel149150, "מקרים של ביטוח רכב בסכום חורג - {}"]
        checkpool["semelonce"] = [semelonce,"מספר מקרים של סמל שמופיע פעם אחת - {}"]
        checkpool["grosscur"] = [grosscur,"מספר עובדים עם הפרשי ברוטו גדולים - {}"]
        checkpool["semeltax"] = [semeltax,"מספר עובדים עם שיעור מס וביטוח לאומי גבוהים - {}"]
        checkpool["grossretro"] = [grossretro,"מספר מקרים של הפרשי רטרו גבוהים - {}"]
        checkpool["fundsdeduct"] = [fundsdeduct,"מספר עובדים עם קופות חריגות - {}"]

        pool = concurrent.futures.ThreadPoolExecutor(max_workers=3)   
        heavyprocess = []

        for reqestcheck in requestlist:
            if reqestcheck in ["semel91025","grosscur", "grossretro"]:
                heavyprocess.append(pool.submit(checkpool[reqestcheck][0],df,xlwriter,refmonth,prevmonth,reqlevel[reqestcheck+"_level"]))

            else:
                res = checkpool[reqestcheck][0](df,xlwriter,refmonth,prevmonth,reqlevel[reqestcheck+"_level"])
                infoobj.show(checkpool[reqestcheck][1].format(res))
            #
        #

        for hp in concurrent.futures.as_completed(heavyprocess):
             res = hp.result()
             infoobj.show(checkpool[res[1]][1].format(res[0]))
        #

        pool.shutdown(wait=True)

        xlwriter.close()
        infoobj.close()       

        #print("POST = " + str(postdict) + "\n")
        #print("FILES = " + str(filesdict) + "\n")

        # reply message should be encoded to be sent back to browser ----------------------------------------------
        # encoding to base64 is used to send ansi hebrew data. it is decoded to become string and put into json.
        # json is encoded to be sent to browser.

        if bool(filesdict):
        #    file64enc = base64.b64encode(filesdict['doc1'][1])
        #    file64dec = file64enc.decode()
            
            with open("drafts\\"+ refmonth.strftime("%Y-%m") +".xlsx","rb") as f:
                file64enc = base64.b64encode(f.read())
                file64dec = file64enc.decode()
                replymsg = json.dumps([f.name,file64dec]).encode('UTF-8')
            #
            unlink("drafts\\"+ refmonth.strftime("%Y-%m") +".xlsx")
        #
        else: #if filesdict is empty
            replymsg = json.dumps(["Error","No file provided"]).encode('UTF-8')
        #
        
        return replymsg
    #
    
#    except Exception as e:
#        common.errormsg(title=__name__,message=e)
#        replymsg = json.dumps(["Error","myfunc -" + str(e)]).encode('UTF-8')
#        return replymsg
    #
#
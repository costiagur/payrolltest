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
    try:
        postdict = queryobj._POST()

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

        common.infoobj = common.infopopup() #common.root

        pool = concurrent.futures.ThreadPoolExecutor(max_workers=5)
       
        t_semel91025 = pool.submit(semel91025,df,xlwriter,refmonth,prevmonth)
        t_semeltax = pool.submit(semeltax,df,xlwriter,refmonth,prevmonth)
        t_grosscur = pool.submit(grosscur,df,xlwriter,refmonth,prevmonth)
        t_grossretro = pool.submit(grossretro,df,xlwriter,refmonth,prevmonth)
        t_fundsdeduct = pool.submit(fundsdeduct,df,xlwriter,refmonth,prevmonth)

        
        common.infoobj.show("עובדים עם נסיעות ללא שכר -{}".format(semel1616(df,xlwriter,refmonth,prevmonth)))

        common.infoobj.show("מספר עובדים עם חלקיות מעל 100% -{}".format(semel90148(df,xlwriter,refmonth,prevmonth)))

        common.infoobj.show("מספר עובדים שכמור סמל 100 מעל חודש מלא - {}".format(semel100(df,xlwriter,refmonth,prevmonth)))

        common.infoobj.show("מספר עובדים בחוזה אישי שקיבלו כוננות -{}".format(semel65(df,xlwriter,refmonth,prevmonth)))

        common.infoobj.show("מספר עובדים עם הפחתות שעות גדולות - {}".format(semel119(df,xlwriter,refmonth,prevmonth)))

        common.infoobj.show("מספר מקרים של אי שוויון בין סמל 6666 לסמל 6667 - {}".format(semel6666(df,xlwriter,refmonth,prevmonth)))

        common.infoobj.show("מספר מקרים של סמל שמופיע פעם אחת - {}".format(semelonce(df,xlwriter,refmonth,prevmonth)))

        common.infoobj.show("מקרים של ביטוח רכב בסכום חורג - {}".format(semel149150(df,xlwriter,refmonth,prevmonth)))
       
        
        common.infoobj.show("מספר עובדים עם בסיס פנסיה לא סביר ביחס לערך שעה וחלקיות -{}".format(t_semel91025.result()))      
        common.infoobj.show("מספר עובדים עם שיעור מס וביטוח לאומי גבוהים - {}".format(t_semeltax.result()))
        common.infoobj.show("מספר עובדים עם הפרשי ברוטו גדולים - {}".format(t_grosscur.result()))
        common.infoobj.show("מספר מקרים של הפרשי רטרו גבוהים - {}".format(t_grossretro.result()))
        common.infoobj.show("מספר עובדים עם קופות חריגות - {}".format(t_fundsdeduct.result()))
        
        pool.shutdown(wait=True)

        xlwriter.close()
        common.infoobj.close()       

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
    
    except Exception as e:
        common.errormsg(title=__name__,message=e)
        replymsg = json.dumps(["Error","myfunc -" + str(e)]).encode('UTF-8')
        return replymsg
    #
#
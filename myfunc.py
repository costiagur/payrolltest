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
from totalrep import totalrep
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
from semel1313 import semel1313
from semel131365 import semel131365
from semel94010 import semel94010
from semeltwice import semeltwice
from before9months import before9months

CODESTR = "hazuticheck"

def myfunc(queryobj):
#    try:
        postdict = queryobj._POST()

        requestlist = json.loads(postdict["requestlist"])
        reqlevel = json.loads(postdict["reqlevel"])

        filesdict = queryobj._FILES()       

        buff = BytesIO(filesdict['hazuti'][1])

        cols = list(range(5,21,1))
        cols = cols + [2,3]
       
        df = pd.read_csv(buff,sep='\t',header=3,encoding="cp1255",na_filter=True,skip_blank_lines=True,skiprows=[5],usecols=cols,parse_dates=['תאריך ערך','ת.ת. עבודה'],dayfirst=True)
        
        df.rename(columns={"שם עובד":"Empname","מספר עובד":"Empid","מ.נ.":"mn","אגף":"Division","סכום":"PrevAmount","כמות":"PrevQuantity",df.columns[16]:"CurAmount",df.columns[17]:"CurQuantity","תאריך ערך":"Refdate","ת.ת. עבודה":"Startdate","סוג רכיב":"Elemtype_heb","שם רכיב":"Elem_heb","דרוג":"Dirug"},inplace=True)

        df["Elem"] = df["Elem_heb"].str.extract(r'^(\d+|עלות)\s-*')
        df["Rank"] = df["Dirug"].str.extract('(\d+)')

        fromconv = ["מספר ותאור רכיבי תוספות","מספר ותאור רכיבי ניכויי חובה","מספר ותאור רכיבי ניכויי רשות","מספר ותאור רכיבי הפרשות","נתונים נוספים","מספר ותאור  רכיבי זקיפות הטבה"]
        toconv = ["addition components","compulsory deductions","voluntary deductions","provision components","additional data","benefit charge components"]

        df["Elemtype"] = df["Elemtype_heb"]
        df["Elemtype"].replace(to_replace = fromconv, value=toconv,inplace=True)

        df.dropna(axis=0,subset=['PrevAmount','PrevQuantity','CurAmount','CurQuantity'],inplace=True)
        
        refmonth = df["Refdate"].max()
        prevmonth = refmonth.replace(year = refmonth.year -1) if refmonth.month == 12 else refmonth.replace(month=refmonth.month-1)

        buff = BytesIO(filesdict['f1313'][1])

        df1313 = pd.read_csv(buff,sep='\t',header=0,encoding="cp1255",na_filter=True,skip_blank_lines=True,parse_dates=['תוקף עד','תוקף מ'],dayfirst=True,usecols=list(range(0,6,1)))
        df1313.rename(columns={"מספר זהות ":"Empid","שם עובד":"Empname","מ.נ":"mn","תוקף מ":"Refdate","תוקף עד":"Enddate","כמות":"Quantity"}, inplace=True)
        
        for _,i2,i3 in list(df1313[["Empid","mn"]].to_records()):
            df.loc[(df["Empid"] == i2)&(df["mn"] == i3)&(df["Refdate"] == refmonth)&(df["Elem"] == "1"),"CurQuantity"] =sum(df1313.loc[(df1313["Empid"] == i2)&(df1313["mn"] == i3),"Quantity"])
        #

        print(df.head(10))

        xlwriter = pd.ExcelWriter(".\\drafts\\" + refmonth.strftime("%Y-%m") + ".xlsx")
        

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
        checkpool["semel1313"] = [semel1313,"מספר עובדים שיש נוכחות אך אין שכר יסוד - {}"]
        checkpool["semel131365"] = [semel131365,"מספר עובדים עם כמות שעות גבוהה מדי - {}"]
        checkpool["semel94010"] = [semel94010,"מספר עובדים עם ברוטו ביטוח לאומי מעל לתקרה - {}"]
        #checkpool["semeltwice"] = [semeltwice,"סמל שמופיע מספר פעמים באותו תאריך ערך - {}"]
        checkpool["before9months"] = [before9months,"מספר עובדים עם ממשק שלילי להפרשות או ניכויים בדיעבד מעל לתשעה חודשים - {}"]

        pool = concurrent.futures.ThreadPoolExecutor(max_workers=3)   
        heavyprocess = []
        resdict = {}
        resdict = totalrep(df,xlwriter,refmonth,prevmonth)

        for reqestcheck in requestlist:
            if reqestcheck in ["semel91025","grosscur", "grossretro"]:
                heavyprocess.append(pool.submit(checkpool[reqestcheck][0],df,xlwriter,refmonth,prevmonth,reqlevel[reqestcheck+"_level"]))
            
            elif reqestcheck == "semel1313":
                res = semel1313(df,df1313,xlwriter,refmonth,prevmonth,reqlevel["semel1313_level"])
                infoobj.show(checkpool["semel1313"][1].format(res))

            else:
                res = checkpool[reqestcheck][0](df,xlwriter,refmonth,prevmonth,reqlevel[reqestcheck+"_level"])
                infoobj.show(checkpool[reqestcheck][1].format(res))
            #
        #

        for hp in concurrent.futures.as_completed(heavyprocess):
             res = hp.result()
             infoobj.show(checkpool[res[1]][1].format(res[0]))

             if res[1] == "grosscur":
                  pass
        #

        pool.shutdown(wait=True)

        xlwriter.close()
        infoobj.close()       

        #print("POST = " + str(postdict) + "\n")
        #print("FILES = " + str(filesdict) + "\n")

        # reply message should be encoded to be sent back to browser ----------------------------------------------
        # encoding to base64 is used to send ansi hebrew data. it is decoded to become string and put into json.
        # json is encoded to be sent to browser.
        #    file64enc = base64.b64encode(filesdict['doc1'][1])
        #    file64dec = file64enc.decode()
        
        if bool(filesdict):
                    
            with open(".\\drafts\\"+ refmonth.strftime("%Y-%m") +".xlsx","rb") as f:
                file64enc = base64.b64encode(f.read())
                file64dec = file64enc.decode()
                replymsg = json.dumps([f.name,file64dec]).encode('UTF-8')
            #
            
            unlink(".\\drafts\\"+ refmonth.strftime("%Y-%m") +".xlsx")
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
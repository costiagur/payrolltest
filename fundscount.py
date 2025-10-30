import pandas as pd
import numpy as np
import custom
import inspect
import sqlite3
import re

def fundscount(level=""):

    conn = sqlite3.connect("dbsave.db")
    cur = conn.cursor()

    def regexp(pattern, text): #REGEXP doesn't exist natively in SQLite, so we create it
        res = re.findall(pattern, text)
        if res:
            return True
        else:
            return False
    #

    conn.create_function("regexp", 2, regexp) #registering the function in the connection

    REFMONTH = cur.execute("SELECT MAX(Refdate) FROM dfcurr").fetchone()[0]

    query1 = f"SELECT Empid,mn,Empname,Elem,Amount,Startdate,Stopname,Stopfrom,Stoptill,Rank FROM dfcurr WHERE Division <> 90 AND Amount <> 0 AND Refdate = '{REFMONTH}' AND Elemtype IN ('provision components', 'voluntary deductions')"

    middf = pd.read_sql_query(query1, conn)

    #cols = ["Empid","Empname","mn","Startdate","Elem","Rank","Amount"]

    #middf = custom.DFCURR.loc[(custom.DFCURR["Division"] != 90)&(custom.DFCURR["Refdate"]==custom.REFMONTH)&(custom.DFCURR["Elemtype"].isin(("provision components","voluntary deductions")))&(custom.DFCURR["Amount"]!=0.0),cols]
       
    query2 = f"SELECT Empid,mn,Empname,Elem,Amount,Startdate,Stopname,Stopfrom,Stoptill,Rank FROM dfcurr WHERE Division = 90 AND Amount > 0 AND Refdate = '{REFMONTH}' AND Elemtype = 'provision components' " + "AND Elem REGEXP '3[0-9]{5}'"

    gimladf = pd.read_sql_query(query2, conn)

    #gimladf = custom.DFCURR.loc[(custom.DFCURR["Division"] == 90)&(custom.DFCURR["Refdate"]==custom.REFMONTH)&(custom.DFCURR["Elemtype"] == "provision components")&(custom.DFCURR["Amount"] > 0.0),cols+ ["Division"]]


    def fundnum(row):  
        resarr = [0,0,0,0,0,0]

        def impow():
            return 10**(int(row["Elem"][-1])-1)
        #

        if len(row["Elem"]) == 6 and row["Elem"][1] == '3':
            resarr[0] = impow()
        elif len(row["Elem"]) == 6 and row["Elem"][1] == '4':
            resarr[1] = impow()
        elif len(row["Elem"]) == 6 and row["Elem"][1] == '5':
            resarr[2] = impow()
        elif len(row["Elem"]) == 6 and row["Elem"][1] == '6':
            resarr[3] = impow()
        elif len(row["Elem"]) == 6 and row["Elem"][1] == '7':
            resarr[4] = impow()
        elif len(row["Elem"]) == 6 and row["Elem"][1] == '8':
            resarr[5] = impow()
        elif row["Elem"] == '30501':
            resarr[0] = impow()
        #    
        #print(resarr)
        return resarr
    #


    middf[["type3","type4","type5","type6","type7","type8"]] = middf.apply(fundnum,axis=1,result_type='expand')

    gimladf[["type3","type4","type5","type6","type7","type8"]] = gimladf.apply(fundnum,axis=1,result_type='expand')

    groupdf = middf.groupby(by=["Empid","Empname","Startdate","Rank"],as_index=False,group_keys=True).sum(["type3","type4","type5","type6","type7","type8"])
    gimlagroupdf = gimladf.groupby(by=["Empid","mn","Empname","Startdate","Rank"],as_index=False,group_keys=True).sum(["type3","type4","type5","type6","type7","type8"])

    groupdf["Msg"] = ""
    gimladf["Msg"] = "גמלאי"

    groupdf.drop(columns="mn",inplace=True)

    groupdf.loc[(groupdf["type5"]==0)&(~groupdf["Rank"].isin(('71','91'))),"Msg"] = "חסר החזר הוצאות"
    groupdf.loc[(groupdf["type5"] > 0)&(groupdf["Rank"].isin(('71','91'))),"Msg"] = "אינו זכאי לקופת החזר הוצאות"
    groupdf.loc[(groupdf["type6"]==0)&(groupdf["Rank"].isin(('141',"242","2")))&(pd.to_datetime(groupdf["Startdate"]) < pd.to_datetime(REFMONTH) + pd.DateOffset(months = -12)),"Msg"] = "חסר קרן השתלמות"
    groupdf.loc[(groupdf["type6"]==0)&(~groupdf["Rank"].isin(('141',"242","2","91"))),"Msg"] = "חסר קרן השתלמות"
    groupdf.loc[(groupdf["type3"]==0),"Msg"] = "חסרה קופת בסיס הפנסיה"
    groupdf.loc[(groupdf["type6"] > 11),"Msg"] = "כפל קרן השתלמות"
    groupdf.loc[(groupdf["type5"] > 11),"Msg"] = "כפל קופת החזר הוצאות"
    groupdf.loc[(groupdf["type8"] > 100),"Msg"] = "כפל קופת פיצויים"
    groupdf.loc[(groupdf["type8"] == 0)&(groupdf["type3"] == 1)&(groupdf["Rank"] != '185'),"Msg"] = "חסר קופת פיצויים"
    groupdf.loc[(groupdf["type8"] > 0)&(groupdf["Rank"] == '185'),"Msg"] = "לסגור קופת פיצויים"
  
### Case of Stopped Employees    

    query3 = f"SELECT DISTINCT Empid,Stopname,Stopfrom,Stoptill FROM dfcurr WHERE Stopfrom IS NOT NULL"

    stopdf = pd.read_sql_query(query3, conn)
    
    #stopdf = custom.DFCURR.loc[(~custom.DFCURR["Stopfrom"].isna()),["Empid","Stopname","Stopfrom","Stoptill"]]
    #stopdf.drop_duplicates(inplace=True)
    #stopdf.reset_index(inplace=True)

    stopdf["text"] = stopdf.apply(lambda row: f"{row['Stopname']} {row['Stopfrom']} - {row['Stoptill']}", axis=1)
    stopdf.drop(columns=["Stopname","Stopfrom","Stoptill"], inplace=True)
    stopdf.rename(columns={"text": "Stop"}, inplace=True)

    groupdf["Stop"] = groupdf.apply(lambda row: stopdf.loc[stopdf["Empid"] == row["Empid"],"Stop"].tolist(),axis=1)
    groupdf["Stop"] = groupdf["Stop"].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

    gimlagroupdf["Stop"] = gimlagroupdf.apply(lambda row: stopdf.loc[stopdf["Empid"] == row["Empid"],"Stop"].tolist(),axis=1)
    gimlagroupdf["Stop"] = gimlagroupdf["Stop"].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

    findf = pd.concat([groupdf.loc[groupdf["Msg"]!=''],gimlagroupdf],ignore_index=True)

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        findf[["Empid","Empname","Startdate","Rank","Amount","type3","type4","type5","type6","type7","type8","Msg","Stop"]].to_excel(writer,sheet_name="קופות חריגות",header=["מספר עובד","שם","תחילת_העסקה","דרוג","סכום","קופת בסיס","קופת ענ","קופת הה","קהש","עצמאי","אישית לפיצויים","הודעה","בהפסקת עבודה"],index=False)
    #  

    conn.close()

    return [inspect.stack()[0][3],findf.shape[0],"מספר קופות חריגות"]
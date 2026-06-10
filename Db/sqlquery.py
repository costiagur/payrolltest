import pandas as pd
import re
import sqlite3
import custom
import os

def sqlquery(querytxt,source,how='show'):
    dbcon = sqlite3.connect(custom.dbsave)

    if len(re.findall(r'DROP|DELETE|INSERT|UPDATE|ALTER|CREATE',querytxt,re.IGNORECASE))>0:
       raise Exception("רק שאילתות SELECT מותרות")
    elif len(re.findall(r'ERROR',querytxt,re.IGNORECASE))>0:
       raise Exception(querytxt)
    #

    reply = querytxt.replace("\n"," ")
    reply = reply.replace("sqlite","")

    reply = reply.strip()

    req = "SELECT 0"

    if source == "timeschedule":
        req = f"""WITH timeschedule as (SELECT * FROM timesheet) 
        {reply}
        """
    elif source == "hazuti":
        req = f"""WITH hazuti as (SELECT * FROM dfcurr) 
        {reply}
        """
    #

    reqdf = pd.read_sql(req,dbcon)

    dbcon.close()

    for eachcol in reqdf.columns:
        if reqdf[eachcol].sum() == 0 and reqdf[eachcol].max() == 0:
            reqdf.drop(columns=eachcol,inplace=True)
        #
        else:
            renamedict = {}
            renamedict[eachcol] = eachcol.replace("_"," ")
            reqdf.rename(columns=renamedict,inplace=True)

    #

    reqdf.loc['Total'] = round(reqdf.sum(numeric_only=True),2)
    reqdf.fillna("",inplace=True)
    reqdf.drop(columns="index",inplace=True)

    try:
        if how=='show':
            return ["Result",reqdf.to_dict('index')]
        #
        
        elif how=='xls':
            filename = custom.draftslib + '\\resoutput.xlsx'
            reqdf.to_excel(filename,index=False)
            with open(filename,'rb') as f:
                r = f.read()
            #
            os.unlink(filename)                      
            print(r)
            return r
        #
    except Exception as e:
        return ["Error",str(e)]
    #
import pandas as pd
import re
import sqlite3

def sqlquery(querytxt,how='show'):
    dbcon = sqlite3.connect('dbsave.db')

    if len(re.findall(r'DROP|DELETE|INSERT|UPDATE|ALTER|CREATE',querytxt,re.IGNORECASE))>0:
       raise Exception("רק שאילתות SELECT מותרות")
    elif len(re.findall(r'ERROR',querytxt,re.IGNORECASE))>0:
       raise Exception(querytxt)
    #

    reply = querytxt.replace("\n"," ")
    reply = reply.replace("sqlite","")
    reply = reply.strip()

    selections = re.findall(r'^SELECT\s(.*)\sFROM',reply,re.IGNORECASE)
    conditions = re.findall(r'FROM\s\w+\s(.*)$',reply,re.IGNORECASE)

    if len(re.findall(r'timesheet',querytxt,re.IGNORECASE))>0:
        req = "SELECT {} FROM timesheet {}".format(selections[0],conditions[0] if len(conditions)>0 else "")
    elif len(re.findall(r'dfcurr',querytxt,re.IGNORECASE))>0:
        req = "SELECT {} FROM dfcurr {}".format(selections[0],conditions[0] if len(conditions)>0 else "")
    #
        
    try:
        if how=='show':
            reqdf = pd.read_sql(req,dbcon)
            return ["Result",reqdf.to_dict('index')]
        elif how=='xls':
            reqdf = pd.read_sql(req,dbcon)
            filename = 'drafts/timesheet_output.xlsx'
            reqdf.to_excel(filename,index=False)
            return open(filename,'rb').read()
    except Exception as e:
        return ["Error",str(e)]
    finally:
        dbcon.close()
    #
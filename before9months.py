#בדיקה אם יש הפרשות עם רטרו מעל 9 חודשים

import pandas as pd
import custom
import inspect
import sqlite3
import re


def before9months(level=""):
    
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

    res = cur.execute("SELECT MAX(Refdate) FROM dfcurr")
    REFMONTH = res.fetchone()[0]

    query = "SELECT Empid,Empname,Refdate,Amount,Elem,Elem_heb FROM dfcurr WHERE Elemtype IN ('provision components', 'voluntary deductions') AND Elem REGEXP '3[0-9]{5}' AND Amount < 0 " + f"AND Refdate < DATE('{REFMONTH}', '-9 months')"

    middf = pd.read_sql_query(query, conn)

    conn.close()

    #middf = custom.DFCURR[(custom.DFCURR['Elemtype'].isin(("provision components","voluntary deductions")))&(custom.DFCURR['Elem'].str.contains(r'3\d{5}',regex=True))&(custom.DFCURR["Amount"]<0)&(custom.DFCURR["Refdate"] < (pd.to_datetime(custom.REFMONTH) + pd.DateOffset(months = -9)))]

    resdict = dict()
    resdict["Empid"] = []
    resdict["Empname"] = []
    resdict["Fund"] = []
    resdict["Date"] = []
    resdict["Values"] = []

    for eachid in middf["Empid"].unique():
        
        num = middf.loc[middf["Empid"] == eachid,"Elem"].count()
        
        resdict["Empid"] = resdict["Empid"] + [eachid]*num
        resdict["Empname"] = resdict["Empname"] + [middf.loc[middf["Empid"] == eachid,"Empname"].unique()[0]]*num

        resdict["Fund"] = resdict["Fund"] + middf.loc[middf["Empid"] == eachid,"Elem_heb"].to_list()
        resdict["Date"] = resdict["Date"] + middf.loc[middf["Empid"] == eachid,"Refdate"].to_list()
        resdict["Values"] = resdict["Values"] + middf.loc[middf["Empid"] == eachid,"Amount"].to_list()
    #
    
    resdf = pd.DataFrame.from_dict(resdict)
    resdf.rename(columns={"Empid":"מספר עובד","Empname":"שם","Fund":"קופה","Date":"תאריך","Values":"סכום"},inplace=True)
    
    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer,sheet_name="ניכוי קופות מעל 9 חודשים",index=False)
    #      

    return [inspect.stack()[0][3],len(resdf["מספר עובד"].unique()),"מספר עובדים עם ממשק שלילי להפרשות או ניכויים בדיעבד מעל 9 חודשים"]
#
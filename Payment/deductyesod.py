import custom
import pandas as pd
import inspect
import sqlite3

def deductyesod(level=""): #הפחתה של שכר יסוד ברטרו

    conn = sqlite3.connect(custom.dbsave)

    query = f"""SELECT dfcurr.Empid, dfcurr.Empname, dfcurr.mn, dfcurr.Refdate, dfcurr.Rank,dfcurr.Elem_heb, dfcurr.Amount, ST.Stopfrom, ST.Stoptill, ST.Stopname
    FROM dfcurr
    LEFT JOIN (SELECT dfcurr.Empid,dfcurr.Stopfrom, dfcurr.Stoptill, dfcurr.Stopname from dfcurr WHERE dfcurr.Stopname <> "" AND dfcurr.Refdate < (SELECT MAX(dfcurr.Refdate) FROM dfcurr) AND dfcurr.Elem = 1) AS ST ON ST.Empid = dfcurr.Empid 
    WHERE dfcurr.Elem = 1 AND dfcurr.Amount < 0 AND dfcurr.Refdate < (SELECT MAX(dfcurr.Refdate) FROM dfcurr)"""

    middf = pd.read_sql_query(query, conn)

    conn.close()


    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        middf.to_excel(writer,sheet_name="הפחתת יסוד ברטרו",index=False,header=["מספר עובד","שם עובד", "מנ","חודש ערך","דירוג","סמל שכר","סכום","הפסקה מ", "הפסקה עד", "שם הפסקה"])
    #             
    
    return [inspect.stack()[0][3],len(middf["Empid"].unique()),"מספר עובדים עם הפחתה של שכר יסוד ברטרו"]
# 
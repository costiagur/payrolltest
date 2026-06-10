#נטו גדול מברוטו כספי
import custom
import pandas as pd
import inspect
import sqlite3

def NettAboveGross(level = ""):
    conn = sqlite3.connect(custom.dbsave)

    query1 = f"""
    SELECT Total.Empid AS מספר_עובד,Total.Empname AS שם_עובד,Total."שם מחלקה",Total.Gross AS ברוטו, Total.Nett AS נטו, Total.Diff AS הפרש
    FROM
    (SELECT dfcurr.Empid,dfcurr.Empname,dfcurr."שם מחלקה",Round(SUM(dfcurr.Amount),0) AS Gross, ST.Amount as Nett, Round(SUM(dfcurr.Amount)-ST.Amount,0) AS Diff
    FROM dfcurr
    LEFT JOIN (SELECT dfcurr.Empid, dfcurr.Amount FROM dfcurr WHERE dfcurr.Elem = {custom.semelnett}) AS ST ON ST.Empid = dfcurr.Empid
    WHERE dfcurr.Elemtype ="addition components"
    GROUP BY dfcurr.Empid) AS total
    WHERE Total.Diff < 0
    """

    resdf = pd.read_sql_query(query1, conn)

    conn.close()

    
    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer,sheet_name="נטו גדול מברוטו",index=False, header=True)
    # 
        
    return [inspect.stack()[0][3],len(resdf),"נטו גדול מברוטו"]
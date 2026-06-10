#Payment without timesheet
import custom
import pandas as pd
import inspect
import sqlite3

def globalpay(level=""):

    conn = sqlite3.connect(custom.dbsave)

    query = f"""
    SELECT dfcurr.Empid, dfcurr.Empname, dfcurr.Elem, dfcurr.Amount
    FROM dfcurr
    WHERE dfcurr.Division<>90 AND dfcurr.Elem = 1 AND dfcurr.Refdate = (SELECT MAX(dfcurr.Refdate) FROM dfcurr) AND dfcurr.Empid NOT IN (SELECT timesheet.מספר_עובד FROM timesheet)
    """

    resdf = pd.read_sql_query(query, conn)

    conn.close()

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer,sheet_name="שכר_גלובלי",index=False)
    #             
    
    return [inspect.stack()[0][3],resdf.shape[0],"תשלום יסוד ללא נוכחות"]

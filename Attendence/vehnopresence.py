import custom
import pandas as pd
import sqlite3
import inspect

def vehnopresence(level = "3"): #Work on Shabat, not in Moked or Shitur
    conn = sqlite3.connect(custom.dbsave)
    level = int(level)

    query = f"""
    WITH timetab as (SELECT timesheet.מספר_עובד as Empid, COUNT(DISTINCT timesheet.תאריך_נוכחות) as dayscount
    FROM timesheet
    WHERE timesheet.פעילות = "עבודה"
    GROUP BY timesheet.מספר_עובד
    HAVING dayscount <= {level})
    SELECT dfcurr.Empid as מספר_עובד, dfcurr.Empname as שם_עובד, dfcurr.Elem as סמל, dfcurr.Elem_heb as שם_סמל, dfcurr.Quantity as כמות, timetab.dayscount as מספר_ימי_עבודה
    FROM dfcurr
    JOIN timetab ON dfcurr.Empid = timetab.Empid
    WHERE dfcurr.Elem = 194 AND dfcurr.Quantity > 0 AND dfcurr.Refdate = (SELECT MAX(dfcurr.Refdate) FROM dfcurr)
    """

    resdf = pd.read_sql_query(query, conn)

    with pd.ExcelWriter(custom.xlresfile, mode="a",if_sheet_exists='overlay') as writer:
        resdf.to_excel(writer,sheet_name="רכב ללא נוכחות",index=False,startrow=1,header=True)
    # 

    conn.close

    return [inspect.stack()[0][3],resdf.shape[0],"רכב ללא נוכחות"]
#

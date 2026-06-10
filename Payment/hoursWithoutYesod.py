import custom
import pandas as pd
import numpy as np
import inspect
import sqlite3

#יש דיווח של שעות עבודה לתלוש אך אין תשלום סמל שכר יסוד

def hoursWithoutYesod(level="8"):

    conn = sqlite3.connect(custom.dbsave)

    level = float(level)

    query = f"""
    SELECT 
        timesheet.מספר_עובד,שם_עובד, 
        SUM(timesheet.סהכ_לשכר) AS סך_לשכר
    FROM 
        timesheet
    WHERE 
        timesheet.מספר_עובד IN (
            SELECT מספר_עובד 
            FROM timesheet 
            GROUP BY מספר_עובד 
            HAVING SUM(סהכ_לשכר) > 8
        )
    AND timesheet.מספר_עובד NOT IN (
            SELECT Empid 
            FROM dfcurr 
            WHERE Elem IN {custom.yesodandhours} 
            AND Refdate = (SELECT MAX(Refdate) FROM dfcurr)
        )
    GROUP BY 
        timesheet.מספר_עובד"""

    resdf = pd.read_sql_query(query, conn)

    conn.close()

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer,sheet_name="שעות ללא יסוד",index=False)
    #    
    
    return [inspect.stack()[0][3],resdf.shape[0],"מספר עובדים שיש נוכחות אך אין שכר יסוד"]


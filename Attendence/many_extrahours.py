import custom
import pandas as pd
import sqlite3
import inspect


def many_extrahours(level = "44"): #פער גדול בין שעות נוכחות לרגילות

    conn = sqlite3.connect(custom.dbsave)
    level = float(level)

    query = f""" SELECT מספר_עובד, שם_עובד, SUM(סהכ_לשכר) - SUM(שעות_רגילות) - SUM(שעות_100_אינפורמטיב) as שעות_לא_רגילות  
    FROM timesheet
    WHERE פעילות  <> "כוננות"
    GROUP BY מספר_עובד
    HAVING שעות_לא_רגילות > {level}
    ORDER BY שעות_לא_רגילות DESC"""

    resdf = pd.read_sql_query(query, conn)  

    with pd.ExcelWriter(custom.xlresfile, mode="a",if_sheet_exists='overlay') as writer:
        resdf.to_excel(writer,sheet_name="ריבוי שעות לא רגילות",index=False,startrow=1,header=True)
    #  

    conn.close()

    return [inspect.stack()[0][3],resdf.shape[0],"ריבוי שעות לא רגילות"]

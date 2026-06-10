# הפחתות שעות גדולות גם רטרו.
import custom
import pandas as pd
import inspect
import sqlite3

def semel_hourdeduct(level="100"):

    conn = sqlite3.connect(custom.dbsave)

    query = f"""SELECT Empid,Empname,Refdate,Elem_heb,SUM(Quantity) as Hourdeduct FROM dfcurr WHERE Elem IN ({custom.hourdeduct}) GROUP BY Empid,Refdate Having SUM(Quantity) >= {level}"""

    middf = pd.read_sql_query(query, conn)

    conn.close()
   
    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        middf.to_excel(writer,sheet_name="הפחתת שעות גדולה",index=False,header=['מספר עובד','שם','תאריך ערך','סמל','הפחתת שעות'])
    #    

    return [inspect.stack()[0][3],len(middf),"מספר עובדים עם הפחתות שעות גדולות"]
#
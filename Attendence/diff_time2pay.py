import custom
import pandas as pd
import sqlite3
import inspect


def diff_time2pay(level = "10"): #פער בין שעות שנוכח לשעות המועברות לשכר

    conn = sqlite3.connect(custom.dbsave)
    level = float(level)

    query = f"""SELECT מספר_עובד, שם_עובד,SUM(סהכ_נוכח)-SUM(סהכ_לשכר) as הפרש_נוכח_לשכר 
    FROM timesheet
    GROUP BY מספר_עובד
    HAVING הפרש_נוכח_לשכר > {level}
    ORDER BY הפרש_נוכח_לשכר DESC"""

    resdf = pd.read_sql_query(query, conn)  

    with pd.ExcelWriter(custom.xlresfile, mode="a",if_sheet_exists='overlay') as writer:
        resdf.to_excel(writer,sheet_name="פער נוכחות לשכר",index=False,startrow=1,header=True)
    #  

    conn.close()

    return [inspect.stack()[0][3],resdf.shape[0],"פער נוכחות לשעות לשכר"]

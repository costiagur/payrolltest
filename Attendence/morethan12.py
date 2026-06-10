import custom
import pandas as pd
import sqlite3
import inspect


def morethan12(level = ""): #עבודה מעל 12 שעות

    conn = sqlite3.connect(custom.dbsave)
    if level == "":
        level = 12
    else:
        level = float(level)
    #

    query = f""" SELECT מספר_עובד, שם_עובד,תאריך_נוכחות, SUM(סהכ_לשכר) סך_לשכר 
    FROM timesheet
    WHERE פעילות  <> "כוננות"
    group by מספר_עובד, תאריך_נוכחות
    HAVING סך_לשכר > {level}
    ORDER BY סך_לשכר DESC"""

    resdf = pd.read_sql_query(query, conn)

    with pd.ExcelWriter(custom.xlresfile, mode="a",if_sheet_exists='overlay') as writer:
        resdf.to_excel(writer,sheet_name="מעל 12 שעות",index=False,startrow=1,header=True)
    #  

    conn.close()

    return [inspect.stack()[0][3],resdf.shape[0],"מעל 12 שעות"]

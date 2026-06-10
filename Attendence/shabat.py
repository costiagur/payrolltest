import custom
import pandas as pd
import sqlite3
import inspect

def shabat(level = "0"): #Work on Shabat, not in Moked or Shitur
    conn = sqlite3.connect(custom.dbsave)

    query = """
    SELECT timesheet.מספר_עובד, timesheet.שם_עובד, timesheet.שם_מחלקה, timesheet.תאריך_נוכחות, timesheet.יום, timesheet.פעילות, timesheet.סהכ_לשכר 
    FROM timesheet 
    WHERE timesheet.יום = 'ש' AND timesheet.פעילות = 'עבודה' AND timesheet.מחלקה NOT IN (761110,761000)
    """

    resdf = pd.read_sql_query(query, conn)

    with pd.ExcelWriter(custom.xlresfile, mode="a",if_sheet_exists='overlay') as writer:
        resdf.to_excel(writer,sheet_name="עבודה בשבת",index=False,startrow=1,header=True)
    # 

    conn.close

    return [inspect.stack()[0][3],resdf.shape[0],"עבודה בשבת"]
#

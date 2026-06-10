#העדרות בתשלום
import custom
import pandas as pd
import sqlite3
import inspect

def paidabscence(level = ""):
    conn = sqlite3.connect(custom.dbsave)

    query = """
   SELECT timesheet.מספר_עובד,timesheet.שם_עובד, timesheet.מחלקה as מחלקה, jobs.jobname as תפקיד, SUM(timesheet.שעות_רגילות) as העדרות_בתשלום 
    FROM timesheet
    LEFT JOIN jobs ON jobs.empid = timesheet.מספר_עובד
    WHERE timesheet.פעילות = "העדרות בתשלום" 
    GROUP BY timesheet.מספר_עובד
    HAVING העדרות_בתשלום > 0
    ORDER BY העדרות_בתשלום DESC
    """


    resdf = pd.read_sql_query(query, conn)

    with pd.ExcelWriter(custom.xlresfile, mode="a",if_sheet_exists='overlay') as writer:
        resdf.to_excel(writer,sheet_name="העדרות בתשלום",index=False,header=True)
    # 

    conn.close

    return [inspect.stack()[0][3],resdf.shape[0],"העדרות בתשלום"]
#

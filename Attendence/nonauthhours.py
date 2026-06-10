import pandas as pd
import sqlite3
import inspect
import custom

def nonauthhours(level = "10"): #עבודה מעל 10 שעות נוספות לא מאושרות

    conn = sqlite3.connect(custom.dbsave)
    level = float(level)

    query = f""" SELECT timesheet.מספר_עובד, timesheet.שם_עובד, jobs.jobname AS תפקיד, SUM(timesheet.שנ_125_לא_מאוש) AS שנ125_לא_מאושר, SUM(timesheet.שנ_150_לא_מאוש) AS שנ150_לא_מאושר
    FROM timesheet
    LEFT JOIN jobs ON jobs.empid = timesheet.מספר_עובד
    WHERE jobs.jobnum NOT IN {str(custom.managers)} 
    GROUP BY timesheet.מספר_עובד, timesheet.שם_עובד
    HAVING  SUM(timesheet.שנ_125_לא_מאוש) + SUM(timesheet.שנ_150_לא_מאוש) >= {level} 
    ORDER BY SUM(timesheet.שנ_125_לא_מאוש) + SUM(timesheet.שנ_150_לא_מאוש) Desc"""

    resdf = pd.read_sql_query(query, conn)

    with pd.ExcelWriter(custom.xlresfile, mode="a",if_sheet_exists='overlay') as writer:
        resdf.to_excel(writer,sheet_name="שנ לא מאושרות",index=False,startrow=1,header=True)
    #  

    conn.close()

    return [inspect.stack()[0][3],resdf.shape[0],"שנ לא מאושרות"]

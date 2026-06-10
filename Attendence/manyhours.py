#עובדים עם מספר שעות רב מדי
import custom
import pandas as pd
import inspect
from openpyxl import Workbook, load_workbook
import sqlite3


def manyhours(level="220"):
    
    level= float(level)

    conn = sqlite3.connect(custom.dbsave)

    query = f"""SELECT timesheet.מספר_עובד, timesheet.שם_עובד, timesheet.שם_מחלקה, SUM(MAX(timesheet.סהכ_לשכר,timesheet.שעות_רגילות)) as שעות_להעברה
    FROM timesheet 
    WHERE timesheet.פעילות <> 'כוננות'
    GROUP BY timesheet.מספר_עובד, timesheet.שם_עובד
    HAVING שעות_להעברה >={level}"""

    middf = pd.read_sql_query(query, conn)

    conn.close()

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        middf.to_excel(writer,sheet_name="מספר שעות רב",index=False)
    #
    
    return [inspect.stack()[0][3],middf.shape[0],"מספר עובדים עם כמות שעות גבוהה מאוד"]
#
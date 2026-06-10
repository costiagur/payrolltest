import custom
import pandas as pd
import inspect
import sqlite3

# עובדים שעבדו ואין החזר תחבורה ציבורית

def no_pubtransport(level=""):

    conn = sqlite3.connect(custom.dbsave)
    cur = conn.cursor()

    query = f"""
        SELECT timesheet.מספר_עובד, timesheet.שם_עובד, COUNT(timesheet.פעילות)
        FROM timesheet
        WHERE timesheet.מחלקה <> '817800' AND timesheet.פעילות IN ('עבודה','החתמה ידנית באישור','השתלמות')
        AND timesheet.מספר_עובד NOT IN (SELECT DISTINCT dfcurr.Empid
            FROM dfcurr
            WHERE dfcurr.Elem IN (1616,300,1365) AND dfcurr.Amount > 0 AND dfcurr.Refdate = (SELECT MAX(Refdate) FROM dfcurr))
        GROUP BY timesheet.מספר_עובד
    """

    resdf = pd.read_sql_query(query, conn)

    conn.close()

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer, sheet_name="אין החזר תחבורה", index=False, header=["מספר עובד", "שם", "מספר נוכחויות"])

    return [inspect.stack()[0][3], len(resdf), "עובדים שעבדו ואין החזר תחבורה ציבורית"]

import custom
import pandas as pd
import inspect
import sqlite3

#תשלום נסיעות ללא סמל שכר יסוד

def pubtrasport_nowork(level=""):

    conn = sqlite3.connect(custom.dbsave)
    cur = conn.cursor()

    REFMONTH = cur.execute("SELECT MAX(Refdate) FROM dfcurr").fetchone()[0]

    query = f"""
        SELECT Empid_mn, Empname, Elem_heb, Amount
        FROM dfcurr 
        WHERE
        Elem IN {custom.pubtransport} AND Amount > 0 AND Refdate = {REFMONTH} AND 
        (Empid_mn NOT IN (SELECT DISTINCT Empid_mn FROM dfcurr WHERE Elem in {custom.yesodandhours})
        OR
        dfcurr.Empid NOT IN (SELECT DISTINCT timesheet.מספר_עובד
            FROM timesheet
            WHERE timesheet.פעילות IN ('עבודה','החתמה ידנית באישור','השתלמות')))
    """

    resdf = pd.read_sql_query(query, conn)

    conn.close()

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer,sheet_name="נסיעות ללא שכר",index=False,header=["מספר עובד ומנ", "שם", "סמל", "סכום"])
    #

    return [inspect.stack()[0][3],len(resdf),"עובדים עם נסיעות ללא שכר"]
#
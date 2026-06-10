import custom
import pandas as pd
import inspect
import sqlite3

#תשלום נסיעות כשלעובד יש ליסינג

def pubtransport_leasing(level=""):

    conn = sqlite3.connect(custom.dbsave)
    cur = conn.cursor()

    REFMONTH = cur.execute("SELECT MAX(Refdate) FROM dfcurr").fetchone()[0]

    query = f"""
        SELECT dfcurr.Empid, dfcurr.Empname, dfcurr.Elemtype_heb, dfcurr.Amount
        FROM dfcurr
        WHERE dfcurr.Elem IN {custom.pubtransport} AND dfcurr.Empid IN (SELECT DISTINCT dfcurr.Empid
        FROM dfcurr
        WHERE dfcurr.Elem = 300) AND dfcurr.Refdate = {REFMONTH}
    """

    resdf = pd.read_sql_query(query, conn)

    conn.close()

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer, sheet_name="נסיעות וליסינג", index=False, header=["מספר עובד", "שם", "סמל", "סכום"])
    #

    return [inspect.stack()[0][3], len(resdf), "עובדים עם נסיעות ליסינג"]
#

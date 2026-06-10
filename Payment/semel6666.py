#6666 ו 6667 שווים
import custom
import pandas as pd
import inspect
import sqlite3

def semel6666(level=""):

    conn = sqlite3.connect(custom.dbsave)

    query = f"""
    SELECT dfcurr.Empid,dfcurr.Empname,dfcurr.mn,SUM(dfcurr.Amount)
    FROM dfcurr
    WHERE dfcurr.Elem IN (6666, 6667)
    GROUP BY dfcurr.Empid,dfcurr.Empname,dfcurr.mn
    HAVING SUM(dfcurr.Amount) <> 0
    """
    resdf = pd.read_sql_query(query, conn)

    conn.close()

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer,sheet_name="6666_6667",index=False)
    #             
    
    return [inspect.stack()[0][3],len(resdf),"מספר מקרים של אי שוויון בין סמל 6666 לסמל 6667"]
# 
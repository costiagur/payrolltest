#6666 ו 6667 שווים
import custom
import pandas as pd
import inspect
import sqlite3

def semel6666(level=""):

    conn = sqlite3.connect("dbsave.db")
    cur = conn.cursor()

    REFMONTH = cur.execute("SELECT MAX(Refdate) FROM dfcurr").fetchone()[0]

    query = f"SELECT Empid,mn,Empname,Amount,Elem FROM dfcurr WHERE Refdate = '{REFMONTH}' AND Elem IN (6666,6667)"

    middf = pd.read_sql_query(query, conn)

    conn.close()

    #middf = custom.DFCURR.loc[(custom.DFCURR["Refdate"] == custom.REFMONTH)&(custom.DFCURR["Elem"].isin(("6666","6667"))),["Empid","Empname","mn","Elem","Amount"]]

    resdf = middf.groupby(by = ["Empid","Empname","mn"],as_index=False,group_keys=True).sum("Amount")

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer,sheet_name="6666_6667",index=False)
    #             
    
    return [inspect.stack()[0][3],len(resdf.loc[resdf["Amount"] > 0,"Empid"].unique()),"מספר מקרים של אי שוויון בין סמל 6666 לסמל 6667"]
# 
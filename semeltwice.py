#סמל שמופיע מספר פעמים באותו תאריך ערך
import custom
import pandas as pd
import sqlite3

def semeltwice(level="1"):
    level = int(level)

    conn = sqlite3.connect("dbsave.db")
    cur = conn.cursor()

    #REFMONTH = cur.execute("SELECT MAX(Refdate) FROM dfcurr").fetchone()[0]

    query = f"SELECT Empid,mn,Empname,Refdate,Amount,Elem_heb FROM dfcurr WHERE Amount <> 0.0)"

    middf = pd.read_sql_query(query, conn)

    conn.close()

    #middf = custom.DFCURR[custom.DFCURR["Amount"] != 0]
    grouped = middf.groupby(by=["Empid","Empname","mn","Refdate","Elem_heb"],as_index=False,group_keys=True)
    groupdf = grouped["Amount"].count()
    resdf = groupdf[groupdf["Amount"] > level]
    resdf.rename(columns={"Amount":"Count"}, inplace=True)

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer,sheet_name="semeltwice",index=False)
    #

    return len(resdf["Empid"].unique())
#
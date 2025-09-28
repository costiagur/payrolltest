#חלקיות משרה מעל 100%
import custom
import pandas as pd
import inspect
import sqlite3

def semel_ratio(level="1.1"):

    level = float(level)

    conn = sqlite3.connect("dbsave.db")
    cur = conn.cursor()

    REFMONTH = cur.execute("SELECT MAX(Refdate) FROM dfcurr").fetchone()[0]

    query = f"SELECT Empid AS 'מספר עובד',mn AS מנ, Empname AS שם, Elem_heb AS 'סמל שכר',Amount AS 'סכום שוטפת' FROM dfcurr WHERE Refdate = '{REFMONTH}' AND Elem = {custom.semelratio} AND Amount > {level}"

    middf = pd.read_sql_query(query, conn)

    conn.close()


    #middf = custom.DFCURR.loc[(custom.DFCURR["Elem"] == custom.semelratio)&(custom.DFCURR["Refdate"] == custom.REFMONTH)&(custom.DFCURR["Amount"]>level),["Empid","Empname","mn","Elem_heb","Amount"]]

    #middf.rename(columns={"Empid":"מספר עובד","Empname":"שם","mn":"מנ","Elem_heb":"סמל שכר","Amount":"סכום שוטף"},inplace=True)


    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        middf.to_excel(writer,sheet_name="חלקיות מעל 1",index=False)
    # 

    return [inspect.stack()[0][3],len(middf),"מספר עובדים עם חלקיות מעל 100%"]

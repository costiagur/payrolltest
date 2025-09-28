#ברוטו ביטוח לאומי מעל התקרה
import custom
import pandas as pd
import inspect
import sqlite3


def highgrossbtl(level="47465"):

    level = float(level)

    conn = sqlite3.connect("dbsave.db")
    cur = conn.cursor()

    REFMONTH = cur.execute("SELECT MAX(Refdate) FROM dfcurr").fetchone()[0]

    query = f"SELECT Empid AS 'מספר עובד', mn AS מנ, Empname AS שם, Elem_heb AS 'סמל שכר' FROM dfcurr WHERE Division <> 90 AND Elem = {custom.grossbtlsemel} AND Refdate = '{REFMONTH}' AND Amount > {level}"

    middf = pd.read_sql_query(query, conn)

    conn.close()

    #middf = custom.DFCURR[(custom.DFCURR["Division"] != custom.pensiondepartment)&(custom.DFCURR["Elem"] == custom.grossbtlsemel)&(custom.DFCURR["Refdate"] == custom.REFMONTH)&(custom.DFCURR["Amount"] > level)][["Empid","Empname","mn","Elem_heb"]]

    #middf.rename(columns={"Empid":"מספר עובד","Empname":"שם","mn":"מנ","Elem_heb":"סמל שכר"},inplace=True)

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        middf.to_excel(writer,sheet_name="ברוטו בל גבוה",index=False)
    #  

    return [inspect.stack()[0][3],len(middf["מספר עובד"].unique()),"מספר עובדים עם ברוטו ביטוח לאומי מעל לתקרה"]
#

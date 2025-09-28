#הזינו סכום במקום כמות בסמל שעות עבודה בשכר לפי שעות
import custom
import pandas as pd
import inspect
import sqlite3

def semel_payhours(level="173"):

    level = float(level)

    conn = sqlite3.connect("dbsave.db")
    cur = conn.cursor()

    REFMONTH = cur.execute("SELECT MAX(Refdate) FROM dfcurr").fetchone()[0]

    query = f"SELECT Empid AS 'מספר עובד',mn AS מנ, Empname AS שם, Elem_heb AS 'סמל שכר',Quantity AS 'כמות שוטפת' FROM dfcurr WHERE Refdate = '{REFMONTH}' AND Elem = {custom.byhourpay} AND Quantity > {level}"

    middf = pd.read_sql_query(query, conn)

    conn.close()


    #middf = custom.DFCURR[(custom.DFCURR["Refdate"] == custom.REFMONTH)&((custom.DFCURR["Elem"] == custom.byhourpay)&(custom.DFCURR["Quantity"] > level))][["Empid","Empname","mn","Elem_heb","Quantity"]]
    
    #middf.rename(columns={"Empid":"מספר עובד","Empname":"שם","mn":"מנ","Elem_heb":"סמל שכר","Quantity":"כמות שוטפת"},inplace=True)

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        middf.to_excel(writer,sheet_name="מספר שעות עבודה גבוה",index=False)
    # 

    return [inspect.stack()[0][3],len(middf),"מספר עובדים שכמות שעות עבודה לפי שעות מעל חודש מלא"]
#
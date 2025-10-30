import custom
import pandas as pd
import numpy as np
import inspect
import sqlite3

#יש דיווח של שעות עבודה לתלוש אך אין תשלום סמל שכר יסוד

def hoursWithoutYesod(level=""):

    conn = sqlite3.connect("dbsave.db")
    cur = conn.cursor()

    REFMONTH = cur.execute("SELECT MAX(Refdate) FROM dfcurr").fetchone()[0]

    query1 = f"SELECT Empid_mn FROM dfcurr WHERE Elem IN {str(tuple(custom.yesodandhours))} AND Refdate = '{REFMONTH}' AND Division <> 90"

    middf = pd.read_sql_query(query1, conn)

    query2 = f"SELECT Empid_mn FROM dfhours WHERE WorkHours > 0"

    hours = pd.read_sql_query(query2, conn)

    dataNotin = np.isin(hours,middf,invert=True) #find which are present in hours and not in dfcurr

    empids = hours.loc[dataNotin,"Empid_mn"].tolist()

    query3 = f"SELECT Empid AS 'מספר עובד', Empname AS שם, mn AS מנ, Refdate AS 'תאריך ערך', WorkHours AS 'שעות עבודה' FROM dfhours WHERE Empid_mn IN {str(tuple(empids))}"

    resdf = pd.read_sql_query(query3, conn)

    conn.close()

    #middf = custom.DFCURR.loc[(custom.DFCURR["Elem"].isin(custom.yesodandhours))&(custom.DFCURR["Refdate"] == custom.REFMONTH)&(custom.DFCURR["Division"] != custom.pensiondepartment),"Empid_mn"]

    #hours = custom.DFHOURS.loc[custom.DFHOURS["WorkHours"] > 0,"Empid_mn"]

    #resdf = custom.DFHOURS.loc[dataNotin].copy()

    #resdf.rename(columns={"Empid":"מספר עובד","Empname":"שם","mn":"מנ","Amount":"סכום שוטף","Refdate":"תאריך ערך","WorkHours":"שעות עבודה"},inplace=True)

    #resdf.drop(columns=["Empid_mn","Elem"],inplace=True)

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer,sheet_name="שעות ללא יסוד",index=False)
    #    
    
    return [inspect.stack()[0][3],resdf.shape[0],"מספר עובדים שיש נוכחות אך אין שכר יסוד"]


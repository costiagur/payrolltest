import custom
import numpy
import pandas as pd
import inspect
import sqlite3

#תשלום נסיעות ללא סמל שכר יסוד

def pubtrasport_nowork(level="0"):

    conn = sqlite3.connect("dbsave.db")
    cur = conn.cursor()

    REFMONTH = cur.execute("SELECT MAX(Refdate) FROM dfcurr").fetchone()[0]

    query1 = f"SELECT DISTINCT Empid_mn FROM dfcurr WHERE Elem IN {str(tuple(custom.pubtransport))} AND Amount > 0 AND Refdate = '{REFMONTH}'"

    arrpubtrans = pd.read_sql_query(query1, conn)

    query2 = f"SELECT DISTINCT Empid_mn FROM dfcurr WHERE Elem IN {str(tuple(custom.yesodandhours))} AND Amount > 0 AND Refdate = '{REFMONTH}'"

    arryesod = pd.read_sql_query(query2, conn)

    diffarr = numpy.setdiff1d(arrpubtrans,arryesod,assume_unique=True)
    
    print(diffarr)

    query3 = f"SELECT Empid AS 'מספר עובד',mn AS מנ, Empname AS שם, Refdate AS 'תאריך ערך',Amount AS 'סכום',Elem_heb AS 'סמל' FROM dfcurr WHERE Empid_mn IN {str(tuple(diffarr))} AND Elem IN {str(tuple(custom.yesodandhours+custom.pubtransport))}"

    resdf = pd.read_sql_query(query3, conn)

    conn.close()

    #arrpubtrans = custom.DFCURR.loc[(custom.DFCURR["Elem"].isin(custom.pubtransport))&(custom.DFCURR["Amount"]>0)&(custom.DFCURR["Refdate"] == custom.REFMONTH),"Empid_mn"].unique()
    #arryesod = custom.DFCURR.loc[(custom.DFCURR['Elem'].isin(custom.yesodandhours))&(custom.DFCURR["Amount"]>0)&(custom.DFCURR["Refdate"] == custom.REFMONTH),"Empid_mn"].unique()
    
    #resdf = custom.DFCURR[(custom.DFCURR["Empid_mn"].isin(diffarr))&(custom.DFCURR["Elem"].isin(custom.yesodandhours+custom.pubtransport))][["Empid","Empname","mn","Refdate","Elem_heb","Amount"]]
    #resdf.rename(columns={"Empid":"מספר עובד","Empname":"שם עובד","mn":"מנ","Elem_heb":"סמל","Amount":"סכום","Refdate":"תאריך ערך"},inplace=True)

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer,sheet_name="נסיעות ללא שכר",index=False)
    #

    return [inspect.stack()[0][3],len(resdf["מספר עובד"].unique()),"עובדים עם נסיעות ללא שכר"]
#
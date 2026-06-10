import custom
import pandas as pd
import sqlite3
from Db import db
import inspect


def newsymbols(level = ""):

    conn = sqlite3.connect(custom.dbsave)
    mydb = db.MYSQLDB()

    query = f"""
    WITH Currlist as (SELECT DISTINCT dfcurr.Empid,dfcurr.Empname,dfcurr.Empid_mn,dfcurr.Dirug,dfcurr.Elem_heb, jobs.jobname 
    from dfcurr 
    LEFT JOIN jobs ON dfcurr.Empid_mn = jobs.empid_mn
    WHERE dfcurr.Elem in {custom.byreport}),
    Prevlist as (SELECT DISTINCT dfprev.Empid, dfprev.Empname,dfprev.Empid_mn,dfprev.Dirug, dfprev.Elem_heb, jobs.jobname 
    from dfprev
    Left JOIN jobs ON dfprev.Empid_mn = jobs.empid_mn 
    where dfprev.Elem in {custom.byreport})
    SELECT Currlist.Empid,Currlist.Empname,Currlist.Dirug, Currlist.Elem_heb,Currlist.jobname, "חדש" as State
    FROM Currlist
    LEFT JOIN Prevlist ON Prevlist.Empid_mn = Currlist.Empid_mn 
    WHERE Currlist.Elem_heb NOT IN (SELECT Elem_heb FROM Prevlist WHERE Prevlist.Empid_mn = Currlist.Empid_mn)
    UNION
    SELECT Prevlist.Empid,Prevlist.Empname,Prevlist.Dirug, Prevlist.Elem_heb,Prevlist.jobname, "נעלם" as State
    FROM Prevlist
    LEFT JOIN Currlist ON Prevlist.Empid_mn = Currlist.Empid_mn 
    WHERE Prevlist.Elem_heb NOT IN (SELECT Elem_heb FROM Currlist WHERE Prevlist.Empid_mn = Currlist.Empid_mn)"""

    resdf = pd.read_sql_query(query, conn) 

    query2 = 'SELECT MAX(Refdate) from dfcurr limit 1'
    
    REFMONTH = conn.execute(query2).fetchone()[0]

    eomonth = pd.to_datetime(REFMONTH) + pd.DateOffset(months = +1)
    listoflists = mydb.searchorders(REFMONTH,eomonth)
    orderdf = pd.DataFrame(listoflists,columns=['empid','ordercapt','ordertext'])

    orderdf["text"] = orderdf.apply(lambda row: "{} - {}".format(row["ordercapt"] if isinstance(row["ordercapt"],str) else row["ordercapt"].decode('UTF-8'),row["ordertext"] if isinstance(row["ordertext"],str) else row["ordertext"].decode('UTF-8')),axis=1)

    orderdf.drop_duplicates(inplace=True)

    resdf["Record"] = resdf.apply(lambda row: orderdf.loc[orderdf["empid"] == row["Empid"],"text"].values[0] if len(orderdf.loc[orderdf["empid"] == row["Empid"]]) > 0 else "", axis=1)

    with pd.ExcelWriter(custom.xlresfile, mode="a",if_sheet_exists='overlay') as writer:
        resdf.to_excel(writer,sheet_name="סמל לראשונה",index=False,startrow=1,header=True)
    #  

    conn.close()

    return [inspect.stack()[0][3],resdf.shape[0],"סמלים שהופיעו לראשונה או נעלמו"]

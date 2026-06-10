import pandas as pd
import numpy as np
import custom
import inspect
import sqlite3

def rationonbase(level=''):

    conn = sqlite3.connect(custom.dbsave)
    cur = conn.cursor()

    REFMONTH = cur.execute("SELECT MAX(Refdate) FROM dfcurr").fetchone()[0]

    query = f"""
    with pensionbase as (SELECT dfcurr.Empid, dfcurr.Empname,dfcurr.Stopname, round(dfcurr.Amount,0) as pensamount, remamount
    FROM dfcurr
    LEFT JOIN (Select dfcurr.Empid, dfcurr.Empname, round(SUM(dfcurr.Amount),0) as remamount FROM dfcurr WHERE dfcurr.Elem in {custom.inbase} AND dfcurr.Refdate = '{REFMONTH}' AND dfcurr.Division <> 90 GROUP BY dfcurr.Empid, dfcurr.Empname) AS remove ON dfcurr.Empid = remove.Empid 
    WHERE dfcurr.Elem = {custom.pensionbasesemel} AND dfcurr.Refdate = '{REFMONTH}' AND dfcurr.Division <> 90),

    cleangross as (Select dfcurr.Empid, dfcurr.Empname, Round(SUM(dfcurr.Amount),0) as grossamount, grossremamount
    FROM dfcurr
    LEFT JOIN (Select dfcurr.Empid, dfcurr.Empname, Round(SUM(dfcurr.Amount),0) as grossremamount FROM dfcurr WHERE Elem in {custom.gilum + custom.lics + custom.instotal + custom.miluim + custom.annualelement} AND dfcurr.Refdate = '{REFMONTH}' AND dfcurr.Division <> 90 GROUP BY dfcurr.Empid, dfcurr.Empname) as grossremove
    ON dfcurr.Empid = grossremove.Empid
    WHERE dfcurr.Elemtype = "addition components" AND dfcurr.Refdate = '{REFMONTH}' AND dfcurr.Division <> 90
    GROUP BY dfcurr.Empid, dfcurr.Empname)

    SELECT pensionbase.Empid, pensionbase.Empname,IFnull(pensionbase.Stopname,"") Stop, pensionbase.pensamount- IFNULL(remamount,0) as Basis, IFNULL(grossamount,0) - IFNULL(grossremamount,0) - (pensionbase.pensamount- IFNULL(remamount,0)) as nonBasis 
    FROM pensionbase 
    LEFT JOIN cleangross ON cleangross.Empid = pensionbase.Empid
    WHERE pensionbase.Empid NOT IN (SELECT dfcurr.Empid FROM dfcurr WHERE dfcurr.Elem IN {custom.gmarheshbon} AND dfcurr.Refdate = '{REFMONTH}')
"""

    middf = pd.read_sql_query(query, conn)

    conn.close()

    resdf = middf.loc[(middf["nonBasis"] > 1.2*middf["Basis"])|(middf["nonBasis"] < -1*middf["Basis"])]  

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer,sheet_name="יחס פנימי בשכר",index=False,header=["מספר עובד","שם","הפסקה","בסיס הפנסיה","תוספות ללא בסיס פנסיה"])
    #

    return [inspect.stack()[0][3],resdf.shape[0],"יחס חלקי שכר חריג"]
#
import pandas as pd
import numpy as np
import custom
import inspect
import sqlite3

def rationonbase(level=''):

    conn = sqlite3.connect("dbsave.db")
    cur = conn.cursor()

    REFMONTH = cur.execute("SELECT MAX(Refdate) FROM dfcurr").fetchone()[0]

    query = f"SELECT Empid,Empname,Refdate,Elemtype,Amount,Elem,Elem_heb FROM dfcurr WHERE Division <> 90 AND Refdate = '{REFMONTH}' AND (Elemtype = 'addition components' OR Elem = '{custom.pensionbasesemel}') AND Amount <> 0"

    middf = pd.read_sql_query(query, conn)

    conn.close()

    #cols = ["Empid","Empname","Refdate","Elemtype","Elem","Elem_heb","Amount"]
    prevyear = pd.to_datetime(REFMONTH) + pd.DateOffset(months = -12)

    #middf = custom.DFCURR.loc[(custom.DFCURR["Division"] != 90)&(custom.DFCURR["Refdate"]==custom.REFMONTH)&((custom.DFCURR["Elemtype"] == "addition components")|(custom.DFCURR["Elem"]==custom.pensionbasesemel))&(custom.DFCURR["Amount"]!=0.0),cols]

    def applystack(row):
        res = []
        res = res + [row["Amount"] if row["Elem"] == custom.pensionbasesemel else 0]
        res = res + [row["Amount"] if row["Elem"] in custom.annualelement else 0]
        res = res + [row["Amount"] if row["Elem"] in custom.annualvehicle else 0]
        res = res + [row["Amount"] if row["Elem"] in (custom.pizuim + custom.HodaaMukdemetHayavBL) else 0]
        res = res + [row["Amount"] if row["Elem"] in custom.miluim else 0]
        return res
    #

    middf[["pensionbase","annual","annualvehicle","pizuim","miluim"]] = middf.apply(applystack,axis=1,result_type='expand')

    middf.loc[(middf["Elem"] == custom.pensionbasesemel)|(middf["Elem"].isin(custom.annualelement))|(middf["Elem"].isin(custom.annualvehicle))|(middf["Elem"].isin(custom.pizuim))|(middf["Elem"].isin(custom.miluim)),"Amount"] = 0

    groupdf = middf.groupby(by=["Empid","Empname"],as_index=False,group_keys=True).sum(["Amount","pensionbase","annual","annualvehicle","pizuim","miluim"])

    groupdf["Amount"] = groupdf["Amount"] - groupdf["pensionbase"]

    resdf = groupdf.loc[(groupdf["Amount"] > 1.2*groupdf["pensionbase"])|(groupdf["Amount"] < -1*groupdf["pensionbase"])]
    resdf.reset_index(drop=True,inplace=True)

    resdf.rename(columns={"Empid":"מספר עובד","Empname":"שם","Amount":"תוספות ללא בסיס פנסיה","pensionbase":"בסיס הפנסיה"},inplace=True)
    resdf.drop(columns=["annual","annualvehicle","pizuim","miluim"],inplace=True)

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer,sheet_name="יחס פנימי בשכר",index=False)
    #

    return [inspect.stack()[0][3],resdf.shape[0],"יחס חלקי שכר חריג"]
#
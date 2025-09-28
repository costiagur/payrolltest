import custom
import pandas as pd
import numpy as np
import inspect
import sqlite3

def semel_without(level="0.05"):

    level = 1-float(level)

    conn = sqlite3.connect("dbsave.db")
    cur = conn.cursor()

    REFMONTH = cur.execute("SELECT MAX(Refdate) FROM dfcurr").fetchone()[0]

    query = f"SELECT Empid,mn,Empname,Refdate,Elemtype,Amount,Elem,Elem_heb,Rank,Startdate FROM dfcurr WHERE Division <> 90 AND Refdate = '{REFMONTH}' AND Elemtype = 'addition components' OR Elem IN {str(tuple(custom.annualvehicle+custom.miluim+custom.meshulav))} AND Amount <> 0.0"

    middf = pd.read_sql_query(query, conn)

    conn.close()

    #middf = custom.DFCURR.loc[(custom.DFCURR["Division"]!= 90)&(custom.DFCURR["Refdate"]==custom.REFMONTH)&(custom.DFCURR["Amount"]!=0)&(custom.DFCURR["Elemtype"]=="addition components")&(~custom.DFCURR["Elem"].isin((custom.annualvehicle+custom.miluim+custom.meshulav))),["Rank","Dirug","Elem","Elem_heb","Amount","Empid","Empname"]]

    groupdf = middf.groupby(by=["Rank","Elem","Elem_heb"],as_index=False,group_keys=True).count()
    groupempdf = middf.groupby(by="Rank",as_index=False,group_keys=True).nunique()

    def numofemps(row):
        return groupempdf.loc[groupempdf["Rank"] == row["Rank"],"Empid"].item()

    groupdf["EmpsNum"] = groupdf.apply(numofemps, axis=1)

    groupdf["required"] = groupdf.apply(lambda row: True if row["Empid"] > row["EmpsNum"]*level and  row["Empid"] < row["EmpsNum"] else False, axis=1)

    resdict = dict()

    def filteremps(row):
        existdf = middf.loc[(middf["Elem"] == row["Elem"])&(middf["Rank"] == row["Rank"]),"Empid"]
        idinRank = middf.loc[middf["Rank"] == row["Rank"],"Empid"].unique()
        absentids = np.setdiff1d(idinRank,existdf)
        for eachid in absentids:
            resdict[eachid] = row.to_dict() | {'Empname': middf.loc[middf["Empid"] == eachid,"Empname"].unique()[0]}    
        #
        return 0
    #

    groupdf["absentids"] = groupdf.loc[groupdf["required"]].apply(filteremps,axis=1)

    resdf = pd.DataFrame.from_dict(resdict,orient='index')

    resdf["EmpsWithout"] = resdf["EmpsNum"] - resdf["Empid"]

    resdf.drop(["Amount","Empid","required"],axis=1,inplace = True)

    resdf.rename(columns={"Empid":"מספר עובד","Empname":"שם","Elem":"מספר סמל","Elem_heb":"סמל שכר","EmpsWithout":"עובדים ללא סמל","EmpsNum":"מספר עובדים"},inplace=True)


    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer,sheet_name="ללא סמל",index=True)
    #   

    return [inspect.stack()[0][3],resdf.shape[0],"עובדים ללא סמל שיש לשאר עובדים בדירוג"]



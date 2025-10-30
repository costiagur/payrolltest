    #בדיקת סבירות של ניכוים לקופות

import pandas as pd
import numpy as np
import custom
import statsmodels.formula.api as smf
import inspect
import sqlite3

def fundsprovision(level=""):   

    pd.set_option('display.float_format', lambda x: '%.2f' % x)

    #cols = ["Empid","Empname","mn","Startdate","Refdate","Elemtype","Elem","Elem_heb","Rank","Amount"]

    conn = sqlite3.connect("dbsave.db")
    cur = conn.cursor()

    custom.REFMONTH = cur.execute("SELECT MAX(Refdate) FROM dfcurr").fetchone()[0]

    query = f"SELECT Empid,mn,Empname,Refdate,Elemtype,Amount,Elem,Elem_heb,Rank,Startdate FROM dfcurr WHERE Division <> 90 AND Refdate = '{custom.REFMONTH}' AND ((Elemtype IN ('addition components','provision components') OR Elem = '{custom.takzivit}') AND (Elem NOT IN ({str(tuple(custom.nonpension))}) ) AND Amount <> 0.0)"

    middf = pd.read_sql_query(query, conn)

    conn.close()

    prevyear = pd.to_datetime(custom.REFMONTH) + pd.DateOffset(months = -12)

    #middf = custom.DFCURR.loc[(custom.DFCURR["Division"] != 90)&(custom.DFCURR["Refdate"]==custom.REFMONTH)&((custom.DFCURR["Elemtype"].isin(("addition components","provision components"))|(custom.DFCURR["Elem"]==custom.takzivit))&(~custom.DFCURR["Elem"].isin(custom.nonpension))&(custom.DFCURR["Amount"]!=0.0)),cols]

    def apply1(row):
        reslist = []
        reslist.append(1 if row["Startdate"] > prevyear and row["Rank"] in custom.edufund_fromsecondyear else 0) #in case of non eligible for edu fund during first year
        reslist.append(1 if row["Elem"]=="30501" else 0)
        reslist.append(row["Amount"] if row["Elemtype"] == "provision components" else 0)
        reslist.append(row["Amount"] if row["Elemtype"] == "addition components" else 0)
        reslist.append(1 if row["Rank"] in custom.hozeishi else 0)
        reslist.append(row["Amount"] if row["Elemtype"] == "addition components" and row["Elem"] in (custom.annualelement+ custom.annualvehicle)  else 0)
   
        return reslist
    #

    middf[["FirstYear","Takzivit","Provision","Addition","HighRank","AnnualElem"]] = middf.apply(apply1,axis=1,result_type='expand')

    groupdf = middf.groupby(by = ["Empid","Empname"],as_index=False,group_keys=True).sum(("Provision","Addition","Takzivit","FirstYear","HighRank","AnnualElem"))

    def apply2(row):

        reslist = []

        reslist.append(1 if row["FirstYear"] > 0 else 0) #FirstYear
        reslist.append(1 if row["Takzivit"] > 0 else 0) #Takzivit
        reslist.append(1 if row["HighRank"] > 0 else 0) #HighRank
        
        return reslist
    #

    groupdf[["FirstYear","Takzivit","HighRank"]] = groupdf.apply(apply2,axis=1,result_type='expand')

    model = smf.ols(formula="Provision ~ Addition + AnnualElem + FirstYear*Addition + Takzivit*Addition + HighRank*Addition",data=groupdf,missing='drop').fit()
    print(model.summary())
    
    groupdf["Yhat"] = model.predict()
    groupdf["Residual"] = model.resid
    
    groupdf["Yhatrate"] = groupdf.apply(lambda row: (row["Yhat"]/row["Addition"]) if row["Addition"] != 0 else row["Yhat"],axis=1)
    groupdf["Provisionrate"] =groupdf.apply(lambda row: (row["Provision"]/row["Addition"]) if row["Addition"] != 0 else row["Provision"],axis=1) 

    hists,bins = np.histogram(groupdf["Residual"],100)

    leng = abs(bins[1] - bins[0])

    groupdf["Hist"] = groupdf.apply(lambda row: hists[min(np.floor((row["Residual"] - bins[0])/leng).astype(int),99)],axis=1)

    resdf = groupdf.loc[groupdf["Hist"] <= 10,["Empid","Empname","Addition","Provision","Provisionrate","Yhat","Yhatrate"]]

    resdf.rename(columns={"Empid":"מספר עובד","Empname":"שם","Addition":"תוספות","Provision":"הפרשה","Provisionrate":"שעור הפרשה","Yhat":"אומדן רוחבי","Yhatrate":"שעור אומדן"},inplace=True)

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer,sheet_name="שיעור הפרשה לקופות",index=False)
    #  

    return [inspect.stack()[0][3],len(resdf["מספר עובד"].unique()),"מספר עובדים עם קופות חריגות"]
#

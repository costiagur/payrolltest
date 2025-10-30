import custom
import pandas as pd
import numpy as np
import inspect
import sqlite3


#בסיס פנסיה מחושב אינו סביר ביחס לבסיס פנסיה בתלוש. לדוגמה כאשר חלקיות אינה סבירה ביחס לבסיס הפנסיה

def BasisvsCalculated(level="0.1"):

    conn = sqlite3.connect("dbsave.db")
    cur = conn.cursor()

    level = float(level)

    pd.set_option('display.float_format', lambda x: '%.2f' % x)

    semelsneeded = ((custom.semelratio,custom.pensionbasesemel,custom.hourdeduct,custom.takzivit)+custom.nottakzivitbase+custom.yesodandhours+custom.inbase)

    res = cur.execute("SELECT MAX(Refdate) FROM dfcurr")

    REFMONTH = res.fetchone()[0]

    query = f"SELECT Empid,mn,Empid_mn,Dirug,Empname,Elemtype,Elem_heb,Amount,Elem,Division FROM dfcurr WHERE Refdate = '{REFMONTH}' AND (Elem IN {str(tuple(semelsneeded))} OR Elem_heb = {chr(34) + custom.dayvalue + chr(34)}) AND Division <> {custom.pensiondepartment} AND mn <> 99 AND Rank NOT IN {str(tuple(custom.hourwageranks))}"

    middf = pd.read_sql_query(query, conn)

    conn.close()

    #middf = custom.DFCURR.loc[(custom.DFCURR["Refdate"] == custom.REFMONTH)&((custom.DFCURR["Elem"].isin(semelsneeded))|(custom.DFCURR["Elem_heb"] == custom.dayvalue))&(custom.DFCURR["Division"] != custom.pensiondepartment)&(custom.DFCURR["mn"] != "99")&(~custom.DFCURR["Rank"].isin(custom.hourwageranks)), \
    #                 ["Empname","Empid","mn","Dirug","Division","Empid_mn","Elemtype","Elem_heb","Elem","Amount"]]
    
    middf["Intakzivit"] = middf.apply(lambda row: 1 if row["Elem"] == custom.takzivit else 0,axis=1)
    
    middf["Deductions"] = middf.apply(lambda row: row["Amount"] if row["Elem"] in ((custom.hourdeduct,custom.byhourpay)+custom.inbase) else 0,axis=1)
    
    middf["Nottakzivitbase"] = middf.apply(lambda row: row["Amount"] if row["Elem"] in (custom.nottakzivitbase) else 0,axis=1)
        
    middf["actBasis"] = middf.apply(lambda row: row["Amount"] if row["Elem"] == custom.pensionbasesemel else 0,axis=1)
    
    middf["Wagerate"] = middf.apply(lambda row: row["Amount"] if row["Elem"] == custom.semelratio else 0,axis=1)
        
    def calcBasis(row):
        res = 0
        
        #if row["Elem_heb"] == custom.dayvalue:            
        res = row["Amount"] * 22 * middf.loc[(middf["Elem"] == custom.semelratio)&(middf["Empid_mn"] == row["Empid_mn"]),"Amount"].sum()
        #else:
        #    res = 0
        #
        return res
    #
    
    middf["calcBasis"] = middf.loc[middf["Elem_heb"] == custom.dayvalue].apply(calcBasis,axis=1)
    
    groupdf = middf.groupby(by=["Empname","Empid","mn","Dirug","Division"],as_index=False,group_keys=True).sum(["Wagerate","actBasis","Intakzivit","Deductions","Nottakzivitbase","calcBasis"])
    
    groupdf["Ratio"] = groupdf.apply(lambda row: (row["actBasis"] - row["Deductions"] + row["Nottakzivitbase"]*row["Intakzivit"])/(row["calcBasis"] if row["calcBasis"] != 0 else 1),axis=1)
    
    findf = groupdf.loc[(groupdf["Ratio"] <1-level) |(groupdf["Ratio"] > 1+level)&(np.round(groupdf["Ratio"],3) != round(25/22,3))].copy()

    #findf.rename(columns={"Empname":"שם","Empid":"מספר עובד","mn":"מנ","Dirug":"דירוג","Division":"אגף","Amount":"סכום","actBasis":"בסיס פנסיה בפועל","Wagerate":"חלקיות משרה","calcBasis":"בסיס מחושב"},inplace=True)

    with pd.ExcelWriter(custom.xlresfile, mode="a",if_sheet_exists='replace') as writer:
        findf[["Empid","Empname","mn","Dirug","Division","actBasis","Wagerate","calcBasis"]].to_excel(writer,sheet_name="בסיס פנסיה",float_format="%.2f",header=["מספר עובד","שם","מנ","דירוג","אגף","בסיס פנסיה בפועל","חלקיות משרה","בסיס מחושב"],index=False)
    #      
    

    return [inspect.stack()[0][3],len(findf),"מספר עובדים עם בסיס פנסיה לא סביר ביחס לערך שעה וחלקיות"]
#
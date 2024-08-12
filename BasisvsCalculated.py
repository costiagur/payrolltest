import custom
import pandas as pd
import numpy as np

#בסיס פנסיה מחושב אינו סביר ביחס לבסיס פנסיה בתלוש. לדוגמה כאשר חלקיות אינה סבירה ביחס לבסיס הפנסיה

def BasisvsCalculated(level="0.1"):

    level = float(level)

    pd.set_option('display.float_format', lambda x: '%.2f' % x)

    semelsneeded = ((custom.semelratio,custom.pensionbasesemel,custom.hourdeduct,custom.takzivit)+custom.nottakzivitbase+custom.yesodandhours+custom.inbase)

    middf = custom.DF101.loc[(custom.DF101["Refdate"] == custom.REFMONTH)&((custom.DF101["Elem"].isin(semelsneeded))|(custom.DF101["Elem_heb"] == custom.dayvalue))&(custom.DF101["Division"] != custom.pensiondepartment)&(custom.DF101["mn"] != "99")&(~custom.DF101["Rank"].isin(custom.hourwageranks)), \
                     ["Empname","Empid","mn","Dirug","Division","Empid_mn","Elemtype","Elem_heb","Elem","CurAmount"]]
    
    middf["Intakzivit"] = middf.apply(lambda row: 1 if row["Elem"] == custom.takzivit else 0,axis=1)
    
    middf["Deductions"] = middf.apply(lambda row: row["CurAmount"] if row["Elem"] in ((custom.hourdeduct,custom.byhourpay)+custom.inbase) else 0,axis=1)
    
    middf["Nottakzivitbase"] = middf.apply(lambda row: row["CurAmount"] if row["Elem"] in (custom.nottakzivitbase) else 0,axis=1)
        
    middf["actBasis"] = middf.apply(lambda row: row["CurAmount"] if row["Elem"] == custom.pensionbasesemel else 0,axis=1)
    
    middf["Wagerate"] = middf.apply(lambda row: row["CurAmount"] if row["Elem"] == custom.semelratio else 0,axis=1)
        
    def calcBasis(row):
        res = 0
        
        #if row["Elem_heb"] == custom.dayvalue:            
        res = row["CurAmount"] * 22 * middf.loc[(middf["Elem"] == custom.semelratio)&(middf["Empid_mn"] == row["Empid_mn"]),"CurAmount"].sum()
        #else:
        #    res = 0
        #
        return res
    #
    
    middf["calcBasis"] = middf.loc[middf["Elem_heb"] == custom.dayvalue].apply(calcBasis,axis=1)
    
    groupdf = middf.groupby(by=["Empname","Empid","mn","Dirug","Division"],as_index=False,group_keys=True).sum(["Wagerate","actBasis","Intakzivit","Deductions","Nottakzivitbase","calcBasis"])
    
    groupdf["Ratio"] = groupdf.apply(lambda row: (row["actBasis"] - row["Deductions"] + row["Nottakzivitbase"]*row["Intakzivit"])/(row["calcBasis"] if row["calcBasis"] != 0 else 1),axis=1)
    
    findf = groupdf.loc[(groupdf["Ratio"] <1-level) |(groupdf["Ratio"] > 1+level)&(np.round(groupdf["Ratio"],3) != round(25/22,3))].copy()

    findf.rename(columns={"Empname":"שם","Empid":"מספר עובד","mn":"מנ","Dirug":"דירוג","Division":"אגף","CurAmount":"סכום","actBasis":"בסיס פנסיה בפועל","Wagerate":"חלקיות משרה","calcBasis":"בסיס מחושב"},inplace=True)

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        findf[["מספר עובד","שם","מנ","דירוג","אגף","בסיס פנסיה בפועל","חלקיות משרה","בסיס מחושב"]].to_excel(writer,sheet_name="בסיס פנסיה",index=False)
    #      
    

    return len(findf)
#
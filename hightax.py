#מס הכנסה גבוה
import numpy as np
import pandas as pd
import custom
import statsmodels.formula.api as smf
import inspect
import sqlite3

def hightax(level = ""):
    
    pd.set_option('display.float_format', lambda x: '%.2f' % x)

    conn = sqlite3.connect("dbsave.db")
    cur = conn.cursor()

    #REFMONTH = cur.execute("SELECT MAX(Refdate) FROM dfcurr").fetchone()[0]
    #PREVMONTH = cur.execute("SELECT MAX(Refdate) FROM dfprev").fetchone()[0]

    query = "SELECT Empid, Empname, Division, Elemtype, Elem_heb, Elem, Rank, vetek, Amount as {} FROM {} WHERE Elemtype IN ('addition components', 'benefit charge components', 'compulsory deductions')"

    dfcurr = pd.read_sql_query(query.format("CurAmount","dfcurr"), conn)
    dfprev = pd.read_sql_query(query.format("PrevAmount","dfprev"), conn)

    conn.close()

    #custom.REFMONTH = curdf["Refdate"].max()
    #custom.PREVMONTH = prevdf["Refdate"].max()

    #dfcurr = custom.DFCURR.loc[custom.DFCURR["Elemtype"].isin(["addition components","benefit charge components","compulsory deductions"]),["Empname","Empid","Division","Elemtype","Elem_heb","Elem","Amount","Rank","vetek"]]
    #dfprev = custom.DFPREV.loc[custom.DFPREV["Elemtype"].isin(["addition components","benefit charge components","compulsory deductions"]),["Empname","Empid","Division","Elemtype","Elem_heb","Elem","Amount","Rank","vetek"]]

    #dfcurr.rename(columns={"Amount":"CurAmount"},inplace=True)
    #dfprev.rename(columns={"Amount":"PrevAmount"},inplace=True)

    middf = pd.merge(dfcurr,dfprev,how="left",on=["Empname","Empid","Division","Elemtype","Elem_heb","Elem","Rank","vetek"])

    def apply1(row):
            reslist = []

            reslist.append(row["PrevAmount"] if row["Elem"] in custom.elembtl else 0) #btlPrev
            reslist.append(row["CurAmount"] if row["Elem"] in custom.elembtl else 0) #btlCur
            reslist.append(row["PrevAmount"] if row["Elem"] == custom.elemtax else 0) #taxPrev
            reslist.append(row["CurAmount"] if row["Elem"] == custom.elemtax else 0) #taxCur
            #reslist.append(1 if row["Rank"] == custom.sayaot else 0) #mostfemale
            reslist.append(1 if row["Division"]==custom.pensiondepartment else 0) #pension
            #reslist.append(row["CurAmount"] if row["Elem"] in custom.pizuim else 0) #CurPizuim
            #reslist.append(row["CurAmount"] if row["Elem"] in custom.annualelement else 0) #Annual
            reslist.append(row["CurAmount"] if row["Elemtype"] in ("addition components","benefit charge components") else 0) #Current Gross Amounts
            reslist.append(row["PrevAmount"] if row["Elemtype"] in ("addition components","benefit charge components") else 0) #Previous Gross Amounts

            return reslist
    #

    middf[["btlPrev","btlCur","taxPrev","taxCur","pension","CurAm","PrevAm"]] =  middf.apply(apply1,axis=1,result_type='expand') #"mostfemale","CurPizuim","Annual",

    groupdf = middf.groupby(by = ["Empname","Empid"],as_index=False,group_keys=True).agg({"CurAm":'sum',"PrevAm":'sum',"btlCur":'sum',"btlPrev":'sum',"taxCur":'sum',"taxPrev":'sum',"pension":'max',"vetek":'max'}) #"CurPizuim":'sum',"Annual":'sum',"mostfemale":'max',
        
    def apply2(row):
            reslist = []

            reslist.append(row["btlCur"] / row["CurAm"] if row["CurAm"] != 0 else np.nan) #btlrateCur
            reslist.append(row["taxCur"] / row["CurAm"] if row["CurAm"] != 0 else np.nan) #taxrateCur
            reslist.append(np.power(row["CurAm"],2)/100000) #CurAm2
            reslist.append((row["taxCur"]+row["btlCur"]) if row["taxCur"]+row["btlCur"] > 0 else 0) #DeductCur
            #reslist.append(np.power(row["CurPizuim"],2)/100000) #CurPizuim2

            return reslist
        #

    groupdf[["btlrateCur","taxrateCur","CurAm2","DeductCur"]] = groupdf.apply(apply2,axis=1,result_type='expand') #,"CurPizuim2"

    #model = smf.ols(formula="DeductCur ~ CurAm2 + CurAm + pension*CurAm + mostfemale*CurAm + CurPizuim2 + Annual + vetek*CurAm + vetek*Annual",data=groupdf,missing='drop').fit() #CurPizuim

    #print(model.summary())

    #groupdf["Yhat"] = model.predict()

    #groupdf["Residual"] = model.resid

    #hists,bins = np.histogram(groupdf["Residual"],100)

    #leng = abs(bins[1] - bins[0])

    #groupdf["Hist"] = groupdf.apply(lambda row: hists[min(np.floor((row["Residual"]-bins[0])/leng).astype(int),99)],axis=1)


    def tests(row):
            res = []

            #if row["Hist"] <= 10:
            #    res.append("סכומי מס וביטוח לאומי חורגים מממוצע")               
            ##
            
            if 0 < row["btlrateCur"] < 0.031 and row["pension"] == 0:
                res.append("שיעור ביטוח לאומי נמוך ממזערי")
            #
            
            if row["taxrateCur"] > 0.4:
                res.append("שיעור מס גבוה")
            #
            
            if row["taxCur"] < -10 and row["taxPrev"] < -10:
                res.append("מס שלילי חודשיים ברציפות")
            #
            
            return ". ".join(res)
        #
        
    groupdf["ErrorDescr"] = groupdf.apply(tests,axis=1)
    
    groupdf.rename(columns={"Empid":"מספר עובד","Empname":"שם","CurAm":"סכום שוטף","PrevAm":"סכום חודש קודם","btlCur":"בל שוטף","btlPrev":"בל קודם","taxCur":"מס שוטף","taxPrev":"מס קודם","btlrateCur":"שיעור בל שוטף","taxratePrev":"שיעור מס קודם","taxrateCur":"שיעור מס שוטף","DeductCur":"מס ובל","ErrorDescr":"שגיאה"},inplace=True) #"Yhat":"אומדן",
    
    cols = ["מספר עובד","שם","סכום שוטף","סכום חודש קודם","בל שוטף","מס שוטף","שיעור בל שוטף","שיעור מס שוטף","מס ובל","שגיאה"] #"אומדן",
    
    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        groupdf.loc[groupdf["שגיאה"] != "",cols].to_excel(writer,sheet_name="מס חריג",index=False)
    #  
    
    return [inspect.stack()[0][3],len(groupdf.loc[groupdf["שגיאה"] != "","מספר עובד"].unique()),"מספר עובדים עם שיעור מס וביטוח לאומי חריגים"]
#
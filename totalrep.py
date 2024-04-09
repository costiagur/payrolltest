#מצג כולל
import custom
import db
import numpy as np
import pandas as pd
import grosscur
import grossretro

def totalrep(level="0.2,2000"):

    mydb = db.MYSQLDB()

    middf = custom.DF101.loc[custom.DF101["Elemtype"].isin(("addition components","compulsory deductions","voluntary deductions")),["Empid","Empname","Refdate","Elemtype","PrevAmount","CurAmount","Elem"]]   
       
    middf["GrossCur"] = middf.apply(lambda row: row["CurAmount"] if row["Elemtype"] == "addition components" else 0,axis=1)
    middf["GrossPrev"] = middf.apply(lambda row: row["PrevAmount"] if row["Elemtype"] == "addition components" else 0,axis=1)
    middf["GrossCurCur"] = middf.apply(lambda row: row["GrossCur"] if row["Refdate"] == custom.REFMONTH else 0,axis=1)
    middf["GrossCurRetro"] = middf.apply(lambda row: row["GrossCur"] if row["Refdate"] < custom.REFMONTH else 0, axis=1)
    middf["GrossPrevCur"] = middf.apply(lambda row: row["GrossPrev"] if row["Refdate"] == custom.PREVMONTH else 0, axis=1)
    middf["TaxesCur"] = middf.apply(lambda row: row["CurAmount"] if row["Elemtype"] == "compulsory deductions" else 0,axis=1)
    middf["DeductsCur"] = middf.apply(lambda row: row["CurAmount"] if row["Elemtype"] == "voluntary deductions" else 0,axis=1)
    middf["NetCur"] = middf.apply(lambda row: np.round(row["CurAmount"],0) if row["Elemtype"] == "addition components" else np.round(-row["CurAmount"],0), axis=1)
    middf["Annual"] = middf.apply(lambda row: row["GrossCur"]-row["GrossPrev"] if row["Elem"] in custom.annualelement else 0, axis=1)
    middf["Vehicle"] = middf.apply(lambda row: row["GrossCur"]-row["GrossPrev"] if row["Elem"] in custom.annualvehicle else 0, axis=1)
    
    groupdf = middf.groupby(by = ["Empname","Empid"],as_index=False,group_keys=True).sum(["GrossCur","GrossPrev","GrossCurCur","GrossCurRetro","GrossPrevCur","TaxesCur","DeductsCur","NetCur","Annual","Vehicle"])
    groupdf.drop(columns=["CurAmount","PrevAmount"],inplace=True)
    
    groupdf["Unexplained"] = groupdf.apply(lambda row: np.round(row["GrossCur"] -row["GrossPrev"]- row["Annual"] - row["Vehicle"],0), axis=1)

    groupdf.sort_values(by=['NetCur'], ascending=False, inplace=True)
    
    eomonth = pd.to_datetime(custom.REFMONTH) + pd.DateOffset(months = +1)
    listoflists = mydb.searchorders(custom.REFMONTH,eomonth)
    orderdf = pd.DataFrame(listoflists,columns=['empid','ordercapt','ordertext'])

    orderdf["text"] = orderdf.apply(lambda row: "{} - {}".format(row["ordercapt"] if isinstance(row["ordercapt"],str) else row["ordercapt"].decode('UTF-8'),row["ordertext"] if isinstance(row["ordertext"],str) else row["ordertext"].decode('UTF-8')),axis=1)

    orderdf.drop_duplicates(inplace=True)
    
    groupdf["Order"] = groupdf.apply(lambda row: "; ".join(orderdf.loc[orderdf["empid"] == row["Empid"],"text"].tolist()),axis=1) 

    cols = ["Empid","Empname","NetCur","GrossCur","GrossPrev","GrossCurCur","GrossCurRetro","GrossPrevCur","TaxesCur","DeductsCur","Annual","Vehicle","Unexplained","Order"]

    groupdf = groupdf[cols]

    groupdf.set_index("Empid",inplace=True)

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        groupdf.to_excel(writer,sheet_name="Total",index=True)
    #

    jsdict = groupdf[["Empname","NetCur","GrossCur","GrossCurRetro","TaxesCur","DeductsCur","GrossPrevCur","Annual","Vehicle","Unexplained","Order"]].to_dict('index')

    currdiff = grosscur.grosscur(level)
    retrodiff = grossretro.grossretro(level)

    for eachempid in jsdict:
        jsdict[eachempid]["CurrDiff"]  = currdiff[eachempid] if eachempid in currdiff else ""
        jsdict[eachempid]["RetroDiff"]  = retrodiff[eachempid] if eachempid in retrodiff else ""
    #

    return jsdict

#
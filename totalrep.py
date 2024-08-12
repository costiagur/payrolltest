#מצג כולל
import custom
import db
import numpy as np
import pandas as pd
import grosscur
import grossretro

def totalrep(level="0.2,2000"):

    mydb = db.MYSQLDB()

    levellist = level.split(",")

    cutoffrate = min([float(eachlevel) for eachlevel in levellist])
    cutoffamount = max([float(eachlevel) for eachlevel in levellist])

    middf = custom.DF101.loc[custom.DF101["Elemtype"].isin(("addition components","compulsory deductions","voluntary deductions")),["Empid","Empname","Refdate","Elemtype","PrevAmount","CurAmount","Elem"]]   

    def calccols(row):
       reslist = []
       reslist.append(row["CurAmount"] if row["Elemtype"] == "addition components" else 0) #middf["GrossCur"]
       reslist.append(row["PrevAmount"] if row["Elemtype"] == "addition components" else 0) #middf["GrossPrev"]
       reslist.append(reslist[0] if row["Refdate"] == custom.REFMONTH else 0) #middf["GrossCurCur"]
       reslist.append(reslist[0] if row["Refdate"] < custom.REFMONTH else 0) #middf["GrossCurRetro"]
       reslist.append(reslist[1] if row["Refdate"] == custom.PREVMONTH else 0) #middf["GrossPrevCur"]
       reslist.append(row["CurAmount"] if row["Elemtype"] == "compulsory deductions" else 0) #middf["TaxesCur"]
       reslist.append(row["CurAmount"] if row["Elemtype"] == "voluntary deductions" else 0) #middf["DeductsCur"]
       reslist.append(np.round(row["CurAmount"],0) if row["Elemtype"] == "addition components" else np.round(-row["CurAmount"],0)) #middf["NetCur"]
       reslist.append(reslist[0]-reslist[1] if row["Elem"] in custom.annualelement else 0) #middf["Annual"]
       reslist.append(reslist[0]-reslist[1] if row["Elem"] in custom.annualvehicle else 0) #middf["Vehicle"]

       return reslist
    #

    middf[["GrossCur","GrossPrev","GrossCurCur","GrossCurRetro","GrossPrevCur","TaxesCur","DeductsCur","NetCur","Annual","Vehicle"]] = middf.apply(calccols,axis=1,result_type='expand')
    
    groupdf = middf.groupby(by = ["Empname","Empid"],as_index=False,group_keys=True).sum(["GrossCur","GrossPrev","GrossCurCur","GrossCurRetro","GrossPrevCur","TaxesCur","DeductsCur","NetCur","Annual","Vehicle"])
    groupdf.drop(columns=["CurAmount","PrevAmount"],inplace=True)
    
    groupdf["Unexplained"] = groupdf.apply(lambda row: np.round(row["GrossCur"] -row["GrossPrev"]- row["Annual"] - row["Vehicle"],0), axis=1)    
    
    curdf= pd.concat([grosscur.grosscur(eachid) for eachid in groupdf.loc[abs(groupdf["Unexplained"]) >= cutoffamount,"Empid"].unique()]) 

    prevdf = pd.concat([grossretro.grossretro(eachid,cutoffrate,cutoffamount) for eachid in groupdf.loc[abs(groupdf["GrossCurRetro"])>= cutoffamount,"Empid"].unique()])

    totaldf = pd.concat([groupdf,curdf,prevdf],ignore_index=True)

    totaldf["NetSorting"] = totaldf.apply(lambda row: groupdf.loc[groupdf["Empid"] == row["Empid"],"NetCur"].sum(),axis=1)

    eomonth = pd.to_datetime(custom.REFMONTH) + pd.DateOffset(months = +1)
    listoflists = mydb.searchorders(custom.REFMONTH,eomonth)
    orderdf = pd.DataFrame(listoflists,columns=['empid','ordercapt','ordertext'])

    orderdf["text"] = orderdf.apply(lambda row: "{} - {}".format(row["ordercapt"] if isinstance(row["ordercapt"],str) else row["ordercapt"].decode('UTF-8'),row["ordertext"] if isinstance(row["ordertext"],str) else row["ordertext"].decode('UTF-8')),axis=1)

    orderdf.drop_duplicates(inplace=True)
    
    totaldf["Order"] = totaldf.apply(lambda row: "; ".join(orderdf.loc[orderdf["empid"] == row["Empid"],"text"].tolist()),axis=1) 

    cols = ["Empid","Empname","NetCur","GrossCur","GrossPrev","GrossCurCur","GrossCurRetro","GrossPrevCur","TaxesCur","DeductsCur","Annual","Vehicle","Unexplained","Elem_heb","Currentdiff","Retrodiff","Order","NetSorting"]

    totaldf = totaldf[cols]

    jsdf = totaldf.loc[abs(totaldf["NetCur"])>0,["Empid","Empname","NetCur","GrossCur","GrossPrev","TaxesCur","DeductsCur","Annual","Vehicle","Unexplained","Order"]]

    jsdf.set_index("Empid",inplace=True)

    jsdict = jsdf.to_dict('index')

    totaldf.rename(columns={"Empid":"מספר עובד","Empname":"שם","NetCur":"נטו","GrossCur":"ברוטו שוטף","GrossPrev":"ברוטו חודש קודם","GrossCurCur":"ברוטו שוטף החודש","GrossCurRetro":"ברוטו רטרו החודש","GrossPrevCur":"ברוטו שוטף חודש שעבר","TaxesCur":"מסים החודש","DeductsCur":"ניכויים החודש","Annual":"תשלומים שנתיים","Vehicle":"תשלומי רכב שנתיים","Unexplained":"יתרה לא מוסברת","Elem_heb":"סמל שכר","Currentdiff":"הפרשים שוטפים","Retrodiff":"הפרשי רטרו","Order":"הוראה"},inplace=True)

    totaldf.set_index("מספר עובד",inplace=True)

    totaldf.sort_values(by=['NetSorting','מספר עובד',"שם"], ascending=False, inplace=True)

    totaldf.drop(columns='NetSorting',inplace=True)

    with pd.ExcelWriter(custom.xlresfile, mode="a",if_sheet_exists='replace') as writer:
        totaldf.to_excel(writer,sheet_name="מרכז",index=True)
    #

    currdiff = {}
    retrodiff = {}

    for eachid in curdf["Empid"].unique():
        currdiff[eachid] = curdf.loc[curdf["Empid"].eq(eachid),["Elem_heb","Currentdiff"]].to_dict('list')
    
    for eachid in prevdf["Empid"].unique():
        retrodiff[eachid] = prevdf.loc[prevdf["Empid"].eq(eachid),["Elem_heb","Retrodiff"]].to_dict('list')
#    
    
    for eachempid in jsdict:
        jsdict[eachempid]["CurrDiff"]  = currdiff[eachempid] if eachempid in currdiff else ""
        jsdict[eachempid]["RetroDiff"]  = retrodiff[eachempid] if eachempid in retrodiff else ""
    #

    return jsdict

#
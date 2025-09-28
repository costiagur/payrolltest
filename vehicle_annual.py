#בדיקה שך סכום הביטוח אינו עולה על הסכום המרבי
import custom
import pandas as pd
import inspect
import sqlite3


def vehicle_annual(level="1779,1750,7000"):

    conn = sqlite3.connect("dbsave.db")

    #curdf= custom.DFCURR.loc[custom.DFCURR["Elem"].isin(custom.instotal+custom.lics),["Empid","Empname","Elem","Elem_heb","Amount","Refdate"]]
    #prevdf = custom.DFPREV.loc[custom.DFPREV["Elem"].isin(custom.instotal+custom.lics),["Empid","Empname","Elem","Elem_heb","Amount","Refdate"]]

    #curdf.rename(columns={"Amount":"CurAmount"},inplace=True)
    #prevdf.rename(columns={"Amount":"PrevAmount"},inplace=True)

    query = "SELECT Empid,Empname,Refdate,Amount as {},Elem,Elem_heb FROM {} WHERE Elem IN {}"

    semellist = tuple(list(custom.instotal) + list(custom.lics))

    curdf = pd.read_sql_query(query.format("CurAmount","dfcurr",semellist), conn)
    prevdf = pd.read_sql_query(query.format("PrevAmount","dfprev",semellist), conn)

    conn.close()

    custom.REFMONTH = curdf["Refdate"].max()
    custom.PREVMONTH = prevdf["Refdate"].max()

    middf = pd.merge(curdf,prevdf,how="outer",on=["Empid","Empname","Elem","Elem_heb","Refdate"])    
    middf["PrevAmount"] = middf["PrevAmount"].fillna(0) #filling NaN with 0 so that calculations will be correct
    middf["CurAmount"] = middf["CurAmount"].fillna(0)
    
    middf.sort_values(by=["Empid","Elem","Refdate"],ascending=[True,True,False],axis=0,ignore_index=True,inplace=True)


    def calcrow(row):
        reslist = {}
        if row["Elem"] in custom.lics:
            reslist["lics"] = row["PrevAmount"]+row["CurAmount"]
        else:
            reslist["lics"] = 0
        #
        if row["Elem"] in custom.inshova:
            reslist["inshova"] = row["PrevAmount"]+row["CurAmount"]
        else:
            reslist["inshova"] = 0
        #
        if row["Elem"] in custom.instotal:
            reslist["instotal"] = row["PrevAmount"]+row["CurAmount"]
        else:
            reslist["instotal"] = 0
        #
        if abs(row["PrevAmount"]) > 0 and abs(row["CurAmount"])>0:
            reslist["both"] = 1
        else:
            reslist["both"] = 0
        #
        return reslist.values()
    #

    middf[["Lic","Inshova","Instotal","Both"]] = middf.apply(calcrow,axis=1,result_type='expand')

    levellist = level.split(",")

    licamount = float(levellist[0])
    hovaamount = float(levellist[1])
    insamount = float(levellist[2])

    groupdf = middf.groupby(by = ["Empid","Empname"],as_index=False,group_keys=True).sum(("Lic","Inshova","Instotal","Both"))
    filteredempid = groupdf.loc[(groupdf["Lic"]>licamount)|(groupdf["Inshova"]>hovaamount)|(groupdf["Instotal"]>insamount)|(groupdf["Both"]>0),"Empid"].unique()

    middf.rename(columns={"Empname":"שם","Empid":"מספר עובד","Elem":"סמל","Elem_heb":"שם סמל","PrevAmount":"סכום חודש קודם","CurAmount":"סכום שוטף"},inplace=True)

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        middf.loc[middf["מספר עובד"].isin(filteredempid),["מספר עובד","שם","שם סמל","סכום חודש קודם","סכום שוטף"]].to_excel(writer,sheet_name="רישיון וביטוח רכב",index=False)
    #  

    return [inspect.stack()[0][3],len(filteredempid),"מקרים של ביטוח רכב בסכום חורג"]
#
    
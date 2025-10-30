import custom
import pandas as pd
import sqlite3

def onecompare(searchedid):

    conn = sqlite3.connect('dbsave.db')

    searchedid = int(searchedid)

    query = 'SELECT Empid, mn, Division, Elemtype, CASE WHEN Elemtype = "addition components" THEN 1 WHEN Elemtype = "benefit charge components" THEN 2 WHEN Elemtype = "compulsory deductions" THEN 3 WHEN Elemtype = "voluntary deductions" THEN 4' \
    ' ELSE 5 END AS SORTCOL, Elem_heb, Refdate, CASE WHEN Elemtype IN ("compulsory deductions","voluntary deductions") THEN Amount * -1 ELSE Amount END AS {} FROM {} WHERE Empid = {} AND ' \
    '(Elemtype IN ("addition components","compulsory deductions","voluntary deductions","benefit charge components") OR Elem IN ({},{}))'

    currdf = pd.read_sql_query(query.format("CurAmount","dfcurr",searchedid,custom.semelratio,custom.semelnett), conn) 
    prevdf = pd.read_sql_query(query.format("PrevAmount","dfprev",searchedid,custom.semelratio,custom.semelnett), conn) 

    REFMONTH = currdf["Refdate"].max()
    PREVMONTH = prevdf["Refdate"].max()

    middf = pd.concat([currdf,prevdf],ignore_index=True)

    middf["PrevAmount"] = middf["PrevAmount"].fillna(0) #filling NaN with 0 so that calculations will be correct
    middf["CurAmount"] = middf["CurAmount"].fillna(0)

    def setperiod(row):
        if row["CurAmount"] != 0:
            if row["Refdate"] == REFMONTH:
                return "שוטף"
            else:
                return "רטרו"
            #
        elif row["PrevAmount"] != 0:
            if row["Refdate"] == PREVMONTH:
                return "שוטף"
            else:
                return "רטרו"
            #
        #
    #

    middf["Period"] = middf.apply(setperiod,axis=1)

    middf.sort_values(by=["mn","SORTCOL","Elem_heb","Period"],ascending=[True,True,True,False],axis=0,ignore_index=True,inplace=True)

    groupdf = middf.groupby(by = ["Division","mn","SORTCOL","Elemtype","Elem_heb","Period"],as_index=False,group_keys=True).sum(("CurAmount","PrevAmount"))

    groupdf["Elemtype_heb"] = groupdf["Elemtype"].map({"addition components":"תוספות","compulsory deductions":"ניכויי חובה","voluntary deductions":"ניכויים אחרים","benefit charge components":"שווי","additional data":"מידע"})

    groupdf["Diff"] = round(groupdf["CurAmount"] - groupdf["PrevAmount"],2)

    groupdf.drop(columns=["Empid"],inplace=True)

    sumdf = groupdf.groupby(by=["Division","mn","Elemtype_heb"],as_index=False,group_keys=True).agg({"CurAmount":"sum","PrevAmount":"sum","Diff":"sum","SORTCOL":"max"})

    sumdf["SORTCOL"] = sumdf["SORTCOL"]+0.01
    sumdf["Elem_heb"] = "סך " + sumdf["Elemtype_heb"]
    sumdf["Period"] = ''

    resdf = pd.concat([groupdf,sumdf],ignore_index=True)

    resdf.sort_values(by=["mn","SORTCOL","Elem_heb","Period"],ascending=[True,True,True,False],axis=0,ignore_index=True,inplace=True)
    
    resdf.drop(resdf[resdf["Elem_heb"] == "סך מידע"].index, inplace=True)
    
    conn.close()
    
    return groupdf[["Division","mn","Elemtype_heb","Elem_heb","Period","CurAmount","PrevAmount","Diff"]].to_dict('index')
#
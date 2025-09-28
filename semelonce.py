#סמלים שמופיעים פעם אחת
import custom
import pandas as pd
import inspect
import sqlite3

def semelonce(level="0.05"):

    level = float(level)

    conn = sqlite3.connect("dbsave.db")
    cur = conn.cursor()

    REFMONTH = cur.execute("SELECT MAX(Refdate) FROM dfcurr").fetchone()[0]

    query = f"SELECT Empid,Empname,Dirug,Amount,Elem,Elem_heb,Rank FROM dfcurr WHERE Division <> 90 AND Refdate = '{REFMONTH}' AND Elemtype = 'addition components' AND Elem IN {str(tuple(custom.annualvehicle+custom.miluim))} AND Amount <> 0.0"

    middf = pd.read_sql_query(query, conn)

    conn.close()

    #middf = custom.DFCURR.loc[(custom.DFCURR["Division"]!= 90)&(custom.DFCURR["Refdate"]==custom.REFMONTH)&(custom.DFCURR["Amount"]!=0)&(custom.DFCURR["Elemtype"]=="addition components")&(~custom.DFCURR["Elem"].isin((custom.annualvehicle+custom.miluim))),["Rank","Dirug","Elem","Elem_heb","Amount","Empid","Empname"]]

    groupdf = middf.groupby(by=["Rank","Dirug","Elem"],as_index=False,group_keys=True).count()
    groupempdf = middf.groupby(by="Rank",as_index=False,group_keys=True).nunique()

    groupempdf["bench"] = groupempdf["Empid"] * level

    def getbench(row):
        return groupempdf.loc[groupempdf["Rank"] == row["Rank"],"bench"].item()

    groupdf["bench"] = groupdf.apply(getbench, axis=1)

    filterdf = groupdf.loc[(groupdf["Amount"]<4)&(groupdf["Amount"]<groupdf["bench"])]

    def filterrow(row):
        return filterdf.loc[(filterdf["Elem"] == row["Elem"])&(filterdf["Rank"] == row["Rank"])].shape[0] > 0


    middf["filter"] = middf.apply(filterrow,axis=1)

    middf.rename(columns={"Empid":"מספר עובד","Empname":"שם","Elem":"מספר סמל","Elem_heb":"סמל שכר","filter":"מסנן","Dirug":"דירוג","Rank":"דרגה","Amount":"סכום שוטף"},inplace=True)

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        middf.loc[middf["מסנן"] == True, ["מספר עובד","שם","סמל שכר","סכום שוטף"]].to_excel(writer,sheet_name="סמל ייחודי",index=False)
    # 
        

    return  [inspect.stack()[0][3],middf.loc[middf["מסנן"] == True].shape[0],"מספר מקרים של סמל שמופיע פעם אחת"]

#
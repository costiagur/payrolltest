# הפחתות שעות גדולות גם רטרו.
import custom
import pandas as pd
import inspect
import sqlite3

def semel_hourdeduct(level="100"):

    level = float(level)

    conn = sqlite3.connect("dbsave.db")
    cur = conn.cursor()

    #REFMONTH = cur.execute("SELECT MAX(Refdate) FROM dfcurr").fetchone()[0]

    query = f"SELECT Empid,Empname,Refdate,Amount,Elem,Quantity FROM dfcurr WHERE Elem IN ({custom.hourdeduct},{custom.semelnett}) AND Elemtype IN ('additional data','addition components')"

    middf = pd.read_sql_query(query, conn)

    conn.close()

    #middf = custom.DFCURR.loc[(custom.DFCURR["Elem"].isin((custom.hourdeduct,custom.semelnett))&(custom.DFCURR["Elemtype"].isin(["additional data","addition components"])))][["Empid","Empname","Elem","Refdate","Amount","Quantity"]]
    
    middf["Nett"] = middf.apply(lambda row:row["Amount"] if row["Elem"] == custom.semelnett else 0, axis=1 )
    middf["Hourdeduct"] = middf.apply(lambda row:row["Quantity"] if row["Elem"] == custom.hourdeduct else 0, axis=1 )
    
    groupdf = middf.groupby(by=["Empid","Empname"],as_index=False,group_keys=True).sum(["Nett","Hourdeduct"])
    filtereddf = groupdf.loc[((groupdf["Nett"]<1000)&(groupdf["Hourdeduct"]>10))|(groupdf["Hourdeduct"]>level),"Empid"]
    
    middf.rename(columns={"Empid":"מספר עובד","Empname":"שם","Refdate":"תאריך ערך","Nett":"נטו","Hourdeduct":"הפחתת שעות"},inplace=True)

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        middf.loc[(middf["מספר עובד"].isin(filtereddf))&((middf["הפחתת שעות"] != 0)|(middf["נטו"] != 0)),["מספר עובד","שם","תאריך ערך","נטו","הפחתת שעות"]].to_excel(writer,sheet_name="הפחתת שעות גדולה",index=False)
    #    

    return [inspect.stack()[0][3],len(filtereddf.unique()),"מספר עובדים עם הפחתות שעות גדולות"]
#
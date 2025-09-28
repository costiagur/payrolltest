import pandas as pd
import custom
import inspect
import sqlite3

def ratelow(level="1.2"):
    level = float(level)

    pd.set_option('display.float_format', lambda x: '%.2f' % x)

    conn = sqlite3.connect("dbsave.db")
    cur = conn.cursor()

    REFMONTH = cur.execute("SELECT MAX(Refdate) FROM dfcurr").fetchone()[0]

    semellist = list(custom.extrahours) + [custom.konenut,custom.byhourpay,custom.yesod,custom.hourdeduct,custom.semelratio]

    query = f"SELECT Empid,Empname,Refdate,Elem,Elem_heb,Amount,Quantity,WorkHours FROM dfcurr WHERE Division <> 90 AND Refdate = '{REFMONTH}' AND Rank NOT IN {str(tuple(custom.hourwageranks))} AND Elem IN {str(tuple(semellist))}"

    middf = pd.read_sql_query(query, conn)

    conn.close()

    #cols = ["Empid","Empname","Refdate","Elem","Elem_heb","Quantity","Amount","WorkHours"]

    #middf = custom.DFCURR.loc[(custom.DFCURR["Division"] != 90)&(~custom.DFCURR["Rank"].isin(custom.hourwageranks))&(custom.DFCURR["Refdate"]==custom.REFMONTH)&(custom.DFCURR["Elem"].isin(custom.extrahours+(custom.konenut,custom.byhourpay,custom.yesod,custom.hourdeduct,custom.semelratio))),cols]

    def applystack(row):
        res = []
        res = res + [row["Amount"] if row["Elem"] == custom.semelratio else 0]
        res = res + [row["Quantity"] if row["Elem"] in custom.extrahours+(custom.konenut,custom.byhourpay) else -1*row["Quantity"] if row["Elem"] == custom.hourdeduct else 0]
        res = res + [row["WorkHours"] if row["Elem"] == custom.yesod else 0]
        return res
    #

    middf[["GivenRatio","ByhourReg","WorkHours"]] = middf.apply(applystack,axis=1,result_type='expand')

    groupdf = middf.groupby(by=["Empid","Empname"],as_index=False,group_keys=True).sum(["GivenRatio","ByhourReg","WorkHours","GivenRatio","ByhourReg","WorkHours"])

    groupdf["YesodHours"] = groupdf["WorkHours"] - groupdf["ByhourReg"]

    resdf = groupdf.loc[(groupdf["YesodHours"]/173.33 > 1.2*groupdf["GivenRatio"])&(groupdf["Amount"] > 0),["Empid","Empname","GivenRatio","ByhourReg","WorkHours","YesodHours"]]

    resdf.rename(columns={"Empid":"מספר עובד","Empname":"שם עובד","GivenRatio":"חלקיות משרה","ByhourReg":"תשלומי שעות","WorkHours":"שעות עבודה","YesodHours":"שעות תקן לכאורה"},inplace=True)

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer,sheet_name="חלקיות נמוכה",index=False)
    #

    return [inspect.stack()[0][3],len(resdf),"חלקיות נמוכה משעות עבודה"]
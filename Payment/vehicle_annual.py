#בדיקה שך סכום הביטוח אינו עולה על הסכום המרבי
import custom
import pandas as pd
import inspect
import sqlite3


def vehicle_annual(level="2032,7000"):

    conn = sqlite3.connect(custom.dbsave)

    lic,insurance = level.split(",")

    query = f"""
        with CurrElemt AS (SELECT dfcurr.Empid,dfcurr.Empname,dfcurr.Elem ,dfcurr.Amount AS CurrAmount, 0 as PrevAmount
        FROM dfcurr
        WHERE dfcurr.Elem IN {custom.instotal+custom.lics}),
        PrevElemt AS (SELECT dfprev.Empid,dfprev.Empname,dfprev.Elem ,0 AS CurrAmount, dfprev.Amount AS PrevAmount
        FROM dfprev
        WHERE dfprev.Elem IN {custom.instotal+custom.lics}),
        tot AS (Select * FROM CurrElemt UNION ALL Select * FROM PrevElemt)
        SELECT *, SUM(CurrAmount) + SUM(PrevAmount) AS Total FROM tot 
        GROUP BY Empid, Empname, Elem
        HAVING  (SUM(CurrAmount) + SUM(PrevAmount) > {lic} AND Elem IN {custom.lics}) OR (SUM(CurrAmount) + SUM(PrevAmount) > {insurance} AND Elem IN {custom.instotal})
    """


    middf = pd.read_sql(query, conn)

    conn.close()


    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        middf.to_excel(writer,sheet_name="רישיון וביטוח רכב",index=False,header=["מספר עובד","שם","סמל","סכום החודש","סכום חודש שעבר","סך סכום"])
    #  

    return [inspect.stack()[0][3],len(middf),"מקרים של ביטוח רכב בסכום חורג"]
#
    
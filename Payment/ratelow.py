import pandas as pd
import custom
import inspect
import sqlite3

def ratelow(level="1.2"):
    level = float(level)

    pd.set_option('display.float_format', lambda x: '%.2f' % x)

    conn = sqlite3.connect(custom.dbsave)
    cur = conn.cursor()

    REFMONTH = cur.execute("SELECT MAX(Refdate) FROM dfcurr").fetchone()[0]

    query = f"""SELECT dfcurr.Empid, dfcurr.Empname, dfcurr.mn, dfcurr.Amount as GivenRatio, SUM(timesheet.שעות_רגילות) + SUM(timesheet.שעות_100_אינפורמטיב) as Workhours
    FROM dfcurr
    LEFT JOIN timesheet ON dfcurr.Empid = timesheet.מספר_עובד
    WHERE dfcurr.Elem={custom.semelratio} and dfcurr.Refdate = '{REFMONTH}' AND dfcurr.Division <> 90 AND timesheet.פעילות <> "כוננות" AND dfcurr.Rank NOT IN {str(tuple(custom.hourwageranks))}
    GROUP BY dfcurr.Empid ORDER BY Workhours DESC;"""


    middf = pd.read_sql_query(query, conn)

    conn.close()
   

    resdf = middf.loc[(middf["Workhours"]/173.33 > level*middf["GivenRatio"])&(middf["GivenRatio"] > 0),["Empid","Empname","GivenRatio","Workhours"]]

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer,sheet_name="חלקיות נמוכה",index=False,header=["מספר עובד","שם עובד","חלקיות משרה","שעות רגילות"])
    #

    return [inspect.stack()[0][3],len(resdf),"חלקיות נמוכה משעות עבודה"]
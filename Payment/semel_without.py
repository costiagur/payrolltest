import custom
import pandas as pd
import numpy as np
import inspect
import sqlite3

def semel_without(level="0.05"):

    level = 1-float(level)

    conn = sqlite3.connect(custom.dbsave)

#לסנן טבלה של עובדים עם תקפידים
#לבנות טבלה של מספר מופעים של כל סמל לפי דירוג ותפקיד
#לבנות טבלה של מספר עובדים בכל דירוג ותפקיד
#ליצור טבלה לכל עובד של כל הסמלים שיש לו בשורה אחת
#ליצור סינון של מקרים בהם באותה השורה אינו מופיע סמל מסוים מטבלה קודמת, על בסיס התאמה של דירוג ותפקיד

    query = f"""
with CO as(
SELECT dfcurr.Elem_heb, dfcurr.Dirug, jobs.jobname, dfcurr.Empid
FROM dfcurr
LEFT JOIN jobs ON jobs.empid = dfcurr.Empid
WHERE dfcurr.Division <> 90 AND dfcurr.Refdate = (SELECT MAX(Refdate) FROM dfcurr) AND dfcurr.Elemtype = 'addition components' AND Elem NOT IN (1,119,121,122,123,9150,9151,1030,1029,4971,4972,100,124,125,130,91110,1261,1262,1263,261)),

allcases as (
SELECT CO.Elem_heb, CO.Dirug, CO.jobname, COUNT(CO.Empid) as elemcases
 FROM CO
 GROUP BY CO.Elem_heb,CO.Dirug, CO.jobname
 HAVING COUNT(CO.Empid) > 5),

allpeople as (
SELECT CO.Dirug, CO.jobname, COUNT(DISTINCT CO.Empid) as empcases
 FROM CO
 GROUP BY CO.Dirug, CO.jobname),
 
Elemneeded as (
SELECT allcases.Elem_heb, allcases.Dirug, allcases.jobname, elemcases, empcases
FROM allcases
LEFT JOIN allpeople ON allcases.Dirug =allpeople.Dirug AND allcases.jobname =allpeople.jobname
WHERE empcases - elemcases > 0 AND empcases - elemcases < 3
),
Elembyemp as (
SELECT Empid, Dirug, jobname, GROUP_CONCAT(DISTINCT Elem_heb) AS allelems
FROM CO
GROUP BY Empid)
 
SELECT DISTINCT Elembyemp.Empid,dfcurr.Empname as Empname, Elembyemp.Dirug, Elembyemp.jobname,Elemneeded.Elem_heb
FROM Elembyemp
LEFT JOIN Elemneeded ON Elemneeded.Dirug = Elembyemp.Dirug AND  Elemneeded.jobname = Elembyemp.jobname
JOIN dfcurr ON Elembyemp.Empid = dfcurr.Empid
WHERE Elemneeded.Elem_heb not null AND INSTR(allelems, Elemneeded.Elem_heb) = 0
"""

    middf = pd.read_sql_query(query, conn)

    conn.close()


    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        middf.to_excel(writer,sheet_name="ללא סמל",index=True,header=["מספר עובד","שם עובד","דירוג","תפקיד","סמל חסר"])
    #   

    return [inspect.stack()[0][3],middf.shape[0],"עובדים ללא סמל שיש לשאר עובדים בדירוג"]



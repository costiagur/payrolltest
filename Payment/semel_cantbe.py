#סמלים שלא אמורים להיות משולמים, כגון כוננות בחוזה אישי, תוספת קידום ראשון למי שהתחיל לעבוד אחרי 1999
import custom
import pandas as pd
import inspect
import sqlite3

def semel_cantbe(level="0"):  
    
    conn = sqlite3.connect(custom.dbsave)
    cur = conn.cursor()

    REFMONTH = cur.execute("SELECT MAX(Refdate) FROM dfcurr").fetchone()[0]

    query = f"""
    SELECT dfcurr.Empid,dfcurr.Empname,dfcurr.mn,dfcurr.Dirug,dfcurr.Elem_heb,dfcurr.Amount,dfcurr.Quantity 
    FROM dfcurr 
    WHERE 
    (dfcurr.Refdate = '{REFMONTH}' AND dfcurr.Elemtype='addition components' AND dfcurr.Elem NOT IN (1,119,190,193,194,1311,1451,121,122,1616,4971,4972,9150,9151,131,5227) AND dfcurr.Rank IN {custom.hozeishi} AND dfcurr.Amount > 0 AND dfcurr.Division<>90) 
    OR
    (dfcurr.Startdate > '2000-01-01' AND dfcurr.Elem IN (5,9,31,47,64,66,68,69,76,83,110,115,128,140,146,151,152,161,162,165,166,168,170,172,180,202,205,219,235,238,299,333,334,335,426,512,620,640,695,805,849,1001,1007,1008,1015,1040,1049,1052,1069,1104,1368,1369,1429,1511,1665,4600,5119,5124,5246,5247,5261,5298,5321,5472,5609,5635,5820,5829,5830,5837,10193)
      AND dfcurr.Division<>90)
    OR
    (dfcurr.Elem IN ('15','16','17','1056') AND dfcurr.Rank IN (242,241,124,216) AND dfcurr.Division<>90)
    OR
    (dfcurr.Elem IN ('15','17') AND dfcurr.Rank IN (2,141) AND dfcurr.Division<>90)
    OR
    (dfcurr.Elem IN (9) AND dfcurr.Rank NOT IN (141) AND dfcurr.Division<>90)
    OR
    (dfcurr.Elem IN ('250') AND dfcurr.Division<>90)
    OR 
    (dfcurr.Elem = '194' AND dfcurr.Refdate = '{REFMONTH}' AND dfcurr.Empid NOT IN (SELECT dfcurr.Empid FROM dfcurr WHERE dfcurr.Refdate = '{REFMONTH}' AND dfcurr.Elem IN ('190', '193')))
    OR
    (dfcurr.Elem = '119' AND dfcurr.Division=90)
    """

    middf = pd.read_sql_query(query, conn)

    conn.close()
    
    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf = middf[["Empid","Empname","Dirug","Elem_heb","Amount"]].copy()
        resdf.rename(columns={"Empid":"מספר עובד","Empname":"שם","Dirug":"דירוג","Elem_heb":"סמל","Amount":"סכום"},inplace=True)
        middf[["Empid","Empname","Dirug","Elem_heb","Amount"]].to_excel(writer,sheet_name="סמלים לא הגיוניים",index=False)
    # 
        
    return [inspect.stack()[0][3],len(middf),"סמלים לא הגיוניים"]
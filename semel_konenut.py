#כוננות בחוזה אישי
import custom
import pandas as pd
import inspect
import sqlite3

def semel_konenut(level="0"):  
    
    conn = sqlite3.connect("dbsave.db")
    cur = conn.cursor()

    REFMONTH = cur.execute("SELECT MAX(Refdate) FROM dfcurr").fetchone()[0]

    query = f"SELECT Empid,Empname,Dirug,Elem_heb,Quantity FROM dfcurr WHERE Refdate = '{REFMONTH}' AND Elem = {custom.konenut} AND Rank IN {str(tuple(custom.hozeishi))} AND Quantity > 0"

    middf = pd.read_sql_query(query, conn)

    conn.close()
    
    #middf = custom.DFCURR.loc[(custom.DFCURR["Refdate"] == custom.REFMONTH)&(custom.DFCURR["Rank"].isin(custom.hozeishi))&((custom.DFCURR["Elem"] == custom.konenut)&(custom.DFCURR["Quantity"] > 0)),["Empid","Empname","Dirug","Elem_heb","Quantity"]]

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf = middf[["Empid","Empname","Dirug","Elem_heb","Quantity"]].copy()
        resdf.rename(columns={"Empid":"מספר עובד","Empname":"שם","Dirug":"דירוג","Elem_heb":"סמל","Quantity":"כמות"},inplace=True)
        middf[["Empid","Empname","Dirug","Elem_heb","Quantity"]].to_excel(writer,sheet_name="כוננות בחוזה אישי",index=False)
    # 
        
    return [inspect.stack()[0][3],len(middf),"מספר עובדים בחוזה אישי שקיבלו כוננות"]
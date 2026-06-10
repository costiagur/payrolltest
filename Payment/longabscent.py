#עובדים שפתוחים בדוח תפקידים אך לא קיבלו שכר לא החודש ולא חודש שעבר
import custom
import pandas as pd
import inspect
import sqlite3

def longabscent(level = ""):
    conn = sqlite3.connect(custom.dbsave)
    
    query1 = f"""
    SELECT jobs.empid AS מספר_עובד, jobs.empname AS שם_עובד, jobs.jobname AS תפקיד
    FROM jobs
    WHERE jobs.empid NOT IN (SELECT DISTINCT dfcurr.empid FROM dfcurr) AND jobs.empid NOT IN (SELECT DISTINCT dfprev.empid FROM dfprev)
    AND jobs.jobnum NOT IN (20021,991001)
    """

    resdf = pd.read_sql_query(query1, conn)

    conn.close()
    
    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer,sheet_name="עובדים לא עבדו חודשים",index=False, header=True)
    # 
        
    return [inspect.stack()[0][3],len(resdf),"עובדים לא עבדו חודשים"]
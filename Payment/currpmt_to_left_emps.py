#תשלום שכר יסוד לעובדים שקיבלו גמר חשבון בחודש שעבר
# או מקרים של שכר יסוד שוטף לעובד שבמקביל קיבל פיצויים בגין חודש שעבר. צשצע סיים כבר בחודש שעבר
import custom
import pandas as pd
import inspect
import sqlite3

def currpmt_to_left_emps(level = ""):
    conn = sqlite3.connect(custom.dbsave)
    cur = conn.cursor()

    REFMONTH = cur.execute("SELECT MAX(Refdate) FROM dfcurr").fetchone()[0]

    query1 = f"""
    Select dfcurr.Empid, dfcurr.Empname, dfcurr.Refdate, dfcurr.Elem_heb, dfcurr.Stopfrom,dfcurr.Stoptill, dfcurr.Stopname, dfcurr.Amount 
    FROM dfcurr 
    where
    dfcurr.Elem = 1 AND dfcurr.Division <> 90 AND dfcurr.Refdate = {REFMONTH} AND 
    dfcurr.Empid in (SELECT dfcurr.Empid FROM dfcurr WHERE dfcurr.Elem in {str(custom.gmarheshbon)} AND dfcurr.Refdate < {REFMONTH})
    """

    middf1 = pd.read_sql_query(query1, conn)

    query2 = f"""
    Select dfcurr.Empid, dfcurr.Empname, dfcurr.Refdate, dfcurr.Elem_heb, dfcurr.Stopfrom,dfcurr.Stoptill, dfcurr.Stopname, dfcurr.Amount 
    FROM dfcurr 
    where
    dfcurr.Elem = 1 AND dfcurr.Division <> 90 AND dfcurr.Empid IN (SELECT dfprev.Empid FROM dfprev WHERE dfprev.Elem in {str(custom.gmarheshbon)})
    """

    middf2 = pd.read_sql_query(query2, conn)

    query3 = f"""
    SELECT dfcurr.Empid, dfcurr.Empname, dfcurr.Refdate, dfcurr.Elem_heb, dfcurr.Stopfrom,dfcurr.Stoptill, dfcurr.Stopname, dfcurr.Amount
    FROM dfcurr
    WHERE dfcurr.Stopcode <> 1 AND dfcurr.Stopfrom <= {REFMONTH} AND dfcurr.Stoptill >= (SELECT date({REFMONTH}, 'start of month', '+1 month', '-1 day'))
    """

    middf3 = pd.read_sql_query(query3, conn)

    conn.close()

    if not middf1.empty and not middf2.empty:
        middf = pd.concat([middf1,middf2,middf3],ignore_index=True)
    elif not middf1.empty and middf2.empty:
        middf = pd.concat([middf1,middf3],ignore_index=True)
    elif middf1.empty and not middf2.empty:
        middf = pd.concat([middf2,middf3],ignore_index=True)
    else:
        return [inspect.stack()[0][3],0,"יסוד שוטף למופסקים"]
    #

    middf.sort_values(by="Empid",inplace=True,ignore_index=True)

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf = middf[["Empid","Empname","Refdate","Elem_heb","Stopfrom","Stoptill","Stopname","Amount"]].copy()
        resdf.to_excel(writer,sheet_name="יסוד שוטף למופסקים",index=False, header=["מספר עובד","שם","תאריך ערך","סמל","תחילת הפדקה","סיום הפסקה","שם הפסקה","סכום"])
    # 
        
    return [inspect.stack()[0][3],len(resdf),"יסוד שוטף למופסקים"]
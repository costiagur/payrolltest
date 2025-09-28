#נטו שלילי
import custom
import pandas as pd
import inspect
from openpyxl import Workbook, load_workbook
import sqlite3

def nettnegative(level=""):
    
    pd.set_option('display.float_format', lambda x: '%.2f' % x)

    conn = sqlite3.connect("dbsave.db")
    cur = conn.cursor()

    query = f"SELECT Empid,mn,Empname,Amount,Stopname,Stopfrom,Stoptill FROM dfcurr WHERE Elem = {custom.nettnegative}"

    middf = pd.read_sql_query(query, conn)

    middf["Stop"] = middf.apply(lambda row:  "" if row["Stopfrom"] is None else f'{row["Stopname"]} {row["Stopfrom"]} - {row["Stoptill"]}', axis=1)

    conn.close()

    #middf = custom.DFCURR.loc[custom.DFCURR["Elem"]==custom.nettnegative]
    #middf.drop(columns=["Refdate","Division","שם אגף","Dirug","darga","Startdate","Elemtype_heb","Elem_heb","Elem","Rank","Empid_mn","Elemtype","WorkHours","vetek","Quantity","Stopcode"],inplace=True)
    
    with pd.ExcelWriter(custom.xlresfile, mode="a",if_sheet_exists='replace') as writer:
        middf.loc[:,["Empid","Empname","mn","Amount","Stop"]].to_excel(writer,sheet_name="נטו שלילי",float_format="%.2f",header=["מספר עובד","שם עובד","מנ","סכום","הפסקה"],index=False)
    #
 
    return [inspect.stack()[0][3],middf.shape[0],"עובדים עם נטו שלילי"]
#
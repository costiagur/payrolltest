#נטו שלילי
import custom
import pandas as pd

def nettnegative(level=""):
    
    pd.set_option('display.float_format', lambda x: '%.2f' % x)

    empsdf = custom.DF101.loc[(custom.DF101["CurAmount"]!=0)&(custom.DF101["Elemtype"].isin(["addition components","compulsory deductions","voluntary deductions"]))].groupby(["Empid","Empname","Elemtype"],as_index=False).sum("CurAmount")
    empsdf["Nett"] = empsdf.apply(lambda row: row["CurAmount"] if row["Elemtype"] == "addition components" else -1 * row["CurAmount"],axis=1)
    empsdf.drop(columns=["mn","vetek","Division","מחלקה","PrevAmount","PrevQuantity","CurQuantity","CurAmount","Elemtype"],inplace=True)
    nettdf = empsdf.groupby(["Empid","Empname"],as_index=False).sum("Nett")
    
    nettdf.rename(columns={"Empid":"מספר עובד","Empname":"שם","Nett":"נטו שלילי","WorkHours":"שעות עבודה"},inplace=True)

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        nettdf.loc[nettdf["נטו שלילי"] < -10].to_excel(writer,sheet_name="נטו שלילי",index=False)
    #
 
    return nettdf.loc[nettdf["נטו שלילי"] < -10].shape[0]
#
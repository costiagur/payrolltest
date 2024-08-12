#ברוטו ביטוח לאומי מעל התקרה
import custom
import pandas as pd

def highgrossbtl(level="47465"):

    level = float(level)

    resdf = custom.DF101[(custom.DF101["Division"] != custom.pensiondepartment)&(custom.DF101["Elem"] == custom.grossbtlsemel)&(custom.DF101["Refdate"] == custom.REFMONTH)&(custom.DF101["CurAmount"] > level)][["Empid","Empname","mn","Elem_heb","CurQuantity"]]

    resdf.rename(columns={"Empid":"מספר עובד","Empname":"שם","mn":"מנ","Elem_heb":"סמל שכר","CurQuantity":"כמות שוטפת"},inplace=True)

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer,sheet_name="ברוטו בל גבוה",index=False)
    #  

    return len(resdf["מספר עובד"].unique())
#

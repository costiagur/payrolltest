#ברוטו ביטוח לאומי מעל התקרה
import custom
import pandas as pd

def highgrossbtl(level="47465"):

    level = float(level)

    resdf = custom.DF101[(custom.DF101["Division"] != custom.pensiondepartment)&(custom.DF101["Elem"] == custom.grossbtlsemel)&(custom.DF101["Refdate"] == custom.REFMONTH)&(custom.DF101["CurAmount"] > level)][["Empid","Empname","mn","Elem_heb","CurQuantity"]]

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer,sheet_name="highgrossbtl",index=False)
    #  

    return len(resdf["Empid"].unique())
#

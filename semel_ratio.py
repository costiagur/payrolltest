#חלקיות משרה מעל 100%
import custom
import pandas as pd

def semel_ratio(level="1.1"):

    level = float(level)

    resdf = custom.DF101[(custom.DF101["Elem"] == custom.semelratio)&(custom.DF101["Refdate"] == custom.REFMONTH)&(custom.DF101["CurAmount"]>level)][["Empid","Empname","mn","Elem_heb","CurAmount"]]

    resdf.rename(columns={"Empid":"מספר עובד","Empname":"שם","mn":"מנ","Elem_heb":"סמל שכר","CurAmount":"סכום שוטף"},inplace=True)


    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer,sheet_name="חלקיות",index=False)
    # 

    resdf.head(10)

    return len(resdf)

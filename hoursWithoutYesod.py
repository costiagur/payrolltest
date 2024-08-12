import custom
import pandas as pd
import numpy as np

#יש דיווח של שעות עבודה לתלוש אך אין תשלום סמל שכר יסוד

def hoursWithoutYesod(level=""):

    Elem1_100 = custom.DF101.loc[(custom.DF101["Elem"].isin(custom.yesodandhours))&(custom.DF101["Refdate"] == custom.REFMONTH)&(custom.DF101["Division"] != custom.pensiondepartment),"Empid_mn"]

    hours = custom.DFHOURS.loc[custom.DFHOURS["WorkHours"] > 0,"Empid_mn"]

    dataNotin = np.isin(hours,Elem1_100,invert=True) #find which are present in hours and not in DF101
    resdf = custom.DFHOURS.loc[dataNotin].copy()

    resdf.rename(columns={"Empid":"מספר עובד","Empname":"שם","mn":"מנ","CurAmount":"סכום שוטף","Refdate":"תאריך ערך","WorkHours":"שעות עבודה"},inplace=True)

    resdf.drop(columns=["Empid_mn","Elem"],inplace=True)

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer,sheet_name="שעות ללא יסוד",index=False)
    #    
    
    return len(resdf["מספר עובד"])


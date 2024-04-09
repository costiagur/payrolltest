import custom
import pandas as pd

#יש דיווח של שעות עבודה לתלוש אך אין תשלום סמל שכר יסוד

def hoursWithoutYesod(level="8.5"):

    level = float(level)
    
    DF1_100 = custom.DF101.loc[(custom.DF101["Elem"].isin(custom.yesodandhours))&(custom.DF101["CurAmount"] > 0)&(custom.DF101["Refdate"] == custom.REFMONTH)&(custom.DF101["Division"] != custom.pensiondepartment),["Empid","Empname","mn","Refdate","Empid_mn","Elem","CurAmount"]]

    DFHOURS100 = custom.DFHOURS.copy()

    DFHOURS100["Elem"] = "100"

    DFHOURS1_100 = pd.concat([custom.DFHOURS,DFHOURS100],ignore_index=True)    

    merged = pd.merge(DFHOURS1_100,DF1_100,how="left", on=["Empid","Empname","mn","Empid_mn","Refdate","Elem"])

    merged.drop(columns="Empid_mn",inplace=True)

    merged1 = merged[(merged["CurAmount"].isna())&(merged["Elem"] == "1")]
    merged100 = merged[(merged["CurAmount"].isna())&(merged["Elem"] == "100")]

    resdf = pd.merge(merged1,merged100,how="inner",on=["Empid","Empname","mn","Refdate"])

    resdf

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer,sheet_name="HoursWithoutYesod",index=False)
    #    
    
    return len(resdf["Empid"])


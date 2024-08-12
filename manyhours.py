#עובדים עם מספר שעות רב מדי
import custom
import pandas as pd

def manyhours(level="264"):
    
    level= float(level)
    
    middf = custom.DF101.loc[(custom.DF101['Elem'].isin((custom.yesod,custom.konenut)))&(custom.DF101["Division"]!=custom.pensiondepartment)&(custom.DF101["Refdate"]==custom.REFMONTH),["Empid","Empname","mn","Elem_heb","CurQuantity","Elem","WorkHours"]]

    middf["CurQuantity"] = middf.apply(lambda row: -1 * row["CurQuantity"] if row["Elem"] == custom.konenut else row["WorkHours"],axis=1)

    groupdf = middf.groupby(by = ["Empid","Empname","mn"],as_index=False,group_keys=True).sum("CurQuantity")

    groupdf.rename(columns={"Empid":"מספר עובד","Empname":"שם","mn":"מנ","CurQuantity":"כמות שעות שוטפת","WorkHours":"שעות עבודה"},inplace=True)

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        groupdf.loc[groupdf["כמות שעות שוטפת"] >=level].to_excel(writer,sheet_name="מספר שעות רב",index=False)
    #
 
    return len(groupdf.loc[groupdf["כמות שעות שוטפת"] >=level,"מספר עובד"].unique())
#
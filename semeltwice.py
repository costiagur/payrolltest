#סמל שמופיע מספר פעמים באותו תאריך ערך
import custom
import pandas as pd

def semeltwice(level="1"):
    level = int(level)

    middf = custom.DF101[custom.DF101["CurAmount"] != 0]
    grouped = middf.groupby(by=["Empid","Empname","mn","Refdate","Elem_heb"],as_index=False,group_keys=True)
    groupdf = grouped["CurAmount"].count()
    resdf = groupdf[groupdf["CurAmount"] > level]
    resdf.rename(columns={"CurAmount":"Count"}, inplace=True)

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer,sheet_name="semeltwice",index=False)
    #

    return len(resdf["Empid"].unique())
#
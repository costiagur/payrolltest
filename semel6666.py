#6666 ו 6667 שווים
import custom
import pandas as pd

def semel6666(level=""):

    middf = custom.DF101[(custom.DF101["Refdate"] == custom.REFMONTH)&(custom.DF101["Elem"].isin(("6666","6667")))]

    resdf = middf.groupby(by = ["Empid","Empname","mn"],as_index=False,group_keys=True).sum("CurAmount")

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer,sheet_name="6666_6667",index=False)
    #             
    
    return len(resdf.loc[resdf["CurAmount"] > 0,"Empid"].unique())
# 
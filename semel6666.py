#6666 ו 6667 שווים
import pandas as pd
import numpy as np

def semel6666(df,xlwriter,refmonth,prevmonth,level="0"):

    middf = df[(df["Refdate"] == refmonth)&(df["Elem"].isin(("6666","6667")))]
    
    resdict = dict()
    resdict["Empid"] = []
    resdict["Elem"] = []
    resdict["CurAmount"] = []


    for eachid in middf["Empid"].unique():
        
        if middf.loc[(middf["Empid"] == eachid),"CurAmount"].sum() != 0:
            for eachelem in middf.loc[middf["Empid"] == eachid,"Elem"]:
                resdict["Empid"].append(eachid)
                resdict["Elem"].append(eachelem)
                resdict["CurAmount"].append(sum(middf.loc[(middf["Empid"] == eachid)&(middf["Elem"] == eachelem),"CurAmount"].sum()))
        #
   
    
    resdf = pd.DataFrame.from_dict(resdict)
    resdf.to_excel(xlwriter,sheet_name="6666_6667",index=False)
    return len(resdf["Empid"].unique())
# 
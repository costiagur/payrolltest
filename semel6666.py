#6666 ו 6667 שווים
import pandas as pd
import numpy as np

def semel6666(df,xlwriter,refmonth,prevmonth,level="0"):

    middf = df[(df["Refdate"] == refmonth)&(df["Elem"].isin(("6666","6667")))]
    
    resdict = dict()
    resdict["Empid"] = []
    resdict["Empname"] = []
    resdict["Elem_heb"] = []
    resdict["CurAmount"] = []


    for eachid in middf["Empid"].unique():
        
        if middf.loc[(middf["Empid"] == eachid),"CurAmount"].sum() != 0:
            resdict["Empid"] = resdict["Empid"] + middf.loc[(middf["Empid"] == eachid),"Empid"].to_list()
            resdict["Empname"] = resdict["Empname"] + middf.loc[(middf["Empid"] == eachid),"Empname"].to_list()
            resdict["Elem_heb"] = resdict["Elem_heb"] + middf.loc[(middf["Empid"] == eachid),"Elem_heb"].to_list()
            resdict["CurAmount"] = resdict["CurAmount"] + middf.loc[(middf["Empid"] == eachid),"CurAmount"].to_list()
        #
    #
    
    resdf = pd.DataFrame.from_dict(resdict)
    resdf.to_excel(xlwriter,sheet_name="6666_6667",index=False)
    return len(resdf["Empid"].unique())
# 
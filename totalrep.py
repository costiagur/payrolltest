#מצג כולל

import pandas as pd
import numpy as np

def totalrep(df,xlwriter,refmonth,prevmonth):

    df["CurofCur"] = df["CurAmount"] * (df["Refdate"] == refmonth) * (df["Elemtype"] == "addition components")
    df["RetrofCur"] = df["CurAmount"] * (df["Refdate"] < refmonth) * (df["Elemtype"] == "addition components")
    df["CurofPrev"] =  df["PrevAmount"] * (df["Refdate"] == prevmonth) * (df["Elemtype"] == "addition components")
    df["NetCur"] =  df["CurAmount"] * (df["Elem"] == "91096")

    groupdf = df.groupby(by = ["Empname","Empid","Elemtype"],as_index=False,group_keys=True).sum(["CurofCur","RetrofCur","CurofPrev","NetCur"])
    groupdf.drop(columns=["mn","וותק","אגף","מחלקה","PrevQuantity","CurQuantity"],inplace=True)
    groupdf["CurrDiff"] = (groupdf["CurofCur"] -  groupdf["CurofPrev"])

    resdict = {}
    resdict["Empid"] = []
    resdict["Empname"] = []
    resdict["Net"] = []
    resdict["CurrGross"] = []
    resdict["RetroGross"] = []
    resdict["CompulsoryDeduct"] = []
    resdict["VoluntaryDeduct"] = []
    resdict["PrevCurrGross"] = []
    resdict["CurrDiffGross"] = []

    for eachid in groupdf["Empid"].unique():
        resdict["Empid"].append(eachid)
        resdict["Empname"].append(groupdf.loc[groupdf["Empid"] == eachid,"Empname"].unique()[0])
        resdict["Net"].append(groupdf.loc[groupdf["Empid"] == eachid,"NetCur"].sum())
        resdict["CurrGross"].append(groupdf.loc[(groupdf["Empid"] == eachid)&(groupdf["Elemtype"]=="addition components"),"CurofCur"].sum())
        resdict["RetroGross"].append(groupdf.loc[(groupdf["Empid"] == eachid)&(groupdf["Elemtype"]=="addition components"),"RetrofCur"].sum())
        resdict["CompulsoryDeduct"].append(groupdf.loc[(groupdf["Empid"] == eachid)&(groupdf["Elemtype"]=="compulsory deductions"),"CurAmount"].sum())
        resdict["VoluntaryDeduct"].append(groupdf.loc[(groupdf["Empid"] == eachid)&(groupdf["Elemtype"]=="voluntary deductions"),"CurAmount"].sum())
        resdict["PrevCurrGross"].append(groupdf.loc[(groupdf["Empid"] == eachid)&(groupdf["Elemtype"]=="addition components"),"PrevAmount"].sum())
        resdict["CurrDiffGross"].append(groupdf.loc[(groupdf["Empid"] == eachid)&(groupdf["Elemtype"]=="addition components"),"CurrDiff"].sum())
    #

    resdf = pd.DataFrame.from_dict(resdict)

    resdf.head(10)

    resdf.to_excel(xlwriter,sheet_name="Total",index=False)

#
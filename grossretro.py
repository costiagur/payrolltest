    #הפרשי ברוטו ברטרו
import numpy as np
import custom
import pandas as pd

def grossretro(level="5000,0.2"):

    levellist = level.split(",")
    levellist = level.split(",")
    cutoffrate = min([float(eachlevel) for eachlevel in levellist])
    cutoffamount = max([float(eachlevel) for eachlevel in levellist])

    grossretro = custom.DF101.loc[(custom.DF101["Elemtype"] == "addition components")&(custom.DF101["Refdate"] < custom.REFMONTH)].groupby(by = ["Empid"],as_index=False,group_keys=True).sum("CurAmount")
    grossretro = grossretro.loc[(grossretro['CurAmount']>=cutoffamount)|(grossretro['CurAmount']<=-cutoffamount)]

    groupdf = custom.DF101.loc[(custom.DF101["Empid"].isin(grossretro["Empid"]))&(custom.DF101["Elemtype"] == "addition components")&(custom.DF101["Refdate"] < custom.REFMONTH)].groupby(by = ["Empid","Empname","Elem_heb","Elem","Refdate"],as_index=False,group_keys=True).sum("CurAmount")
       
    groupdf["Significant"] = groupdf.apply(lambda row: np.round(row["CurAmount"],0) if abs(row["CurAmount"]) >= abs(cutoffrate*grossretro.loc[grossretro['Empid'] == row['Empid'],'CurAmount'].item()) else 0 ,axis=1)

    jsdict = {}

    for eachindex in groupdf["Empid"].unique():
        jsdict[eachindex] = groupdf.loc[(groupdf['Significant']!= 0)&(groupdf['Empid']== eachindex),["Elem_heb","Significant"]].to_dict('records')
    #

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        groupdf.loc[groupdf['Significant']!= 0].to_excel(writer,sheet_name="retrogross")
    #

    return jsdict
    #בדיקת סבירות של ניכוים לקופות

import pandas as pd

def fundsdeduct(df,xlwriter,refmonth,prevmonth,level="0.03,0.15"):
    
    unneeded = ("630","629","666","634","636","610","612","671","622","624","91030","91031","3203")
    cols = ["Empid","Empname","mn","Refdate","Elemtype","Elemtype_heb","Elem","Elem_heb","CurAmount"]
    middf = df[(df["Division"] != 90)&(df["Elemtype"].isin(("addition components","voluntary deductions"))&(~df["Elem"].isin(unneeded))&(df["CurAmount"]!=0.0))][cols]
    grouped = middf.groupby(by = ["Empid","Elemtype"],as_index=False,group_keys=True)
    groupeddf = grouped.sum("CurAmount")

    levellist = level.split(",")

    maxval = max([float(eachlevel) for eachlevel in levellist])
    minxval = min([float(eachlevel) for eachlevel in levellist])

    resdict= dict()
    resdict["Empid"] = []
    resdict["Empname"] = []
    resdict["mn"] = []
    resdict["Refdate"] = []
    resdict["Elemtype_heb"] = []
    resdict["Elem_heb"] = []
    resdict["CurAmount"] = []

    for eachemp in groupeddf["Empid"].unique():
        voldeduct = sum(groupeddf[(groupeddf["Empid"] == eachemp)&(groupeddf["Elemtype"] == "voluntary deductions")]["CurAmount"])
        tosafot = sum(groupeddf[(groupeddf["Empid"] == eachemp)&(groupeddf["Elemtype"] == "addition components")]["CurAmount"])
        
        if tosafot == 0 and voldeduct == 0:
            pass       
        elif (tosafot == 0 and voldeduct != 0) or voldeduct / tosafot > maxval or voldeduct / tosafot < minxval:
            resdict["Empid"] = resdict["Empid"] + middf.loc[middf["Empid"] == eachemp,"Empid"].to_list()
            resdict["Empname"] = resdict["Empname"] + middf.loc[middf["Empid"] == eachemp,"Empname"].to_list()
            resdict["mn"] = resdict["mn"] + middf.loc[middf["Empid"] == eachemp,"mn"].to_list()
            resdict["Refdate"] = resdict["Refdate"] + middf.loc[middf["Empid"] == eachemp,"Refdate"].to_list()
            resdict["Elemtype_heb"] = resdict["Elemtype_heb"] + middf.loc[middf["Empid"] == eachemp,"Elemtype_heb"].to_list()
            resdict["Elem_heb"] = resdict["Elem_heb"] + middf.loc[middf["Empid"] == eachemp,"Elem_heb"].to_list()
            resdict["CurAmount"] = resdict["CurAmount"] + middf.loc[middf["Empid"] == eachemp,"CurAmount"].to_list()
        #  
    #
    resdf = pd.DataFrame.from_dict(resdict)
    resdf.to_excel(xlwriter,sheet_name="Kupotrate",index=False)

    resdf.head(10)

    return len(resdf["Empid"].unique())
#

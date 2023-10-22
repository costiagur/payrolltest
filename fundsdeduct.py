    #בדיקת סבירות של ניכוים לקופות

import pandas as pd

def fundsdeduct(df,xlwriter,refmonth,prevmonth):
    
    unneeded = ("630","629","666","634","636","610","612","671","622","624","91030","91031")
    cols = ["Empid","mn","Refdate","Elemtype","Elem","CurAmount"]
    middf = df[(df["Division"] != 90)&(df["Elemtype"].isin(("addition components","voluntary deductions"))&(~df["Elem"].isin(unneeded))&(df["CurAmount"]!=0.0))][cols]
    grouped = middf.groupby(by = ["Empid","Elemtype"],as_index=False,group_keys=True)
    groupeddf = grouped.sum("CurAmount")

    newdict= dict()
    newdict["Empid"] = []
    newdict["mn"] = []
    newdict["Refdate"] = []
    newdict["Elemtype"] = []
    newdict["Elem"] = []
    newdict["CurAmount"] = []

    for eachemp in groupeddf["Empid"].unique():
        voldeduct = sum(groupeddf[(groupeddf["Empid"] == eachemp)&(groupeddf["Elemtype"] == "voluntary deductions")]["CurAmount"])
        tosafot = sum(groupeddf[(groupeddf["Empid"] == eachemp)&(groupeddf["Elemtype"] == "addition components")]["CurAmount"])
        
        if tosafot == 0 and voldeduct == 0:
            pass       
        elif (tosafot == 0 and voldeduct != 0) or voldeduct / tosafot > 0.15 or voldeduct / tosafot < 0.03:
            for eachrow in range(0,len(middf[middf["Empid"] == eachemp]),1):
                newdict["Empid"].append(eachemp)
                newdict["mn"].append(middf[middf["Empid"] == eachemp].iloc[eachrow,1])
                newdict["Refdate"].append(middf[middf["Empid"] == eachemp].iloc[eachrow,2])
                newdict["Elemtype"].append(middf[middf["Empid"] == eachemp].iloc[eachrow,3])
                newdict["Elem"].append(middf[middf["Empid"] == eachemp].iloc[eachrow,4])
                newdict["CurAmount"].append(middf[middf["Empid"] == eachemp].iloc[eachrow,5])
        #  

        #
    #
    resdf = pd.DataFrame.from_dict(newdict)
    resdf.to_excel(xlwriter,sheet_name="Kupotrate",index=False)

    resdf.head(10)

    return len(resdf["Empid"].unique())
#

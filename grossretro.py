    #הפרשי ברוטו ברטרו
import pandas as pd
import numpy as np

def grossretro(df,xlwriter,refmonth,prevmonth,level="5000,0.2"):

    grouped = df.groupby(by = ["Empid","Empname","Elemtype","Refdate"],as_index=False,group_keys=True)
    groupdf = grouped.sum("CurAmount")
    empids = df[df["Startdate"] <= prevmonth]["Empid"].unique()
    resdict = dict()
    resdict["Empid"] = []
    resdict["Empname"] = []
    resdict["Elem"] = []
    resdict["Diff"] = []
    resdict["Amount"] = []
   
    levellist = level.split(",")

    cutoffrate = min([float(eachlevel) for eachlevel in levellist])
    cutoffamount = max([float(eachlevel) for eachlevel in levellist])

    for eachemp in empids:
        grossretro = sum(groupdf[(groupdf["Empid"] == eachemp)&(groupdf["Elemtype"] == "addition components")&(groupdf["Refdate"] < refmonth)]["CurAmount"])
        
        grossretro = round(grossretro,0)
        
        if abs(grossretro) > cutoffamount:
    
            empname = groupdf.loc[groupdf["Empid"]== eachemp,"Empname"].unique()[0]

            resdict["Empid"].append(eachemp)
            resdict["Empname"].append(empname)
            resdict["Elem"].append("ברוטו רטרו")
            resdict["Diff"].append(grossretro)
            resdict["Amount"].append(0)      


            middf = df[(df["Empid"] == eachemp)&(df["Refdate"] < refmonth)&(df["Elemtype"] == "addition components")]
            
            for eachelem in middf[middf["CurAmount"] != 0]["Elem"].unique():
                retroamount = middf.loc[middf["Elem"] == eachelem,"CurAmount"].sum()
                
                if abs(retroamount)/abs(grossretro) >= cutoffrate:
                    resdict["Empid"].append(eachemp)
                    resdict["Empname"].append(empname)
                    resdict["Elem"].append(middf.loc[(middf["Empid"]== eachemp)&(middf["Elem"] == eachelem),"Elem_heb"].unique()[0])
                    resdict["Diff"].append(0)
                    resdict["Amount"].append(round(retroamount,0))
                #
                        
            #
        #
    #

    resdf = pd.DataFrame.from_dict(resdict)

    resdf.to_excel(xlwriter,sheet_name="grossretro",index=False)

    jsdict = {}
    
    for eachid in resdf["Empid"].unique():
        jsdict[eachid] = {}
        jsdict[eachid] = resdf.loc[resdf["Empid"] == eachid,["Elem","Diff","Amount"]].to_dict('records')
    #

    return [len(resdf["Empid"].unique()),"grossretro",jsdict]
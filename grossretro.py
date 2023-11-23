    #הפרשי ברוטו ברטרו
import pandas as pd

def grossretro(df,xlwriter,refmonth,prevmonth,level="2000,0.2"):

    grouped = df.groupby(by = ["Empid","Empname","Elemtype","Refdate"],as_index=False,group_keys=True)
    groupdf = grouped.sum("CurAmount")
    empids = df[df["Startdate"] <= prevmonth]["Empid"].unique()
    resdict = dict()
    resdict["Empid"] = []
    resdict["Empname"] = []
    resdict["Elem"] = []
    resdict["Diff"] = []
    resdict["Values"] = []
   
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
            resdict["Values"].append(0)      


            middf = df[(df["Empid"] == eachemp)&(df["Refdate"] < refmonth)&(df["Elemtype"] == "addition components")]
            
            for eachelem in middf[middf["CurAmount"] != 0]["Elem"].unique():
                retroamount = middf.loc[middf["Elem"] == eachelem,"CurAmount"].sum()
                
                if abs(retroamount)/abs(grossretro) >= cutoffrate:
                    resdict["Empid"].append(eachemp)
                    resdict["Empname"].append(empname)
                    resdict["Elem"].append(middf.loc[(middf["Empid"]== eachemp)&(middf["Elem"] == eachelem),"Elem_heb"].unique()[0])
                    resdict["Diff"].append(0)
                    resdict["Values"].append(retroamount)
                #
                        
            #
        #
    #

    resdf = pd.DataFrame.from_dict(resdict)

    resdf.to_excel(xlwriter,sheet_name="grossretro",index=False)

    resdf.head(10)

    return [len(resdf["Empid"].unique()),"grossretro"]
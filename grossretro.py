    #הפרשי ברוטו ברטרו
import pandas as pd

def grossretro(df,xlwriter,refmonth,prevmonth,level="2000,0.2"):

    grouped = df.groupby(by = ["Empid","Elemtype","Refdate"],as_index=False,group_keys=True)
    groupdf = grouped.sum("CurAmount")
    empids = set(df[df["Start date"] <= prevmonth]["Empid"])
    resdict = dict()
    resdict["Empid"] = []
    resdict["Elem"] = []
    resdict["Diff"] = []
    resdict["Values"] = []
   
    levellist = level.split(",")

    cutoff = min([float(eachlevel) for eachlevel in levellist])
    cutoamount = max([float(eachlevel) for eachlevel in levellist])

    for eachemp in empids:
        grossretro = sum(groupdf[(groupdf["Empid"] == eachemp)&(groupdf["Elemtype"] == "addition components")&(groupdf["Refdate"] < refmonth)]["CurAmount"])
        
        grossretro = round(grossretro,0)
        
        if abs(grossretro) > cutoamount:
    
            resdict["Empid"].append(eachemp)
            resdict["Elem"].append("RetroGross")
            resdict["Diff"].append(grossretro)
            resdict["Values"].append(0)      


            middf = df[(df["Empid"] == eachemp)&(df["Refdate"] < refmonth)&(df["Elemtype"] == "addition components")]
            
            for eachsemel in middf[(middf["Elemtype"]== "addition components")&(middf["CurAmount"] != 0)]["Elem"].unique():
                retroamount = sum(middf[middf["Elem"] == eachsemel]["CurAmount"])
                
                if abs(retroamount)/abs(grossretro) >= cutoff:
                    resdict["Empid"].append(eachemp)
                    resdict["Elem"].append(eachsemel)
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
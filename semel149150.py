#בדיקה שך סכום הביטוח אינו עולה על הסכום המרבי
import pandas as pd

def semel149150(df,xlwriter,refmonth,prevmonth,level="7000,1750"):

    newdict= dict()
    newdict["Empid"] = []
    newdict["Elem"] = []
    newdict["PrevAmount"] = []
    newdict["CurAmount"] = []

    vehdf = df[df["Elem"].isin(("149","150","7149","7150"))]
 
    levellist = level.split(",")

    maxval = max([float(eachlevel) for eachlevel in levellist])
    minval = min([float(eachlevel) for eachlevel in levellist])

    for eachemp in vehdf["Empid"].unique():
        if sum(vehdf.loc[vehdf["Empid"] == eachemp,["PrevAmount","CurAmount"]].sum()) > maxval:
            for eachrow in range(0,len(vehdf[vehdf["Empid"] == eachemp]),1):
                newdict["Empid"].append(eachemp)
                newdict["Elem"].append(vehdf[vehdf["Empid"] == eachemp].iloc[eachrow,9])
                newdict["PrevAmount"].append(vehdf[vehdf["Empid"] == eachemp].iloc[eachrow,10])
                newdict["CurAmount"].append(vehdf[vehdf["Empid"] == eachemp].iloc[eachrow,12])
            #
        elif sum(vehdf.loc[(vehdf["Empid"] == eachemp)&(vehdf["Elem"].isin(["149","7149"])),["PrevAmount","CurAmount"]].sum()) > minval:
            for eachrow in range(0,len(vehdf[(vehdf["Empid"] == eachemp)&(vehdf["Elem"].isin(("149","7149")))]),1):
                newdict["Empid"].append(eachemp)
                newdict["Elem"].append(vehdf[(vehdf["Empid"] == eachemp)&(vehdf["Elem"].isin(("149","7149")))].iloc[eachrow,9])
                newdict["PrevAmount"].append(vehdf[(vehdf["Empid"] == eachemp)&(vehdf["Elem"].isin(("149","7149")))].iloc[eachrow,10])
                newdict["CurAmount"].append(vehdf[(vehdf["Empid"] == eachemp)&(vehdf["Elem"].isin(("149","7149")))].iloc[eachrow,12])
            
        #
        
    #
    resdf = pd.DataFrame.from_dict(newdict)
    resdf.to_excel(xlwriter,sheet_name="BituahRehev",index=False)

    resdf.head(10)

    return len(resdf["Empid"].unique())
#
    
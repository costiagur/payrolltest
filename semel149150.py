#בדיקה שך סכום הביטוח אינו עולה על הסכום המרבי
import pandas as pd

def semel149150(df,xlwriter,refmonth,prevmonth,level="7000,1750"):

    resdict= dict()
    resdict["Empid"] = []
    resdict["Empname"] = []
    resdict["Elem_heb"] = []
    resdict["PrevAmount"] = []
    resdict["CurAmount"] = []

    vehdf = df[df["Elem"].isin(("149","150","7149","7150"))]
 
    levellist = level.split(",")

    maxval = max([float(eachlevel) for eachlevel in levellist])
    minval = min([float(eachlevel) for eachlevel in levellist])

    for eachemp in vehdf["Empid"].unique():
        if sum(vehdf.loc[vehdf["Empid"] == eachemp,["PrevAmount","CurAmount"]].sum()) > maxval:
            resdict["Empid"] = resdict["Empid"] + vehdf.loc[vehdf["Empid"] == eachemp,"Empid"].to_list()
            resdict["Empname"] = resdict["Empname"] + vehdf.loc[vehdf["Empid"] == eachemp,"Empname"].to_list()
            resdict["Elem_heb"] = resdict["Elem_heb"] + vehdf.loc[vehdf["Empid"] == eachemp,"Elem_heb"].to_list()
            resdict["PrevAmount"] = resdict["PrevAmount"] + vehdf.loc[vehdf["Empid"] == eachemp,"PrevAmount"].to_list()
            resdict["CurAmount"] = resdict["CurAmount"] + vehdf.loc[vehdf["Empid"] == eachemp,"CurAmount"].to_list()
            #
        elif sum(vehdf.loc[(vehdf["Empid"] == eachemp)&(vehdf["Elem"].isin(["149","7149"])),["PrevAmount","CurAmount"]].sum()) > minval:
            resdict["Empid"] = resdict["Empid"] + vehdf.loc[(vehdf["Empid"] == eachemp)&(vehdf["Elem"].isin(("149","7149"))),"Empid"].to_list()
            resdict["Empname"] = resdict["Empname"] + vehdf.loc[(vehdf["Empid"] == eachemp)&(vehdf["Elem"].isin(("149","7149"))),"Empname"].to_list()
            resdict["Elem_heb"] = resdict["Elem_heb"] + vehdf.loc[(vehdf["Empid"] == eachemp)&(vehdf["Elem"].isin(("149","7149"))),"Elem_heb"].to_list()
            resdict["PrevAmount"] = resdict["PrevAmount"] + vehdf.loc[(vehdf["Empid"] == eachemp)&(vehdf["Elem"].isin(("149","7149"))),"PrevAmount"].to_list()
            resdict["CurAmount"] = resdict["CurAmount"] + vehdf.loc[(vehdf["Empid"] == eachemp)&(vehdf["Elem"].isin(("149","7149"))),"CurAmount"].to_list()
        #
    #
    resdf = pd.DataFrame.from_dict(resdict)
    resdf.to_excel(xlwriter,sheet_name="BituahRehev",index=False)

    resdf.head(10)

    return len(resdf["Empid"].unique())
#
    
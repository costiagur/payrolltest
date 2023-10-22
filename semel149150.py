#בדיקה שך סכום הביטוח אינו עולה על הסכום המרבי
import pandas as pd

def semel149150(df,xlwriter,refmonth,prevmonth):

    newdict= dict()
    newdict["Empid"] = []
    newdict["Elem"] = []
    newdict["PrevAmount"] = []
    newdict["CurAmount"] = []

    vehdf = df[df["Elem"].isin(("149","150","7149","7150"))]
    sumlist = []
    for i in range(0,len(vehdf),1):
        sumlist.append(sum(vehdf.iloc[i,[10,12]]))
    #
    vehdf["Total"] = sumlist


    for eachemp in vehdf["Empid"].unique():
        if sum(vehdf[vehdf["Empid"] == eachemp]["Total"]) > 7000:
            for eachrow in range(0,len(vehdf[vehdf["Empid"] == eachemp]),1):
                newdict["Empid"].append(eachemp)
                newdict["Elem"].append(vehdf[vehdf["Empid"] == eachemp].iloc[eachrow,9])
                newdict["PrevAmount"].append(vehdf[vehdf["Empid"] == eachemp].iloc[eachrow,10])
                newdict["CurAmount"].append(vehdf[vehdf["Empid"] == eachemp].iloc[eachrow,12])
            #
        elif sum(vehdf[(vehdf["Empid"] == eachemp)&(vehdf["Elem"] .isin(("149","7149")))]["Total"]) > 1750:
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
    
import pandas as pd
#יש סמל 1313 אך אין תשלום סמל 1

def semel1313(df,df1313,xlwriter,refmonth,prevmonth,level="8.5"):

    level = float(level)
    
    middf1313 = df1313.loc[df1313["Quantity"] > level,["Empid","mn"]]

    resid = []

    resdict = {}

    resdict["Empid"] = []
    resdict["Empname"] = []
    resdict["mn"] = []
    resdict["1313"] = []

    for _,i1,i2 in list(middf1313.to_records()):
        if df.loc[(df["Empid"] == i1)&(df["mn"] ==i2)&(df["Elem"].isin(("1","100")))&(df["Refdate"] == refmonth),"CurAmount"].sum() > 0:
            resid.append(str(i1)+"_"+str(i2))
    #

    seta = set([str(i1)+"_"+str(i2) for _,i1,i2 in df1313.loc[df1313["Quantity"] > level,["Empid","mn"]].to_records()])
    setb = set(resid)
    
    difset = seta.difference(setb)

    for idmn in difset:
        id = int(idmn.split("_")[0])
        mn = int(idmn.split("_")[1])
        
        resdict["Empid"].append(id)
        resdict["mn"].append(mn)
        resdict["Empname"].append(df1313.loc[df1313["Empid"]==id,"Empname"].unique()[0])
        resdict["1313"].append(df1313.loc[(df1313["Empid"]==id)&(df1313["mn"]==mn),"Quantity"].sum())
    #


    resdf = pd.DataFrame.from_dict(resdict)
    resdf.to_excel(xlwriter,sheet_name="1313_no_1",index=False)
    
    return len(resdict["Empid"])


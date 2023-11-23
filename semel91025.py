import pandas as pd
import numpy as np
#בסיס פנסיה מחושב אינו סביר ביחס לבסיס פנסיה בתלוש. לדוגמה כאשר חלקיות אינה סבירה ביחס לבסיס הפנסיה

def semel91025(df,xlwriter,refmonth,prevmonth,level="0.1"):

    idlist = []
    level = float(level)
    filterout = set(df[df["mn"]==99]["Empid"].values)
    semels = ("90148","91203","91025","119","5843","5842","1","2151","1039","30501")

    middf = df[(df["Refdate"] == refmonth)&(df["Startdate"] <= prevmonth)&(~df["Empid"].isin(filterout))&(df["Division"] != 90)&(df["Elem"].isin(semels))&(~df["Rank"].isin((75,91)))]
    
    for each in middf[["Empid","mn"]].to_records():
            idlist.append(str(each[1])+"_"+str(each[2]))
    #

    resdict = dict()
    resdict["Empid"] = []
    resdict["mn"] = []
    resdict["Empname"] = []
    resdict["wageRate"] = []
    resdict["EstBasis"] = []
    resdict["PensionBasis"] = []
    resdict["Ratio"] = []

    for strid in set(idlist):
        id,mn = strid.split("_")
        id = int(id)
        mn = int(mn)
        
        if middf.loc[(middf["Empid"] == id)&(middf["mn"] == mn)&(middf["Elem"] == "1"),"CurAmount"].sum() <=0:
            continue
        else:
            helkiut = middf.loc[(middf["Empid"] == id)&(middf["mn"] == mn)&(middf["Elem"] == "90148"),"CurAmount"].sum()

            estbasis = helkiut*min(middf.loc[(middf["Empid"] == id)&(middf["mn"] == mn)&(middf["Elem"] == "91203"),"CurAmount"].to_list())*177.77 #there are both ereh yom and ereh shaa

            if middf.loc[(middf["Empid"] == id)&(middf["mn"] == mn)&(middf["Elem"] == "30501"),"CurAmount"].sum() != 0:
                estbasis = estbasis - middf.loc[(middf["Empid"] == id)&(middf["mn"] == mn)&(middf["Elem"].isin(["5843","5842"])),"CurAmount"].sum()
            #במקרה של תקציבית, צריך לנכות את שני הסמלים שהם מוגדרים כצוברת ולכן יכנסו לקופת עבודה נוספת

            bsispensia = middf.loc[(middf["Empid"] == id)&(middf["mn"] == mn)&(middf["Elem"] == "91025"),"CurAmount"].sum()
            bsispensia = bsispensia - middf.loc[(middf["Empid"] == id)&(middf["mn"] == mn)&(middf["Elem"].isin(("119","2151","1039"))),"CurAmount"].sum()

            ratio = estbasis/(bsispensia if bsispensia != 0 else np.nan()) 

            if ratio > 1+level or (ratio < 1-level and ratio != 0):
                resdict["Empid"].append(id)
                resdict["mn"].append(mn)
                resdict["Empname"].append(middf.loc[middf["Empid"] == id,"Empname"].unique()[0])
                resdict["wageRate"].append(helkiut)
                resdict["EstBasis"].append(estbasis)
                resdict["PensionBasis"].append(bsispensia)
                resdict["Ratio"].append(ratio)
                
            #
        #
    #

    resdf = pd.DataFrame.from_dict(resdict)

    print(resdf.head(10))

    resdf.to_excel(xlwriter,sheet_name="pensionbase",index=False)

    resdf.head(10)

    return [len(resdf),"semel91025"]
#
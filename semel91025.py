import pandas as pd
#בסיס פנסיה מחושב אינו סביר ביחס לבסיס פנסיה בתלוש. לדוגמה כאשר חלקיות אינה סבירה ביחס לבסיס הפנסיה

def semel91025(df,xlwriter,refmonth,prevmonth):
    filterout = set(df[df["mn"]==99]["Empid"].values)
    semels = ("90148","91203 - Value time","91025","119","5843","5842","1","2151","1039","30501")

    middf = df[(df["Refdate"] == refmonth)&(df["Start date"] <= refmonth)&(~df["Empid"].isin(filterout))&(df["Division"] != 90)&(df["Elem"].isin(semels))&(~df["Rank"].isin((75,91)))]
    idlist = set(middf["Empid"].values)

    resdict = dict()
    resdict["Empid"] = []
    resdict["wageRate"] = []
    resdict["EstBasis"] = []
    resdict["PensionBasis"] = []
    resdict["Ratio"] = []

    for eachid in idlist:
        if sum(middf[(middf["Empid"] == eachid)&(middf["Elem"] == "1")]["CurAmount"].values) <=0:
            continue
        else:
            helkiut = sum(middf[(middf["Empid"] == eachid)&(middf["Elem"] == "90148")]["CurAmount"].values)

            estbasis = helkiut*sum(middf[(middf["Empid"] == eachid)&(middf["Elem"] == "91203 - Value time")]["CurAmount"].values)*182

            if sum(middf[(middf["Empid"] == eachid)&(middf["Elem"] == "30501")]["CurAmount"].values) != 0:
                estbasis = estbasis - sum(middf[(middf["Empid"] == eachid)&(middf["Elem"].isin(["5843","5842"]))]["CurAmount"].values)
            #במקרה של תקציבית, צריך לנכות את שני הסמלים שהם מוגדרים כצוברת ולכן יכנסו לקופת עבודה נוספת

            bsispensia = sum(middf[(middf["Empid"] == eachid)&(middf["Elem"] == "91025")]["CurAmount"].values)
            bsispensia = bsispensia -sum(middf[(middf["Empid"] == eachid)&(middf["Elem"].isin(("119","2151","1039")))]["CurAmount"].values)       

            ratio = estbasis/(bsispensia if bsispensia != 0 else 1) 


            if ratio > 1.1 or ratio < 0.9:
                resdict["Empid"].append(eachid)
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
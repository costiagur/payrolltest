#השוואת ברוטו שוטף ללא חד שנתיים
import pandas as pd

def grosscur(df,xlwriter,refmonth,prevmonth,level="0.2,2000"):
    
    grouped = df.groupby(by = ["Empid","Empname","Elemtype","Refdate"],as_index=False,group_keys=True)
    groupdf = grouped.sum(["PrevAmount","CurAmount"])
    empids = set(df[df["Startdate"] <= prevmonth]["Empid"])
    
    annualelem = ["2276","2278","290","291","295","2151","4737","5831"]
    #annualelem - תשתלומים שנתיים. לא מעניינים לצורך בדיקה זו
    byreport = ["1","16","17","32","153","158","169","1056","100","1034","1039","4200","4500","4501","5127","5128","5234","5243","5244","5245","5403","5404","5405","5410","5411","5465","5466","5467","5840","5841","5842","5843"]
    #byreport - סמלים שצריך לדווח והם בבסיס הפנסיה ולכן תלויים בחלקיות משרה

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
        grosscurr = sum(groupdf[(groupdf["Empid"] == eachemp)&(groupdf["Elemtype"] == "addition components")&(groupdf["Refdate"] == refmonth)]["CurAmount"])
        grossprev = sum(groupdf[(groupdf["Empid"] == eachemp)&(groupdf["Elemtype"] == "addition components")&(groupdf["Refdate"] == prevmonth)]["PrevAmount"])
        grosscurr = grosscurr - sum(df[(df["Empid"] == eachemp)&(df["Refdate"] == refmonth)&(df["Elem"].isin(annualelem))]["CurAmount"])
        grossprev = grossprev - sum(df[(df["Empid"] == eachemp)&(df["Refdate"] == prevmonth)&(df["Elem"].isin(annualelem))]["PrevAmount"])
        
        grossdiff = grosscurr - grossprev
        grossdiff = round(grossdiff,0)
        
        if abs(grossdiff) > cutoffamount:
            
            middf = df[(df["Empid"] == eachemp)&(df["Refdate"] >= prevmonth)]
            
            currate = sum(middf[(middf["Refdate"] == refmonth)&(middf["Elem"] == "90148")]["CurAmount"])
            prevrate = sum(middf[(middf["Refdate"] == prevmonth)&(middf["Elem"] == "90148")]["PrevAmount"])
            prevbase = sum(middf[(middf["Refdate"] == prevmonth)&(middf["Elem"] == "91025")]["PrevAmount"])
            prevbase = prevbase - sum(middf[middf['Elem'].isin(("2151","290"))]["PrevAmount"])

            empname = middf.loc[middf["Empid"]== eachemp,"Empname"].unique()[0]

            resdict["Empid"].append(eachemp)
            resdict["Empname"].append(empname)
            resdict["Elem"].append("הפרש ברוטו שוטף")
            resdict["Diff"].append(grossdiff)
            resdict["Amount"].append(0)      
            
            resdict["Empid"].append(eachemp)
            resdict["Empname"].append(empname)
            resdict["Elem"].append("חלקיות קודמת")
            resdict["Diff"].append(prevrate)
            resdict["Amount"].append(0)

            resdict["Empid"].append(eachemp)
            resdict["Empname"].append(empname)
            resdict["Elem"].append("חלקיות החודש")
            resdict["Diff"].append(currate)
            resdict["Amount"].append(0)

            if prevrate == 0 and currate != 0:
                rateadd = prevbase
            elif prevrate == 0 and currate == 0: #if there is no rate
                pass
            else:
                rateadd = prevbase * (currate / prevrate - 1)
            #
            
            if abs(rateadd)/abs(grossdiff) >= cutoffrate:       
                resdict["Empid"].append(eachemp)
                resdict["Empname"].append(empname)
                resdict["Elem"].append("91025 - בסיס הפנסיה")
                resdict["Diff"].append(0)
                resdict["Amount"].append(round(rateadd,0))
            #
            
            unproratedf = middf[(~middf["Elem"].isin(byreport+annualelem))&(middf["Elemtype"] == "addition components")] #סמלים שאינם קשורים לבסיס הפנסיה
            
            for eachelem in unproratedf['Elem'].unique(): #not prorate
                prevsum = sum(unproratedf[(unproratedf["Elem"] == eachelem)]["PrevAmount"])
                currsum = sum(unproratedf[(unproratedf["Refdate"] == refmonth)&(unproratedf["Elem"] == eachelem)]["CurAmount"])
                if abs(currsum-prevsum)/abs(grossdiff) >= cutoffrate:
                    resdict["Empid"].append(eachemp)
                    resdict["Empname"].append(empname)
                    resdict["Elem"].append(unproratedf.loc[(unproratedf["Empid"]== eachemp)&(unproratedf["Elem"] == eachelem),"Elem_heb"].unique()[0])
                    resdict["Diff"].append(0)
                    resdict["Amount"].append(round(currsum-prevsum,0))
                #
            #

            byreportdf =  middf[middf["Elem"].isin(byreport)]

            for eachelem in byreportdf['Elem'].unique(): #above prorate

                diffamount = 0
                
                prevsum = sum(byreportdf[(byreportdf["Elem"] == eachelem)]["PrevAmount"])
                currsum = sum(byreportdf[(byreportdf["Refdate"] == refmonth)&(byreportdf["Elem"] == eachelem)]["CurAmount"])
                
                if prevrate == 0 and currate != 0:
                    pass
                elif prevrate == 0 and currate == 0: #if there is no rate
                    pass
                else:
                    diffamount = currsum - prevsum * (currate / prevrate)
                #            
                
                if abs(diffamount)/abs(grossdiff) >= cutoffrate:
                    resdict["Empid"].append(eachemp)
                    resdict["Empname"].append(empname)
                    resdict["Elem"].append(byreportdf.loc[(byreportdf["Empid"]== eachemp)&(byreportdf["Elem"] == eachelem),"Elem_heb"].unique()[0])
                    resdict["Diff"].append(0)
                    resdict["Amount"].append(round(diffamount,0))
                #
            #      
        #
    #
    resdf = pd.DataFrame.from_dict(resdict)

    resdf.to_excel(xlwriter,sheet_name="currgross_diff",index=False)

    jsdict = {}

    for eachid in resdf["Empid"].unique():
        jsdict[eachid] = {}
        jsdict[eachid] = resdf.loc[resdf["Empid"] == eachid,["Elem","Diff","Amount"]].to_dict('records')
    #

    return [len(resdf["Empid"].unique()),"grosscur",jsdict]
#
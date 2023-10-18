#השוואת ברוטו שוטף ללא חד שנתיים
import pandas as pd

def grosscur(df,xlwriter,refmonth,prevmonth):
    
    grouped = df.groupby(by = ["Empid","Elemtype","Refdate"],as_index=False,group_keys=True)
    groupdf = grouped.sum(["PrevAmount","CurAmount"])
    empids = set(df[df["Start date"] <= prevmonth]["Empid"])
    
    annualelem = ["143","149","150","7143","7149","7150","4971","4972","2276","2278","290","291","295","1069","2151","4737","5831"]
    unprorate = ["48","65","117","119","120","121","122","123","124","125","126","127","130","132","133","139","163","167","177","215","216","232","236","5258","5241","131","137","173","190","191","192","193","194","217","218","284","285","338","501","502","1311","1315","1365","1616","1367","1451","1922","5227"]
    byreport = ["1","16","17","32","153","158","169","1056","100","1034","1039","4200","4500","4501","5127","5128","5234","5243","5244","5245","5403","5404","5405","5410","5411","5465","5466","5467","5840","5841","5842","5843"]
    
    resdict = dict()
    resdict["Empid"] = []
    resdict["Elem"] = []
    resdict["Diff"] = []
    resdict["Values"] = []

    cutoff = 0.2
    cutoamount = 2000

    for eachemp in empids:
        grosscurr = sum(groupdf[(groupdf["Empid"] == eachemp)&(groupdf["Elemtype"] == "addition components")&(groupdf["Refdate"] == refmonth)]["CurAmount"])
        grossprev = sum(groupdf[(groupdf["Empid"] == eachemp)&(groupdf["Elemtype"] == "addition components")&(groupdf["Refdate"] == prevmonth)]["PrevAmount"])
        grosscurr = grosscurr - sum(df[(df["Empid"] == eachemp)&(df["Refdate"] == refmonth)&(df["Elem"].isin(annualelem))]["CurAmount"])
        grossprev = grossprev - sum(df[(df["Empid"] == eachemp)&(df["Refdate"] == prevmonth)&(df["Elem"].isin(annualelem))]["PrevAmount"])
        
        grossdiff = grosscurr - grossprev
        grossdiff = round(grossdiff,0)
        
        if abs(grossdiff) > cutoamount:
            
            middf = df[(df["Empid"] == eachemp)&(df["Refdate"] >= prevmonth)]
            
            currate = sum(middf[(middf["Refdate"] == refmonth)&(middf["Elem"] == "90148")]["CurAmount"])
            prevrate = sum(middf[(middf["Refdate"] == prevmonth)&(middf["Elem"] == "90148")]["PrevAmount"])
            prevbase = sum(middf[(middf["Refdate"] == prevmonth)&(middf["Elem"] == "91025")]["PrevAmount"])
            prevbase = prevbase - sum(middf[middf['Elem'].isin(("2151","290"))]["PrevAmount"])

            resdict["Empid"].append(eachemp)
            resdict["Elem"].append("CurrGross")
            resdict["Diff"].append(grossdiff)
            resdict["Values"].append(0)      
            
            resdict["Empid"].append(eachemp)
            resdict["Elem"].append("prevrate")
            resdict["Diff"].append(prevrate)
            resdict["Values"].append(0)

            resdict["Empid"].append(eachemp)
            resdict["Elem"].append("currate")
            resdict["Diff"].append(currate)
            resdict["Values"].append(0)

            if prevrate == 0 and currate != 0:
                rateadd = prevbase
            elif prevrate == 0 and currate == 0: #if there is no rate
                pass
            else:
                rateadd = prevbase * (currate / prevrate - 1)
            #
            
            if abs(rateadd)/abs(grossdiff) >= cutoff:       
                resdict["Empid"].append(eachemp)
                resdict["Elem"].append("91025")
                resdict["Diff"].append(0)
                resdict["Values"].append(round(rateadd,0))
            #
            
            unproratedf = middf[middf["Elem"].isin(unprorate)]
            
            for eachelem in unproratedf['Elem'].unique(): #not prorate
                prevsum = sum(unproratedf[(unproratedf["Elem"] == eachelem)]["PrevAmount"])
                currsum = sum(unproratedf[(unproratedf["Refdate"] == refmonth)&(unproratedf["Elem"] == eachelem)]["CurAmount"])
                if abs(currsum-prevsum)/abs(grossdiff) >= cutoff:
                    resdict["Empid"].append(eachemp)
                    resdict["Elem"].append(eachelem)
                    resdict["Diff"].append(0)
                    resdict["Values"].append(round(currsum-prevsum,0))
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
                
                if abs(diffamount)/abs(grossdiff) >= cutoff:
                    resdict["Empid"].append(eachemp)
                    resdict["Elem"].append(eachelem)
                    resdict["Diff"].append(0)
                    resdict["Values"].append(round(diffamount,0))
                #
            #
            
        #
    #
    resdf = pd.DataFrame.from_dict(resdict)

    resdf.to_excel(xlwriter,sheet_name="currgross_diff",index=False)

    resdf.head(10)

    return len(resdf["Empid"].unique())
#
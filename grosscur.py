#השוואת ברוטו שוטף ללא חד שנתיים
import pandas as pd
import numpy as np
import custom

def grosscur(level="0.2,2000"):
    
    levellist = level.split(",")

    cutoffrate = min([float(eachlevel) for eachlevel in levellist])
    cutoffamount = max([float(eachlevel) for eachlevel in levellist])

    currentemp = [None]

    basedict = dict()
    basedict["Empid"] = []
    basedict["Empname"] = []
    basedict["Elemtype"] = []
    basedict["Elem"] = []
    basedict["Elem_heb"] = []
    basedict["Empid_mn"] = []
    basedict["PrevAmount"] = []
    basedict["CurCur"] = []
    basedict["Diff"] = []
    basedict["Significant"] = []

    middf =  custom.DF101.loc[(custom.DF101["Refdate"] >= custom.PREVMONTH)&((custom.DF101["Elemtype"] == "addition components")|(custom.DF101["Elem_heb"] == custom.dayvalue)|(custom.DF101["Elem"] == custom.semelratio)),["Empname","Empid","Refdate","Elem","Elem_heb","PrevAmount","CurAmount","Empid_mn","Elemtype"]]

    def highdiff(row):
        res = 0
        
        if row["Elem"] not in (custom.annualelement + custom.byreport):
        
            if abs(row['Diff']) >= cutoffamount:
                res = row['Diff']
        
            elif abs(row['Diff']) / abs(highdf.loc[highdf['Empid_mn'] == row['Empid_mn'],'Diff'].item()) >= cutoffrate:
                res = row['Diff']
        
            else:
                res = 0
        #
        
        elif row["Elem"] in custom.byreport:
            prevrate = groupdf.loc[(groupdf['Empid_mn']==row['Empid_mn'])&(groupdf['Elem'] == custom.semelratio),'PrevAmount'].item()
            prevhourval = groupdf.loc[(groupdf['Empid_mn']==row['Empid_mn'])&(groupdf["Elem_heb"] == custom.dayvalue),'PrevAmount'].item()
            
            if prevrate != 0:
                currate = groupdf.loc[(groupdf['Empid_mn']==row['Empid_mn'])&(groupdf['Elem'] == custom.semelratio),'CurCur'].item()   
                updatedamount = 22*prevhourval / prevrate * currate
            else:
                updatedamount = 22*prevhourval
                currate = 0
            #
            
            if abs(row['Diff']-updatedamount) >= cutoffamount:
                res = row['Diff']
        
            elif abs(row['Diff']-updatedamount) / abs(highdf.loc[highdf['Empid_mn'] == row['Empid_mn'],'Diff'].item()) >= cutoffrate:
                res = row['Diff']
        
            else:
                res = 0
            #
        
            if row['Empid_mn'] !=currentemp[0] and res != 0:

                basedict["Empid"] = basedict["Empid"] + [row['Empid']]
                basedict["Empname"] = basedict["Empname"] + [row['Empname']]
                basedict["Elemtype"] = basedict["Elemtype"] + ['additional data']
                basedict["Elem"] = basedict["Elem"] + [0]
                basedict["Elem_heb"] = basedict["Elem_heb"] + ['בסיס פנסיה מחושב']
                basedict["Empid_mn"] = basedict["Empid_mn"] + [row['Empid_mn']]
                basedict["PrevAmount"] = basedict["PrevAmount"] + [22*prevhourval*prevrate]
                basedict["CurCur"] = basedict["CurCur"] + [22*prevhourval*currate]
                basedict["Diff"] = basedict["Diff"] + [22*prevhourval * (currate - prevrate)]
                basedict["Significant"] = basedict["Significant"] + [22*prevhourval * (currate - prevrate)]

                currentemp[0] = row['Empid_mn']
                
            #

        return np.round(res,0)
    #


    middf["CurCur"] = middf.apply(lambda row: row["CurAmount"] if row["Refdate"] == custom.REFMONTH else 0,axis=1)

    groupdf = middf.groupby(by = ["Empid","Empname","Elemtype","Elem", "Elem_heb","Empid_mn"],as_index=False,group_keys=True).sum(['PrevAmount','CurCur'])

    groupdf["Diff"] = groupdf['CurCur'] - groupdf['PrevAmount']

    sumdf = groupdf[groupdf['Elemtype'] == "addition components"].groupby(by = "Empid_mn",as_index=False,group_keys=True).sum('Diff')

    highdf = sumdf.loc[(sumdf['Diff'] >= cutoffamount)|(sumdf['Diff'] <= -cutoffamount)] 

    groupdf = groupdf.loc[groupdf["Empid_mn"].isin(highdf["Empid_mn"].unique())]

    groupdf['Significant'] = groupdf.apply(highdiff, axis=1)

    basedictdf = pd.DataFrame.from_dict(basedict)

    finpd = pd.concat([groupdf,basedictdf], ignore_index = True)

    finpd.sort_values(by=["Empid_mn","Elemtype","Elem"],inplace=True,ignore_index=True)

    jsdict = {}

    for eachindex in finpd["Empid"].unique():
        jsdict[eachindex] = finpd.loc[(finpd['Significant']!= 0)&(finpd['Empid']== eachindex),["Elem_heb","Significant"]].to_dict('records')
    
    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        finpd.loc[finpd['Significant']!= 0].to_excel(writer,sheet_name="currgross_diff")
    #


    return jsdict
#
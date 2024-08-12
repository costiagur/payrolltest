#השוואת ברוטו שוטף ללא חד שנתיים
import pandas as pd
import numpy as np
import custom

def grosscur(empid):    

    middf =  custom.DF101.loc[custom.DF101["Empid"].eq(empid)&(custom.DF101["Refdate"] >= custom.PREVMONTH)&((custom.DF101["Elemtype"] == "addition components")|(custom.DF101["Elem_heb"] == custom.dayvalue)|(custom.DF101["Elem"] == custom.semelratio)),["Empid","Refdate","Elem","Elem_heb","PrevAmount","CurAmount","Empid_mn","Elemtype"]]
    middf["CurAmount"] = middf.apply(lambda row: row["CurAmount"] if row["Refdate"] == custom.REFMONTH else 0,axis=1) #nullify current retro payments
    
    groupdf = middf.groupby(by=["Empid","Elem","Elem_heb","Empid_mn","Elemtype"],as_index=False,group_keys=True).sum(["PrevAmount","CurAmount"])
    
    #calculate pensionbase for each mn

    for each_mn in groupdf["Empid_mn"].unique():
    
        prevrateS = groupdf.loc[(groupdf['Empid_mn']==each_mn)&(groupdf['Elem'] == custom.semelratio),'PrevAmount']
        prevrate = prevrateS.item() if prevrateS.size > 0 else 0
        prevhourvalS = groupdf.loc[(groupdf['Empid_mn']==each_mn)&(groupdf["Elem_heb"] == custom.dayvalue),'PrevAmount']
        prevhourval = prevhourvalS.item() if prevhourvalS.size > 0 else 0
        currateS = groupdf.loc[(groupdf['Empid_mn']==each_mn)&(groupdf['Elem'] == custom.semelratio),'CurAmount']
        currate = currateS.item() if currateS.size > 0 else 0

        basedict = {"Empid": [empid],
                "Elem": [99999],
                "Elem_heb": ['בסיס פנסיה מחושב'],
                "Empid_mn":[each_mn],
                "Elemtype": ['additional data'], 
                "PrevAmount": [22*prevhourval*prevrate],
                "CurAmount": [22*prevhourval*currate]}
                
        basedf = pd.DataFrame.from_dict(basedict) 

        groupdf = pd.concat([groupdf,basedf], ignore_index=True)
    #

    groupdf["Diff"] = groupdf["CurAmount"] - groupdf["PrevAmount"]


    def significant_diff(row):
        res = 0
        
        if row["Elem"] not in (custom.annualelement + custom.byreport + (custom.semelratio, custom.dayvalue)): #סמלים שלא בבסיס הפנסיה ולא שנתיים
            

            if abs(row['Diff']) >= 100:
                res = np.round(row['Diff'],0)
 
        #
        
        elif row["Elem"] in custom.byreport: #סמלים בביס הפנסיה שדורשים דווח של חשב שכר

            prevrateS = groupdf.loc[(groupdf['Empid_mn']==row['Empid_mn'])&(groupdf['Elem'] == custom.semelratio),'PrevAmount']
            prevrate = prevrateS.item() if prevrateS.size > 0 else 0
            prevhourvalS = groupdf.loc[(groupdf['Empid_mn']==row['Empid_mn'])&(groupdf["Elem_heb"] == custom.dayvalue),'PrevAmount']
            prevhourval = prevhourvalS.item() if prevhourvalS.size > 0 else 0
            
            if prevrate != 0:
                currateS = groupdf.loc[(groupdf['Empid_mn']==row['Empid_mn'])&(groupdf['Elem'] == custom.semelratio),'CurAmount']   
                currate = currateS.item() if currateS.size > 0 else 0
                updatedamount = 22*prevhourval / prevrate * currate #hypotetical amount based on chages in position rate
            else:
                updatedamount = 0
            #

            if abs(row['Diff']-updatedamount) >= 100: #if the differences is grater that one that stems from position rate changes, analyze it
                res = np.round(row['Diff'],0)

            #
        
        return res
    #

    groupdf["Currentdiff"] = groupdf.apply(significant_diff,axis=1)

    resdf = 0

    if groupdf.loc[groupdf['Currentdiff']!= 0,["Elem_heb","Currentdiff"]].empty:
        resdict = {"Empid":[empid],"Elem_heb":["0"],"Currentdiff":[0]}
        resdf = pd.DataFrame.from_dict(resdict)
    else:
        resdf = groupdf.loc[groupdf['Currentdiff']!= 0,["Empid","Elem_heb","Currentdiff"]]
    #

    return resdf
#
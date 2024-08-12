    #בדיקת סבירות של ניכוים לקופות

import pandas as pd
import numpy as np
import custom
import statsmodels.formula.api as smf

def fundsprovision(level=""):   

    pd.set_option('display.float_format', lambda x: '%.2f' % x)

    cols = ["Empid","Empname","mn","Startdate","Refdate","Elemtype","Elem","Elem_heb","Rank","CurAmount"]
    prevyear = pd.to_datetime(custom.REFMONTH) + pd.DateOffset(months = -12)

    middf = custom.DF101.loc[(custom.DF101["Division"] != 90)&(custom.DF101["Refdate"]==custom.REFMONTH)&((custom.DF101["Elemtype"].isin(("addition components","provision components"))|(custom.DF101["Elem"]==custom.takzivit))&(~custom.DF101["Elem"].isin(custom.nonpension))&(custom.DF101["CurAmount"]!=0.0)),cols]

    def apply1(row):
        reslist = []
        reslist.append(1 if row["Startdate"] > prevyear and row["Rank"] in custom.edufund_fromsecondyear else 0) #in case of non eligible for edu fund during first year
        reslist.append(1 if row["Elem"]=="30501" else 0)
        reslist.append(row["CurAmount"] if row["Elemtype"] == "provision components" else 0)
        reslist.append(row["CurAmount"] if row["Elemtype"] == "addition components" else 0)
        reslist.append(1 if row["Rank"] in custom.hozeishi else 0)
        reslist.append(row["CurAmount"] if row["Elemtype"] == "addition components" and row["Elem"] in (custom.annualelement+ custom.annualvehicle)  else 0)
   
        return reslist
    #

    middf[["FirstYear","Takzivit","Provision","Addition","HighRank","AnnualElem"]] = middf.apply(apply1,axis=1,result_type='expand')

    groupdf = middf.groupby(by = ["Empid","Empname"],as_index=False,group_keys=True).sum(("Provision","Addition","Takzivit","FirstYear","HighRank","AnnualElem"))

    def apply2(row):

        reslist = []

        reslist.append(1 if row["FirstYear"] > 0 else 0) #FirstYear
        reslist.append(1 if row["Takzivit"] > 0 else 0) #Takzivit
        reslist.append(1 if row["HighRank"] > 0 else 0) #HighRank
        
        return reslist
    #

    groupdf[["FirstYear","Takzivit","HighRank"]] = groupdf.apply(apply2,axis=1,result_type='expand')

    model = smf.ols(formula="Provision ~ Addition + AnnualElem + FirstYear*Addition + Takzivit*Addition + HighRank*Addition",data=groupdf,missing='drop').fit()
    print(model.summary())
    
    groupdf["Yhat"] = model.predict()
    groupdf["Residual"] = model.resid
    
    groupdf["Yhatrate"] = groupdf.apply(lambda row: (row["Yhat"]/row["Addition"]) if row["Addition"] != 0 else row["Yhat"],axis=1)
    groupdf["Provisionrate"] =groupdf.apply(lambda row: (row["Provision"]/row["Addition"]) if row["Addition"] != 0 else row["Provision"],axis=1) 

    hists,bins = np.histogram(groupdf["Residual"],100)

    leng = abs(bins[1] - bins[0])

    groupdf["Hist"] = hists[np.floor((groupdf["Residual"] - bins[0])/leng).astype(int)]

    resdf = groupdf.loc[groupdf["Hist"] <= 10,["Empid","Empname","Addition","Provision","Provisionrate","Yhat","Yhatrate"]]

    resdf.rename(columns={"Empid":"מספר עובד","Empname":"שם","Addition":"תוספות","Provision":"הפרשה","Provisionrate":"שעור הפרשה","Yhat":"אומדן רוחבי","Yhatrate":"שעור אומדן"},inplace=True)

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer,sheet_name="שיעור הפרשה לקופות",index=False)
    #  

    return len(resdf["מספר עובד"].unique())
#

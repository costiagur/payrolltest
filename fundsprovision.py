    #בדיקת סבירות של ניכוים לקופות

import pandas as pd
import numpy as np
import custom
import statsmodels.formula.api as smf

def fundsprovision(level=""):   
    
    cols = ["Empid","Empname","mn","Startdate","Refdate","Elemtype","Elem","Elem_heb","Rank","CurAmount"]
    prevyear = pd.to_datetime(custom.REFMONTH) + pd.DateOffset(months = -12)

    middf = custom.DF101.loc[(custom.DF101["Division"] != 90)&(custom.DF101["Refdate"]==custom.REFMONTH)&((custom.DF101["Elemtype"].isin(("addition components","provision components"))|(custom.DF101["Elem"]==custom.takzivit))&(~custom.DF101["Elem"].isin(custom.nonpension))&(custom.DF101["CurAmount"]!=0.0)),cols]
    middf["FirstYear"] = middf.apply(lambda row: 1 if row["Startdate"] > prevyear and row["Rank"] in custom.edufund_fromsecondyear else 0,axis=1) #in case of non eligible for edu fund during first year
    middf["Takzivit"] = middf.apply(lambda row: 1 if row["Elem"]=="30501" else 0,axis=1)
    middf["Provision"] = middf.apply(lambda row: row["CurAmount"] if row["Elemtype"] == "provision components" else 0,axis=1)
    middf["Addition"] = middf.apply(lambda row: row["CurAmount"] if row["Elemtype"] == "addition components" else 0,axis=1)
    middf["HighRank"] = middf.apply(lambda row: 1 if row["Rank"] in custom.hozeishi else 0,axis=1)

    groupdf = middf.groupby(by = ["Empid","Empname"],as_index=False,group_keys=True).sum(("Provision","Addition","Takzivit","FirstYear","HighRank"))
    groupdf["FirstYear"] = groupdf.apply(lambda row: 1 if row["FirstYear"] > 0 else 0,axis=1)
    groupdf["Takzivit"] = groupdf.apply(lambda row: 1 if row["Takzivit"] > 0 else 0,axis=1)
    groupdf["HighRank"] = groupdf.apply(lambda row: 1 if row["HighRank"] > 0 else 0,axis=1)
    
    groupdf["Addition100"] = groupdf["Addition"]/500
    groupdf["Provision100"] = groupdf["Provision"] /500   
    groupdf["AdditionXTakzivit"] = groupdf["Addition100"]*groupdf["Takzivit"] 
    groupdf["AdditionXHighRank"] = groupdf["Addition100"]*groupdf["HighRank"]
    groupdf["AdditionXHFirstYear"] = groupdf["Addition100"]*groupdf["FirstYear"]

    model = smf.ols(formula="Provision100 ~ Addition100 + AdditionXTakzivit + FirstYear + AdditionXHighRank",data=groupdf,missing='drop').fit()

    ssdresid = np.sqrt(model.mse_resid)

    def yhat(row):
        return model.params.Intercept + model.params.Addition100*row["Addition100"] + model.params.AdditionXTakzivit*row["AdditionXTakzivit"]+ model.params.FirstYear*row["FirstYear"] + model.params.AdditionXHighRank*row["AdditionXHighRank"]
    
    groupdf["Yhat"] = groupdf.apply(yhat,axis=1)
    

    def exceeds(row):       
        ttest = (row["Provision100"] - row["Yhat"])/ssdresid
        res = True if ttest >= 2 or ttest <= -2 else False
        
        return res
    #
    
    groupdf["Yhatrate"] = groupdf.apply(lambda row: (row["Yhat"]/row["Addition100"]) if row["Addition100"] != 0 else row["Yhat"],axis=1)
    groupdf["Provisionrate"] =groupdf.apply(lambda row: (row["Provision100"]/row["Addition100"]) if row["Addition100"] != 0 else row["Provision100"],axis=1) 
    groupdf["Exceeds"] = groupdf.apply(exceeds,axis=1)
    
    print(model.summary())    

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        groupdf.loc[groupdf["Exceeds"] == True,["Empid","Empname","Addition","Takzivit","FirstYear","Provision","Provisionrate","Yhat","Yhatrate"]].to_excel(writer,sheet_name="FundsProvisionRate",index=False)
    #  

    return len(groupdf.loc[groupdf["Exceeds"] == True,"Empid"].unique())
#

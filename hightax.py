#מס הכנסה גבוה
import numpy as np
import pandas as pd
import custom
import statsmodels.formula.api as smf


def hightax(level = ""):
 
    middf = custom.DF101.loc[custom.DF101["Elemtype"].isin(["addition components","benefit charge components","compulsory deductions"]),["Empname","Empid","Division","Elemtype","Elem_heb","Elem","PrevAmount","CurAmount","Rank"]]

    middf["btlPrev"] = middf.apply(lambda row: row["PrevAmount"] if row["Elem"] in custom.elembtl else 0, axis=1)
    middf["btlCur"] = middf.apply(lambda row: row["CurAmount"] if row["Elem"] in custom.elembtl else 0, axis=1)
    middf["taxPrev"] = middf.apply(lambda row: row["PrevAmount"] if row["Elem"] == custom.elemtax else 0, axis=1)
    middf["taxCur"] = middf.apply(lambda row: row["CurAmount"] if row["Elem"] == custom.elemtax else 0, axis=1) 
    middf.loc[middf["Elemtype"] == "compulsory deductions",["CurAmount","PrevAmount"]] = 0
    middf["mostfemale"] = middf.apply(lambda row: 1 if row["Rank"]  == custom.sayaot else 0, axis=1)
    middf["pension"] = middf.apply(lambda row: 1 if row["Division"]==custom.pensiondepartment else 0, axis=1)
    middf["CurPizuim"] = middf.apply(lambda row: row["CurAmount"]/1000 if row["Elem"] in custom.pizuim else 0, axis=1)

    groupdf = middf.groupby(by = ["Empname","Empid","Division"],as_index=False,group_keys=True).sum(["CurAmount","CurPizuim","PrevAmount","btlCur","btlPrev","taxCur","taxPrev","mostfemale","pension"])
    
    groupdf["btlrateCur"] = groupdf.apply(lambda row: row["btlCur"] / row["CurAmount"] if row["CurAmount"] != 0 else np.nan,axis=1)
    groupdf["taxratePrev"] = groupdf.apply(lambda row: row["taxPrev"] / row["PrevAmount"] if row["PrevAmount"] != 0 else np.nan,axis=1)
    groupdf["taxrateCur"] = groupdf.apply(lambda row: row["taxCur"] / row["CurAmount"] if row["CurAmount"] != 0 else np.nan,axis=1)
    groupdf["CurAm1"] = groupdf.apply(lambda row: row["CurAmount"]/1000, axis=1)
    groupdf["mostfemale"] = groupdf.apply(lambda row: 1 if row["mostfemale"] >0 else 0, axis=1)
    groupdf["pension"] = groupdf.apply(lambda row: 1 if row["pension"] >0 else 0, axis=1)
    groupdf["CurAm2"] = groupdf.apply(lambda row: np.power(row["CurAm1"],2) ,axis=1)
    groupdf["DeductCur"] = groupdf.apply(lambda row: (row["taxCur"]+row["btlCur"])/10 if row["taxCur"]+row["btlCur"] > 0 else 0,axis=1)
    groupdf["PensionXCurAm1"] = groupdf["CurAm1"]*groupdf["pension"]
    groupdf["femaleXCurAm1"] = groupdf["CurAm1"]*groupdf["mostfemale"]
    groupdf["CurPizuim2"] = groupdf.apply(lambda row: np.power(row["CurPizuim"],2) ,axis=1)

    
    model = smf.ols(formula="DeductCur ~ CurAm2 + CurAm1 + pension + PensionXCurAm1 + femaleXCurAm1+ CurPizuim + CurPizuim2",data=groupdf,missing='drop').fit()
    ssdresid = np.sqrt(model.mse_resid)

    print(model.summary())

    groupdf["Yhat"] = groupdf.apply(lambda row:model.params.Intercept + model.params.CurAm2*row["CurAm2"] + model.params.CurAm1*row["CurAm1"]+model.params.pension*row["pension"]+model.params.PensionXCurAm1*row["PensionXCurAm1"]+model.params.femaleXCurAm1*row["femaleXCurAm1"],axis=1)


    def tests(row):
        res = []
        ttest = (row["DeductCur"] - row["Yhat"])/ssdresid

        if (ttest >= 2 or ttest <= -2) and row["CurAmount"] != 0 and row["DeductCur"] != 0:
            res.append("סכומי מס וביטוח לאומי חורגים מממוצע")               
        #
        
        if 0 < row["btlrateCur"] < 0.034 and row["Division"] != custom.pensiondepartment: #מהותיות 0.01
            res.append("שיעור ביטוח לאומי נמוך ממזערי")
        #
        
        if row["taxrateCur"] > 0.4:
            res.append("שיעור מס גבוה")
        #
        
        if row["taxCur"] < -10 and row["taxPrev"] < -10:
            res.append("מס שלילי חודשיים ברציפות")
        #
        
        return ". ".join(res)
    #
    
    groupdf["ErrorDescr"] = groupdf.apply(tests,axis=1)

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        groupdf.loc[groupdf["ErrorDescr"] != "",["Empname","Empid","Division","CurAmount","PrevAmount","btlCur","btlPrev","taxCur","taxPrev","btlrateCur","taxratePrev","taxrateCur","DeductCur","Yhat","ErrorDescr"]].to_excel(writer,sheet_name="hightax",index=False)
    #  
    
    return len(groupdf.loc[groupdf["ErrorDescr"] != "","Empid"].unique())
#
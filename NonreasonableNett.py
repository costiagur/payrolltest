import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import custom

def NonreasonableNett(level = ""):

    cols = ["Empname","Empid","Rank","Elem","CurAmount","Elemtype"]
    middf = custom.DF101.loc[(custom.DF101["Division"] != custom.pensiondepartment)&(custom.DF101["Refdate"] == custom.REFMONTH)&((custom.DF101["Elemtype"] == "addition components")|(custom.DF101["Elem"]==custom.semelnett)),cols]
    middf["Nett"] = middf.apply(lambda row: row["CurAmount"] if row["Elem"] == custom.semelnett else 0, axis=1)
    middf["Meshulav"] = middf.apply(lambda row: row["CurAmount"] if row["Elem"] in custom.meshulav else 0, axis=1)
    middf["Hourdeduct"] = middf.apply(lambda row: row["CurAmount"] if row["Elem"]==custom.hourdeduct else 0, axis=1)
    middf["Gross"] = middf.apply(lambda row: row["CurAmount"] if row["Elemtype"]=="addition components" else 0, axis=1)
    middf["Veh"] = middf.apply(lambda row: row["CurAmount"] if row["Elem"] in ((custom.lics + custom.instotal)) else 0, axis=1)
    middf["Pizuim"] = middf.apply(lambda row: row["CurAmount"] if row["Elem"] in ((custom.pizuim + custom.HodaaMukdemetHayavBL)) else 0, axis=1)
    middf["Miluim"] = middf.apply(lambda row: row["CurAmount"] if row["Elem"] in (custom.miluim) else 0, axis=1)
    
    newdf = pd.DataFrame()

    for eachrank in custom.ranksforresonablecheck:
        groupdf = middf.loc[middf["Rank"] == eachrank,["Empname","Empid","Rank","Nett","Meshulav","Gross","Hourdeduct","Veh","Pizuim","Miluim"]].groupby(by = ["Empid","Empname","Rank"],as_index=False,group_keys=True).sum(("Miluim","Nett","Meshulav","Gross","Hourdeduct","Veh","Pizuim"))

        #modelGross = smf.ols(formula="Gross ~ Meshulav + Hourdeduct + Veh + Pizuim + Miluim",data=groupdf,missing='drop').fit()
        modelNett = smf.ols(formula="Nett ~ Meshulav + Hourdeduct + Veh + Pizuim + Miluim",data=groupdf,missing='drop').fit()
        ssdresid = np.sqrt(modelNett.mse_resid)
        print(modelNett.summary())

        #plt.scatter(groupdf["Nett"],modelNett.predict()-groupdf["Nett"])
        #plt.show()
        groupdf["Yhat"] = modelNett.predict()
        groupdf["Resid"] = groupdf["Nett"] - groupdf["Yhat"]
        #plt.hist(groupdf["Resid"],bins=500)
        #plt.show()
        groupdf["Ztest"] = groupdf.apply(lambda row:(row["Nett"]-row["Yhat"])/ssdresid,axis=1)
        newdf = pd.concat([newdf,groupdf.loc[abs(groupdf["Ztest"])>2]])
        
    #
    
    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        newdf.to_excel(writer,sheet_name="NonReasonableNett",index=False)
    #

    return len(newdf["Empid"].unique())
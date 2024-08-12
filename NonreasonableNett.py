import numpy as np
import pandas as pd
import statsmodels.api as sm
import custom

def NonreasonableNett(level = ""):

    pd.set_option('display.float_format', lambda x: '%.2f' % x)

    cols = ["Empname","Empid","Rank","Elem","CurAmount","Elemtype"]
    middf = custom.DF101.loc[(custom.DF101["Division"] != custom.pensiondepartment)&(custom.DF101["Elemtype"].isin(["addition components","compulsory deductions","voluntary deductions"])),cols]
    
    def calccols(row):
        reslist = []
        reslist.append(row["CurAmount"] if row["Elemtype"] == "addition components" else -row["CurAmount"])
        reslist.append(row["CurAmount"] if row["Elem"] in custom.meshulav else 0)
        reslist.append(row["CurAmount"] if row["Elem"]==custom.hourdeduct else 0)
        reslist.append(row["CurAmount"] if row["Elemtype"]=="addition components" else 0)
        reslist.append(row["CurAmount"] if row["Elem"] in ((custom.lics + custom.instotal)) else 0)
        reslist.append(row["CurAmount"] if row["Elem"] in ((custom.pizuim + custom.HodaaMukdemetHayavBL)) else 0)
        reslist.append(row["CurAmount"] if row["Elem"] in (custom.miluim) else 0)
        reslist.append(row["CurAmount"] if row["Elem"] in (custom.annualelement) else 0)
        reslist.append(row["CurAmount"] if row["Elem"] in (custom.vacationadds) else 0)

        return reslist
    #
    
    middf[["Nett","Meshulav","Hourdeduct","Gross","Veh","Pizuim","Miluim","Annual","Vacation"]] = middf.apply(calccols,axis=1,result_type='expand')
        
    groupdf = middf[["Empname","Empid","Rank","Nett","Meshulav","Gross","Hourdeduct","Veh","Pizuim","Miluim","Annual","Vacation"]].groupby(by = ["Empid","Empname","Rank"],as_index=False,group_keys=True).sum(("Miluim","Nett","Meshulav","Gross","Hourdeduct","Veh","Pizuim","Annual","Vacation"))

    newdf = pd.get_dummies(data=groupdf,columns=["Rank"],drop_first=False,dtype=float)

    newdf.set_index(["Empid","Empname"],inplace=True)
    Y = newdf["Nett"]
    X = newdf.drop(columns=["Nett"])
    X = sm.add_constant(X)

    modelNett = sm.OLS(Y,X,missing='drop').fit()

    print(modelNett.summary())

    groupdf["Yhat"] = modelNett.predict()

    groupdf["Residual"] = groupdf["Nett"] - groupdf["Yhat"]

    hists,bins = np.histogram(groupdf["Residual"],100)

    leng = abs(bins[1] - bins[0])

    groupdf["Hist"] = hists[np.floor((groupdf["Residual"] - bins[0])/leng).astype(int)]
    
    groupdf.rename(columns={"Empid":"מספר_עובד","Empname":"שם","Rank":"דירוג","Nett":"נטו","Meshulav":"משולב","Gross":"ברוטו","Hourdeduct":"הפחתת שעות","Veh":"רשיון וביטוח רכב","Pizuim":"פיצויים","Miluim":"מילואים","Annual":"תשלום שנתי","Vacation":"עבודה בחופשות","Yhat":"אומדן נטו","Residual":"הפרש מול אומדן","Hist":"מספר מקרים דומים"},inplace=True)

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        groupdf.loc[groupdf["מספר מקרים דומים"] < 10].to_excel(writer,sheet_name="נטו לא סביר",index=False) #5%
    #

    return groupdf.loc[groupdf["מספר מקרים דומים"] < 10,"הפרש מול אומדן"].shape[0]
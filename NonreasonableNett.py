import numpy as np
import pandas as pd
import statsmodels.api as sm
import custom
import inspect
import sqlite3

def NonreasonableNett(level = ""):

    pd.set_option('display.float_format', lambda x: '%.2f' % x)

    conn = sqlite3.connect("dbsave.db")
    cur = conn.cursor()

    query = f"SELECT Empid,Empname,Elemtype,Amount,Elem,Rank FROM dfcurr WHERE Division <> 90 AND Elemtype IN ('addition components','compulsory deductions','voluntary deductions')"

    middf = pd.read_sql_query(query, conn)

    conn.close()

    #cols = ["Empname","Empid","Rank","Elem","Amount","Elemtype"]
    #middf = custom.DFCURR.loc[(custom.DFCURR["Division"] != custom.pensiondepartment)&(custom.DFCURR["Elemtype"].isin(["addition components","compulsory deductions","voluntary deductions"])),cols]
    
    def calccols(row):
        reslist = []
        reslist.append(row["Amount"] if row["Elemtype"] == "addition components" else -row["Amount"])
        reslist.append(row["Amount"] if row["Elem"] in custom.meshulav else 0)
        #reslist.append(row["Amount"] if row["Elem"]==custom.hourdeduct else 0)
        reslist.append(row["Amount"] if row["Elemtype"]=="addition components" else 0)
        #reslist.append(row["Amount"] if row["Elem"] in custom.annualvehicle else 0)
        reslist.append(row["Amount"] if row["Elem"] in (custom.pizuim + custom.HodaaMukdemetHayavBL+("257",)) else 0)
        #reslist.append(row["Amount"] if row["Elem"] in (custom.miluim) else 0)
        #reslist.append(row["Amount"] if row["Elem"] in (custom.annualelement) else 0)
        #reslist.append(row["Amount"] if row["Elem"] in (custom.vacationadds) else 0)

        return reslist
    #
    
    middf[["Nett","Meshulav","Gross","Pizuim"]] = middf.apply(calccols,axis=1,result_type='expand')
        #,"Hourdeduct","Miluim","Annual","Vacation","Veh"
    groupdf = middf[["Empname","Empid","Rank","Nett","Meshulav","Gross","Pizuim"]].groupby(by = ["Empid","Empname","Rank"],as_index=False,group_keys=True).sum(("Nett","Meshulav","Gross","Pizuim")) 

    #"Hourdeduct","Veh","Miluim","Annual","Vacation"

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

    groupdf["Hist"] = groupdf.apply(lambda row:hists[min(np.floor((row["Residual"] - bins[0])/leng).astype(int),99)],axis=1)
    
    groupdf.rename(columns={"Empid":"מספר_עובד","Empname":"שם","Rank":"דירוג","Nett":"נטו","Meshulav":"משולב","Gross":"ברוטו","Pizuim":"פיצויים","Yhat":"אומדן נטו","Residual":"הפרש מול אומדן","Hist":"מספר מקרים דומים"},inplace=True)
    #"Hourdeduct":"הפחתת שעות","Veh":"רשיון וביטוח רכב","Miluim":"מילואים","Annual":"תשלום שנתי","Vacation":"עבודה בחופשות"

    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        groupdf.loc[groupdf["מספר מקרים דומים"] < 10].to_excel(writer,sheet_name="נטו לא סביר",index=False) #5%
    #

    return [inspect.stack()[0][3],groupdf.loc[groupdf["מספר מקרים דומים"] < 10,"הפרש מול אומדן"].shape[0],"סכומי נטו לא סבירים ביחס רוחבי"]
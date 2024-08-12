    #הפרשי ברוטו ברטרו
import numpy as np
import custom
import pandas as pd

def grossretro(empid,cutoffrate,cutoffamount):

    groupdf = custom.DF101.loc[custom.DF101["Empid"].eq(empid)&(custom.DF101["Elemtype"] == "addition components")&(custom.DF101["Refdate"] < custom.REFMONTH)].groupby(by = ["Empid","Elem_heb","Elem","Refdate"],as_index=False,group_keys=True).sum("CurAmount")
       
    groupdf["Retrodiff"] = groupdf.apply(lambda row: np.round(row["CurAmount"],0) if abs(row["CurAmount"]) >= abs(cutoffrate*groupdf['CurAmount'].sum()) or abs(row["CurAmount"]) >= cutoffamount/4 else 0 ,axis=1)

    return groupdf.loc[groupdf['Retrodiff']!= 0,["Empid","Elem_heb","Retrodiff"]]
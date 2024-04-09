#בדיקה אם יש הפרשות עם רטרו מעל 9 חודשים

import pandas as pd
import custom

def before9months(level=""):
    
    middf = custom.DF101[(custom.DF101['Elemtype'].isin(("provision components","voluntary deductions")))&(custom.DF101['Elem'].str.contains(r'3\d{5}',regex=True))&(custom.DF101["CurAmount"]<0)&(custom.DF101["Refdate"] < (pd.to_datetime(custom.REFMONTH) + pd.DateOffset(months = -9)))]

    resdict = dict()
    resdict["Empid"] = []
    resdict["Empname"] = []
    resdict["Fund"] = []
    resdict["Date"] = []
    resdict["Values"] = []

    for eachid in middf["Empid"].unique():
        
        num = middf.loc[middf["Empid"] == eachid,"Elem"].count()
        
        resdict["Empid"] = resdict["Empid"] + [eachid]*num
        resdict["Empname"] = resdict["Empname"] + [middf.loc[middf["Empid"] == eachid,"Empname"].unique()[0]]*num

        resdict["Fund"] = resdict["Fund"] + middf.loc[middf["Empid"] == eachid,"Elem_heb"].to_list()
        resdict["Date"] = resdict["Date"] + middf.loc[middf["Empid"] == eachid,"Refdate"].to_list()
        resdict["Values"] = resdict["Values"] + middf.loc[middf["Empid"] == eachid,"CurAmount"].to_list()
    #
    
    resdf = pd.DataFrame.from_dict(resdict)
    
    with pd.ExcelWriter(custom.xlresfile, mode="a") as writer:
        resdf.to_excel(writer,sheet_name="Kupot_9_months",index=False)
    #      

    return len(resdf["Empid"].unique())
#
#בדיקה אם יש הפרשות עם רטרו מעל 9 חודשים

import pandas as pd
from datetime import timedelta

def before9months(df,xlwriter,refmonth,prevmonth,level=""):
    
    middf = df[(df['Elemtype'].isin(("provision components","voluntary deductions")))&(df['Elem'].str.contains(r'3\d{5}',regex=True))&(df["CurAmount"]<0)&(df["Refdate"] < (refmonth-timedelta(weeks=38)))]

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
    resdf.to_excel(xlwriter,sheet_name="Kupot_9_months",index=False)

    resdf.head(10)

    return len(resdf["Empid"].unique())
#
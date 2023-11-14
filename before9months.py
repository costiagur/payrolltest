#בדיקה אם יש הפרשות עם רטרו מעל 9 חודשים

import pandas as pd
from datetime import timedelta

def before9months(df,xlwriter,refmonth,prevmonth,level=""):
    
    middf = df[(df['Elemtype'].isin(("provision components","voluntary deductions")))&(df['Elem'].str.contains(r'3\d{5}',regex=True))&(df["CurAmount"]<0)&(df["Refdate"] < (refmonth-timedelta(weeks=38)))]

    
    resdf = pd.DataFrame.from_dict(newdict)
    resdf.to_excel(xlwriter,sheet_name="Kupotrate",index=False)

    resdf.head(10)

    return len(resdf["Empid"].unique())
#
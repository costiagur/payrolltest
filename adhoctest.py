import pandas as pd
import numpy as np
import custom
from datetime import date
from io import BytesIO


def adhoctest (semel,reqtype,pensionin=0):

    custom.DFCURR = pd.read_pickle('drafts/dfcurr.pkl')
    custom.DFHOURS = pd.read_pickle('drafts/dfhours.pkl')
    custom.REFMONTH = custom.DFCURR["Refdate"].max()
    #custom.PREVMONTH = pd.to_datetime(custom.REFMONTH) + pd.DateOffset(months = -1)
    #prevyear = pd.to_datetime(custom.REFMONTH) + pd.DateOffset(months = -12)
    pd.set_option('display.float_format', lambda x: '%.2f' % x)

    cols = ["Empid","Empname","mn","Startdate","Refdate","Elemtype","Elem","Elem_heb","Rank","Amount","Division"]
    

    #reqtype = "חריגים" or < > == to some value
    #semel = any semel number as text

    middf = custom.DFCURR.loc[custom.DFCURR["Elem"]==semel,cols] if pensionin == 1 else custom.DFCURR.loc[(custom.DFCURR["Elem"]==semel)&(custom.DFCURR["Division"]!= custom.pensiondepartment),cols]
    groupdf = middf.groupby(by=["Empid","Empname","mn","Division"],as_index=False,group_keys=True).sum("Amount")

    if reqtype == "חריגים":
        hists,bins = np.histogram(groupdf["Amount"],100)
        leng = abs(bins[1] - bins[0])
        groupdf["Hist"] = groupdf.apply(lambda row: hists[min(np.floor((row["Amount"]-bins[0])/leng).astype(int),99)],axis=1)
        groupdf.sort_values(by='Hist',inplace=True)
        groupdf['rolling']=groupdf["Hist"].cumsum()
        resdf = groupdf.loc[(groupdf["Hist"] <= 2)&((groupdf['rolling'] < 0.05*groupdf.shape[0])|(groupdf['rolling'] > 0.95*groupdf.shape[0]))]
        resdf.drop(labels=["Hist","rolling"], axis=1,inplace=True)

    else:
        resdf = groupdf.query('Amount' + reqtype)
    #

    adhocfile = BytesIO()

    with pd.ExcelWriter(adhocfile, mode="w") as writer:
        resdf.to_excel(writer,sheet_name=semel,index=False)
    #  

    return adhocfile
#

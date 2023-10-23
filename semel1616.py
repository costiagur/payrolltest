
#תשלום נסיעות ללא סמל 1 או סמל 100

def semel1616(df,xlwriter,refmonth,prevmonth,level="0"):

    middf = df[df["Elem"].isin(['1','100','1616'])&(df["CurAmount"]>0)&(df["Refdate"] == refmonth)]
    resid = []

    for eachid in list(middf["Empid"]):
        eachlist = middf[middf["Empid"] == eachid]['Elem'].values
        
        if ('1616' in eachlist) and ('1' not in eachlist and '100' not in eachlist):
            resid.append(eachid)
        #
    #

    resdf = middf[middf["Empid"].isin(set(resid))]
    resdf.to_excel(xlwriter,sheet_name="1616_no_work",index=False)
    
    return len(resdf)
#
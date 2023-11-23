
#תשלום נסיעות ללא סמל 1 או סמל 100

def semel1616(df,xlwriter,refmonth,prevmonth,level="0"):

    middf = df[(df["Elem"]=='1616')&(df["CurAmount"]>0)&(df["Refdate"] == refmonth)]
    resid = []

    for eachid in middf["Empid"].unique():
        eachsum = df.loc[(df["Empid"] == eachid)&(df['Elem'].isin(['1','100']))&(df["CurAmount"]>0)&(df["Refdate"] == refmonth),"CurAmount"].sum()
        eachquant = df.loc[(df["Empid"] == eachid)&(df['Elem'].isin(['1','100']))&(df["CurQuantity"]>0)&(df["Refdate"] == refmonth),"CurQuantity"].sum()
    
        if eachsum == 0 or eachquant==0:
            resid.append(eachid)
        #
    #

    resdf = df[(df["Empid"].isin(set(resid)))&(df["Elem"].isin(('1','100','1616')))][["Empid","Empname","mn","Elem_heb","CurAmount","CurQuantity"]]
    resdf.to_excel(xlwriter,sheet_name="1616_no_work",index=False)
    
    return len(resdf)
#
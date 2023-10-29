#יש סמל 1313 אך אין תשלום סמל 1

def semel1313(df,df1313,xlwriter,refmonth,prevmonth,level="8.5"):
    
    middf1313 = df1313.loc[df1313["Quantity"] > 0,["Empid","mn"]]
    resid = []

    level = float(level)

    for _,i1,i2 in list(middf1313.to_records()):
        if df.loc[(df["Empid"] ==i1)&(df["mn"] ==i2)&(df["Elem"] == "1")&(df["Refdate"] == refmonth),"CurAmount"].sum()<= level:
            resid.append(i1)
    #

    resdf = df[(df["Empid"].isin(set(resid)))&(df["Elemtype"]=="addition components")]
    resdf.to_excel(xlwriter,sheet_name="1313_no_1",index=False)
    
    return len(resid)


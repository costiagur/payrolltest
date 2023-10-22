#חלקיות משרה מעל 100%

def semel90148(df,xlwriter,refmonth,prevmonth):

    resdf = df[(df["Elem"] == "90148")&(df["Refdate"] == refmonth)&(df["CurAmount"]>1.1)]
       
    resdf.to_excel(xlwriter,sheet_name="90148_above_1.1",index=False)

    resdf.head(10)

    return len(resdf)

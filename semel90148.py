#חלקיות משרה מעל 100%

def semel90148(df,xlwriter,refmonth,prevmonth,level="1.1"):

    level = float(level)

    resdf = df[(df["Elem"] == "90148")&(df["Refdate"] == refmonth)&(df["CurAmount"]>level)][["Empid","Empname","mn","Elem_heb","CurAmount"]]
       
    resdf.to_excel(xlwriter,sheet_name="90148",index=False)

    resdf.head(10)

    return len(resdf)

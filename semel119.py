#הפחתות שעות גדולות.

def semel119(df,xlwriter,refmonth,prevmonth,level="100"):

    level = float(level)
    
    middf = df[(df["Refdate"] == refmonth)&((df["Elem"] == "119")&(df["CurQuantity"] > level))][["Empid","Empname","mn","Elem_heb","CurQuantity"]]
    
    middf.to_excel(xlwriter,sheet_name="large_119",index=False)

    middf.head(10)

    return len(middf)
#
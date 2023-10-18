#הפחתות שעות גדולות.

def semel119(df,xlwriter,refmonth,prevmonth):

    middf = df[(df["Refdate"] == refmonth)&((df["Elem"] == "119")&(df["CurQuantity"] > 100))]
    middf.to_excel(xlwriter,sheet_name="large_119",index=False)

    middf.head(10)

    return len(middf)
#
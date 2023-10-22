#6666 ו 6667 שווים


def semel6666(df,xlwriter,refmonth,prevmonth):

    middf = df[(df["Refdate"] == refmonth)&(df["Elem"].isin(("6666","6667")))]
    if sum(middf["CurAmount"]) != 0:
        middf.to_excel(xlwriter,sheet_name="6666_6667",index=False)
    #

    middf.head(10)
    
    return len(middf)
# 
#הזינו סכום במקום כמות בסמל 100


def semel100(df,xlwriter,refmonth,prevmonth):
    middf = df[(df["Refdate"] == refmonth)&((df["Elem"] == "100")&(df["CurQuantity"] > 178))]
    middf.to_excel(xlwriter,sheet_name="100_above_182",index=False)

    middf.head(10)

    return len(middf)
#
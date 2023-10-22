#כוננות בחוזה אישי

def semel65(df,xlwriter,refmonth,prevmonth):  
    middf = df[(df["Refdate"] == refmonth)&(df["Rank"].isin((185,186,44,273,515,523,524,551,587,987)))&((df["Elem"] == "65")&(df["CurQuantity"] > 0))]
    middf.to_excel(xlwriter,sheet_name="65_hozeishi",index=False)

    middf.head(10)

    return len(middf)
#ברוטו ביטוח לאומי מעל התקרה

def semel94010(df,xlwriter,refmonth,prevmonth,level="47465"):

    level = float(level)

    resdf = df[(df["Division"] != 90)&(df["Elem"] =="94010")&(df["Refdate"] == refmonth)&(df["CurAmount"] > level)][["Empid","Empname","mn","Elem_heb","CurQuantity"]]

    resdf.to_excel(xlwriter,sheet_name="highgrossbtl",index=False)
    
    return len(resdf["Empid"].unique())
#

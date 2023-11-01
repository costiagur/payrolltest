#סמל שמופיע מספר פעמים באותו תאריך ערך

def semeltwice(df,xlwriter,refmonth,prevmonth,level="1"):
    level = int(level)

    middf = df[df["CurAmount"] != 0]
    grouped = middf.groupby(by=["Empid","mn","Refdate","Elem"],as_index=False,group_keys=True)
    groupdf = grouped["CurAmount"].count()
    resdf = groupdf[groupdf["CurAmount"] > level]
    resdf.rename(columns={"CurAmount":"Count"}, inplace=True)
    
    resdf.to_excel(xlwriter,sheet_name="semeltwice",index=False)
    
    return len(resdf["Empid"].unique())
#
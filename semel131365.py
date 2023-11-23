#עובדים עם מספר שעות רב מדי
def semel131365(df,xlwriter,refmonth,prevmonth,level="264"):
    
    level= float(level)
    
    middf = df[(df['Elem'].isin(("1","65")))&(df["Division"]!=90)&(df["Refdate"]==refmonth)]

    emplist = []

    for eachemp in middf["Empid"].unique():

        if (middf.loc[(middf["Elem"]=="1")&(middf["Empid"]==eachemp),"CurQuantity"].sum() - middf.loc[(middf["Elem"]=="65")&(middf["Empid"]==eachemp),"CurQuantity"].sum()) > 264:
            emplist.append(eachemp)
        #
    #
    
    resdf = middf[(middf["Empid"].isin(emplist))&(middf["Elem"].isin(("1","65")))][["Empid","Empname","mn","Elem_heb","CurQuantity"]]
    resdf.to_excel(xlwriter,sheet_name="manyhours",index=False)
    
    return len(emplist)
#
#סמלים שמופיעים פעם אחת

def semelonce(df,xlwriter,refmonth,prevmonth):

    middf = df[df["Division"] != 90]["Elem"].value_counts()

    reslist = []
    for i in range(0,len((middf).index),1):
        if middf.values[i] == 1:
            reslist.append(middf.index[i])
        #
    #
    resdf = df[(df["Division"] != 90)&(df["Elem"].isin(reslist))]

    resdf.head(10)

    resdf.to_excel(xlwriter,sheet_name="semel_once",index=False)

    return len(resdf)

#
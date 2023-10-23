#סמלים שמופיעים פעם אחת
import pandas as pd
import numpy as np

def semelonce(df,xlwriter,refmonth,prevmonth,level="0"):

    middf = df[(df["Division"] != 90)&(df["Refdate"]==refmonth)&(df["CurAmount"] != 0)&(df["Elemtype"] == "addition components")]

    ranklist = middf["Rank"].unique()

    newdict= dict()
    newdict["Empid"] = []
    newdict["mn"] = []
    newdict["Rank"] = []
    newdict["Elem"] = []
    newdict["CurAmount"] = []

    for eachrank in ranklist:
            rankdf = middf[middf["Rank"] == eachrank]
            empnum = len(rankdf["Empid"].unique())
            elemdf = rankdf["Elem"].value_counts()      
            
            for eachelem in elemdf.index:
                elemcount = elemdf[eachelem]

                if elemcount/empnum < 0.95 and elemcount/empnum > 0.05:
                    pass
                elif elemcount/empnum <= 0.03:
                    newdict["Empid"] = newdict["Empid"] + list(rankdf[rankdf["Elem"] == eachelem]["Empid"])
                    newdict["mn"] = newdict["mn"] + list(rankdf[rankdf["Elem"] == eachelem]["mn"])
                    newdict["Rank"] = newdict["Rank"] + [eachrank] * len(list(rankdf[rankdf["Elem"] == eachelem]["Empid"]))
                    newdict["Elem"] = newdict["Elem"] + list(rankdf[rankdf["Elem"] == eachelem]["Elem"])
                    newdict["CurAmount"] = newdict["CurAmount"] + list(rankdf[rankdf["Elem"] == eachelem]["CurAmount"])
                    
                
                elif elemcount/empnum >= 0.95:
                    seta = set(rankdf["Empid"])
                    setb = set(rankdf[~rankdf["Elem"].isin([eachelem])]["Empid"])
                    difset = seta.difference(setb)
                    
                    if len(difset) > 0:
                        newdict["Empid"] = newdict["Empid"] + list(difset)
                        newdict["mn"] = newdict["mn"] + [np.nan] * len(difset)
                        newdict["Rank"] = newdict["Rank"] + [eachrank] * len(difset) 
                        newdict["Elem"] = newdict["Elem"] + [eachelem] * len(difset)
                        newdict["CurAmount"] = newdict["CurAmount"] + [np.nan]* len(difset)
                    #
                #
            #
            
    #

    resdf = pd.DataFrame.from_dict(newdict)
    resdf.sort_values(by=['Elem'],inplace=True)
            
    resdf.head(10)

    resdf.to_excel(xlwriter,sheet_name="semel_once",index=False)

    return len(resdf)

#
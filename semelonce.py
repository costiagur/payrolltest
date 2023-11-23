#סמלים שמופיעים פעם אחת
import pandas as pd
import numpy as np

def semelonce(df,xlwriter,refmonth,prevmonth,level="0.05"):

    level = float(level)

    middf = df[(df["Division"] != 90)&(df["Refdate"]==refmonth)&(df["CurAmount"] != 0)&(df["Elemtype"] == "addition components")]

    resdict= dict()
    resdict["Empid"] = []
    resdict["Empname"] = []
    resdict["mn"] = []
    resdict["Rank"] = []
    resdict["Elem_heb"] = []
    resdict["CurAmount"] = []

    for eachrank in middf["Rank"].unique():
            rankdf = middf[middf["Rank"] == eachrank]
            empnum = len(rankdf["Empid"].unique())
            elemdf = rankdf["Elem"].value_counts()      
            
            for eachelem in elemdf.index:
                elemcount = elemdf[eachelem]

                if elemcount/empnum < (1-level) and elemcount/empnum > level:
                    pass
                elif elemcount/empnum <= level:
                    resdict["Empid"] = resdict["Empid"] + rankdf.loc[(rankdf["Elem"] == eachelem)&(rankdf["Rank"] == eachrank),"Empid"].to_list()
                    resdict["Empname"] = resdict["Empname"] + rankdf.loc[(rankdf["Elem"] == eachelem)&(rankdf["Rank"] == eachrank),"Empname"].to_list()
                    resdict["mn"] = resdict["mn"] + rankdf.loc[(rankdf["Elem"] == eachelem)&(rankdf["Rank"] == eachrank),"mn"].to_list()
                    resdict["Rank"] = resdict["Rank"] + rankdf.loc[(rankdf["Elem"] == eachelem)&(rankdf["Rank"] == eachrank),"Rank"].to_list()
                    resdict["Elem_heb"] = resdict["Elem_heb"] + rankdf.loc[(rankdf["Elem"] == eachelem)&(rankdf["Rank"] == eachrank),"Elem_heb"].to_list()
                    resdict["CurAmount"] = resdict["CurAmount"] + rankdf.loc[(rankdf["Elem"] == eachelem)&(rankdf["Rank"] == eachrank),"CurAmount"].to_list()
                    
                
                elif elemcount/empnum >= (1-level):
                    seta = set(rankdf["Empid"])
                    setb = set(rankdf[~rankdf["Elem"].isin([eachelem])]["Empid"])
                    difset = seta.difference(setb)
                    
                    if len(difset) > 0:
                        resdict["Empid"] = resdict["Empid"] + list(difset)
                        for eachid in difset:
                            resdict["Empname"] = resdict["Empname"] + [middf.loc[middf["Empid"]==eachid,"Empname"].unique()[0]] # requires loop because there might be two employees with the same name
                        #
                        resdict["mn"] = resdict["mn"] + [np.nan] * len(difset)
                        resdict["Rank"] = resdict["Rank"] + [eachrank] * len(difset) 
                        resdict["Elem_heb"] = resdict["Elem_heb"] + [eachelem] * len(difset)
                        resdict["CurAmount"] = resdict["CurAmount"] + [np.nan]* len(difset)
                    #
                #
            #
            
    #

    resdf = pd.DataFrame.from_dict(resdict)
    resdf.sort_values(by=['Elem_heb'],inplace=True)
            
    resdf.head(10)

    resdf.to_excel(xlwriter,sheet_name="semel_once",index=False)

    return len(resdf["Empid"].unique())

#
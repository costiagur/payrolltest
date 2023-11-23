#מס הכנסה גבוה
import pandas as pd

def semeltax(df,xlwriter,refmonth,prevmonth,level="0.44"):
 
    level = float(level)
    
    emps = set(df["Empid"])

    resdict = dict()
    resdict["Empid"] = []
    resdict["Empname"] = []
    resdict["Gross"] = []
    resdict["Elem_heb"] = []
    resdict["CurAmount"] = []
    resdict["Ratio"] = []

    middf = df.groupby(by = ["Empid","Elemtype"],as_index=False,group_keys=True).sum("CurAmount")

    for eachemp in emps:
        
        gross = sum(middf.loc[(middf["Empid"] == eachemp)&(middf["Elemtype"].isin(["addition components","benefit charge components"])),["CurAmount"]].sum())
        

        if gross == 0:
            continue
        #
        
        tax = middf.loc[(middf["Empid"] == eachemp)&(middf["Elemtype"] == "compulsory deductions"),"CurAmount"].sum()
        
        taxrate = tax / gross
        
        if taxrate > level:
            eachiddf = df[(df["Empid"] == eachemp)&(df["Elemtype"] == "compulsory deductions")][["Empid","Empname","Elem_heb","CurAmount"]]
            eachidroupdf = eachiddf.groupby(by=["Empid","Empname","Elem_heb"],as_index=False,group_keys=True).sum("CurAmount")

            resdict["Empid"] = resdict["Empid"] + eachidroupdf["Empid"].to_list()
            resdict["Empname"] = resdict["Empname"] +eachidroupdf["Empname"].to_list()
            resdict["Gross"] = resdict["Gross"] + [gross]*eachidroupdf["Elem_heb"].count()
            resdict["Elem_heb"] = resdict["Elem_heb"] + eachidroupdf["Elem_heb"].to_list()
            resdict["CurAmount"] = resdict["CurAmount"] + eachidroupdf["CurAmount"].to_list()
            resdict["Ratio"] = resdict["Ratio"] + [eachval/gross for eachval in eachidroupdf["CurAmount"].to_list()]
        #
    #

    resdf = pd.DataFrame.from_dict(resdict)
    resdf.to_excel(xlwriter,sheet_name="hightax",index=False)

    resdf.head(10)
    
    return len(resdf["Empid"].unique())
#
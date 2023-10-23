#מס הכנסה גבוה
import pandas as pd

def semeltax(df,xlwriter,refmonth,prevmonth,level="0.44"):
 
    level = float(level)
    
    emps = set(df["Empid"])

    resdict = dict()
    resdict["Empid"] = []
    resdict["Gross"] = []
    resdict["semel"] = []
    resdict["Value"] = []
    resdict["Ratio"] = []

    grouped = df.groupby(by = ["Empid","Elemtype"],as_index=False,group_keys=True)["CurAmount"]
    middf = grouped.sum("CurAmount")

    for eachemp in emps:
        
        gross = sum(middf[(middf["Empid"] == eachemp)&(middf["Elemtype"].isin(["addition components","benefit charge components"]))]["CurAmount"])
        
        if gross == 0:
            continue
        #
        
        tax = sum(middf[(middf["Empid"] == eachemp)&(middf["Elemtype"] == "compulsory deductions")]["CurAmount"])
        
        taxrate = tax / gross
        
        if taxrate > level:
            elems = set(df[(df["Empid"] == eachemp)&(df["Elemtype"] == "compulsory deductions")]["Elem"])
            
            for eachelem in elems:
                elemval = sum(df[(df["Empid"] == eachemp)&(df["Elem"] == eachelem)]["CurAmount"])
                
                resdict["Empid"].append(eachemp)
                resdict["Gross"].append(gross)
                resdict["semel"].append(eachelem)
                resdict["Value"].append(elemval)
                resdict["Ratio"].append(elemval / gross)
            #
        #
    #

    resdf = pd.DataFrame.from_dict(resdict)
    resdf.to_excel(xlwriter,sheet_name="hightax",index=False)

    resdf.head(10)
    
    return len(resdf["Empid"].unique())
#
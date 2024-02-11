import pandas as pd
import numpy as np

def fundsreplace(buffedfile):
    cols = list(range(4,11,1)) + list(range(13,32,1)) + [34,35,36,55]

    df = pd.read_csv(buffedfile,sep=';',header=4,encoding="cp1255",na_filter=True,skip_blank_lines=True,usecols=cols, parse_dates=['תאריך ערך'],dayfirst=True)
    df.rename(columns={"שם עובד":"Empname","מספר עובד":"Empid","מ.נ.":"mn","מספר פרטי קופה":"fundnum","תאריך ערך":"Refdate","ברוטו לפנסיה":"gross",
                    r'סה"כ לתשלום':"totalpay","מספר אוצר":"ozarnum","סוג תקבול":"paytype","רובד שכר":"paysource","סווג קופה":"fundtype_heb","מעמד הפקדה בקופה":"invstate"},inplace=True)

    df["baseelem"] = 3007*(df["fundtype_heb"] == "קרן השתלמות") + 3008 * (df["paysource"] == 6) + 3009 * (df["paysource"] == 5) + 3006 * (df["fundtype_heb"] != "קרן השתלמות" )* (df["paysource"] == 1)
    df["pizuimrate"] = round(df["הפרשה לפיצויים"]/df["gross"],2)

    df["fundtype"] = 6 * (df["baseelem"] == 3007) + 5 * (df["baseelem"] == 3008) + 4 * (df["baseelem"] == 3009)  + \
    7 * (df["baseelem"] == 3006) * (df["invstate"] == 2) + 8 * (df["baseelem"] == 3006) * (df["invstate"] == 1) * (df["pizuimrate"] >= 1.99) * (df["pizuimrate"] <= 2.16) + \
    3 * (df["baseelem"] == 3006) * (df["invstate"] == 1) * (df["pizuimrate"] < 1.99) * (df["pizuimrate"] > 2.16) 

    df["fundtype"].replace(to_replace = 0, value=3,inplace=True)

    df.dropna(axis=0,subset=['totalpay','gross'],inplace=True)

    refmonth = df["Refdate"].max()

    resdict = {}
    resdict["90226"] = []
    resdict["clientnum"] = []
    resdict["empid"] = []
    resdict["mn"] = []
    resdict["empname"] = []
    resdict["element"] = []
    resdict["startdate"] = []
    resdict["enddate"] = []
    resdict["updatecode"] = []
    resdict["amount"] = []

    ids = df.loc[df["paytype"] == 4,"Empid"].unique()

    for eachid in ids:
        fundtypes = df.loc[(df["paytype"] == 4) & (df["Empid"] == eachid), "fundtype"].unique()
        for fundtype in fundtypes:
                currozars = df.loc[(df["paytype"] == 1) & (df["Empid"] == eachid) & (df["fundtype"] == fundtype) & (df["gross"] != 0), "ozarnum"] # may be several funds, when pension is dispersed
                retroozars = df.loc[(df["paytype"] == 4) & (df["Empid"] == eachid) & (df["fundtype"] == fundtype) & (df["gross"] != 0), "ozarnum"] #same, or several retros
                
                retroset = set(retroozars)
                
                currset = set(currozars)
                
                resset = retroset.difference(currset)

                if len(resset) != 0 and len(currset) != 0 and len(retroset) != 0: # if there are ozars that are not in current set
                    
                    #print("id:{} currset:{} retroset: {} resset: {}".format(eachid,currset,retroset,resset))
                    
                    
                    for retroozar in resset:
                        middf = df.loc[(df["paytype"] == 4) & (df["Empid"] == eachid) & (df["fundtype"] == fundtype) & (df["ozarnum"] == retroozar) & (df["gross"] != 0), ["Empid","mn","baseelem","gross","Refdate","fundtype","ozarnum"]]
                        #print(middf)
                        count = middf["baseelem"].count()

                        for i in [-1,1]:
                            
                            resdict["90226"] = resdict["90226"] + ["90226"]*count
                            resdict["clientnum"] = resdict["clientnum"] + ["##clientnum##"]*count
                            resdict["empid"] = resdict["empid"] + [eachid]*count
                            resdict["mn"] = resdict["mn"] + middf["mn"].to_list()
                            resdict["empname"] = resdict["empname"] + [""]*count
                            resdict["element"] = resdict["element"] + middf["baseelem"].to_list()
                            
                            if i == -1:
                                resdict["startdate"] = resdict["startdate"] + [x.strftime("%d/%m/%Y") for x in middf["Refdate"].to_list()]
                                                      
                                enddatelist = [x + pd.DateOffset(months = 1, days=-1) for x in middf["Refdate"]]
                                resdict["enddate"] = resdict["enddate"] + [x.strftime("%d/%m/%Y") for x in enddatelist]
                            
                            elif i == 1:
                                resdict["startdate"] = resdict["startdate"] + [refmonth.strftime("%d/%m/%Y")]*count 

                                enddate = pd.to_datetime(refmonth) + pd.DateOffset(months = 1, days=-1)
                                resdict["enddate"] = resdict["enddate"] + [enddate.strftime("%d/%m/%Y")]*count
                            #

                            resdict["updatecode"] = resdict["updatecode"] + ["1"] * count
                            resdict["amount"] = resdict["amount"] + [x*i for x in middf["gross"].to_list()]
                        #
                    #
                #
            #
        #
    #
                
    #
    resdf = pd.DataFrame.from_dict(resdict)

    filename = ".\\drafts\\funds"+ refmonth.strftime("%Y-%m") +".csv"

    resdf.to_csv(filename,sep=",",header=False,index=False)

    return filename
#

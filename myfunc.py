import base64
import json
import common
import pandas as pd
import numpy as np
from io import BytesIO
from os import unlink
import concurrent.futures
from datetime import date
from openpyxl import Workbook
from totalrep import totalrep
from pubtrasport_nowork import pubtrasport_nowork
from semel_ratio import semel_ratio
from BasisvsCalculated import BasisvsCalculated
from semel_payhours import semel_payhours
from semel_konenut import semel_konenut
from semel_hourdeduct import semel_hourdeduct
from semel6666 import semel6666
from hightax import hightax
from semelonce import semelonce
from fundscount import fundscount
from vehicle_annual import vehicle_annual
from hoursWithoutYesod import hoursWithoutYesod
from manyhours import manyhours
from highgrossbtl import highgrossbtl
from semeltwice import semeltwice
from before9months import before9months
#from fundsreplace import fundsreplace
from NonreasonableNett import NonreasonableNett
from semel_without import semel_without
import custom
from loaddf import loaddf
from nettnegative import nettnegative
from rationonbase import rationonbase
from ratelow import ratelow
from adhoctest import adhoctest
from analysis13m import analysis13m
from onecompare import onecompare
from llmquery import llmquery
from sqlquery import sqlquery

CODESTR = "hazuticheck"

def myfunc(queryobj):
#    try:
        postdict = queryobj._POST()
        filesdict = queryobj._FILES()      

        request = postdict["request"]
        
        if request == "fileupload":
            res = loaddf(filesdict,postdict["reqfiletype"])
            replymsg = json.dumps(["uploadedrows",res]).encode('UTF-8')
          
            custom.xlresfile = BytesIO()
            wb = Workbook()
            wb.save(custom.xlresfile)
            
        elif request == "salarycheck":
            replymsg = b""

            reqtest = postdict["reqtest"]
            reqlevel = postdict["reqlevel"]
                        
            checkpool = {}

            checkpool["semel_konenut"] = semel_konenut
            checkpool["semel_payhours"] = semel_payhours
            checkpool["semel_hourdeduct"] = semel_hourdeduct
            checkpool["pubtrasport_nowork"] = pubtrasport_nowork
            checkpool["semel6666"] = semel6666
            checkpool["semel_ratio"] = semel_ratio
            checkpool["BasisvsCalculated"] = BasisvsCalculated
            checkpool["vehicle_annual"] = vehicle_annual
            checkpool["semelonce"] = semelonce
            checkpool["hightax"] = hightax
            checkpool["fundscount"] = fundscount
            checkpool["hoursWithoutYesod"] = hoursWithoutYesod
            checkpool["manyhours"] = manyhours
            checkpool["highgrossbtl"] = highgrossbtl
            checkpool["before9months"] = before9months
            checkpool["totalrep"] = totalrep
            checkpool["NonreasonableNett"] = NonreasonableNett
            checkpool["semel_without"] = semel_without
            checkpool["nettnegative"] = nettnegative
            checkpool["rationonbase"] = rationonbase
            checkpool["ratelow"] = ratelow

            res = checkpool[reqtest](reqlevel)
            replymsg = json.dumps([res[0],res[1],res[2]]).encode('UTF-8')


        elif request == "testfile": #request for the resulting XL file with all the tests
                        
            f = custom.xlresfile
            f.seek(0)
            file64enc = base64.b64encode(f.read())
            file64dec = file64enc.decode()
            replymsg = json.dumps(["testfile",r'report_' + date.today().strftime('%Y%m%d') + ".xlsx",file64dec]).encode('UTF-8') #f.name
        #

        elif request == "adhoctest":
            adhocfile = adhoctest(postdict["semel"],postdict["reqtype"],postdict["pensionin"])
            adhocfile.seek(0)
            file64enc = base64.b64encode(adhocfile.read())
            file64dec = file64enc.decode()
            replymsg = json.dumps(["adhocfile",postdict["semel"] + ".xlsx",file64dec]).encode('UTF-8')
        #

        elif request == "hazuti13m":   
            file64enc = base64.b64encode(analysis13m(filesdict,postdict["expectedplus"]))
            file64dec = file64enc.decode()
            replymsg = json.dumps(["outliers.xlsx",file64dec]).encode('UTF-8')
        #

        elif request == "onecompare":
            resdf = onecompare(postdict["empid"])
            replymsg = json.dumps(["oneperson",resdf]).encode('UTF-8')
        #

        elif request == "llmquery":
            restxt = llmquery(postdict["myrequest"],postdict["reqtype"])
            replymsg = json.dumps([postdict["reqtype"],restxt]).encode('UTF-8')
        #
        
        elif request == "sqlquery":
            if postdict["how"] == 'show':
                resjson = sqlquery(postdict["myrequest"],'show')
                replymsg = json.dumps(resjson).encode('UTF-8')
            elif postdict["how"] == 'xls':
                file64enc = base64.b64encode(sqlquery(postdict["myrequest"],'xls'))
                file64dec = file64enc.decode()
                replymsg = json.dumps(["Result",['timesheet_output.xlsx',file64dec]]).encode('UTF-8')
            #
        #

        return replymsg
 
            # reply message should be encoded to be sent back to browser ----------------------------------------------
            # encoding to base64 is used to send ansi hebrew data. it is decoded to become string and put into json.
            # json is encoded to be sent to browser.
            #    file64enc = base64.b64encode(filesdict['doc1'][1])
            #    file64dec = file64enc.decode()
  

    #
    
#    except Exception as e:
#        common.errormsg(title=__name__,message=e)
#        replymsg = json.dumps(["Error","myfunc -" + str(e)]).encode('UTF-8')
#        return replymsg
    #
#
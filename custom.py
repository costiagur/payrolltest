xlresfile = None

## Ranks ##
hozeishi = ("","") #All types of Hoze Ishi. treat as text ("")
edufund_fromsecondyear = ("","","") #Numbers of Ranks that are eligible for education fund starting from the second employment year
sayaot = "" #Number of Rank of payment to Sayaot, according to Sayaot General Agreement
hourwageranks = ("","") #Ranks that are paid on an by-hour basis

## High Offices Codes ##
managers = (,,,) job numbers of high officers

## Symbols ##
konenut = "" #Symbol of Konenut
byhourpay = "" #Symbol of by-hour pay
yesod = "" #Symbol of basic payment, according to CBA tables
hourdeduct = "" #Symbol of hour deduction
yesodandhours = (yesod,byhourpay) #Symbols of Shar Yesod and By-hour pay
meshulav = ("","") #Symbols of Shar Yesd and Vetek addition
pubtransport = ("",) #Symbol of reimbursement for public transporation to get to work
yesod = "" #Symbol os shar yesod
semelratio = "" #Symbol of Salary Ratio
semelnett = "" #Symbol of Nett payment (to bank)
takzivit = "" #Symbol of obligitary deduction to Budget Pension funds
pensionbasesemel = "" #Symbol of salary wich serves as a pension base
pensiondepartment = #Number of Pension Department
grossbtlsemel = "" #Symbol of Gross Salary for the need of  National Security Institute
elemtax = "" #Symbol of tax levied by Tax Authority
nettnegative = "" #Symbol of nett negative values to be deducted in the next payroll
hourvalue = "" #Symbol of a value of an hour
dayvalue = "" #Symbol of day value

unneededdeductions = ("","") #Symbols of deductions that are not to funds
annualelement = ("","")  #Symbols of annual payments
byreport = ("","") #Symbols athat are part of pension base but requre explicit reporting (not automaticly stem from rank). Thus they are multiplied by employment ratio.

inbase = ("","","","") #Symbols wich may be part of pension base, but are not paid on a monthly basis
nottakzivitbase = ("","") #symbols which thoug are in pension base, are not part of Budget Pnesion
nonpension = ("","") #Symbols of payment which don't involve provisions to funds
lics = ("","") #Symbols of payment for vehicle authorization costs
inshova = ("","") #Symbols of payment for obligatory vehicle insurance
instotal = ("","","","") + inshova #Symbols of payment for vehicle insurance
elembtl = ("","") #Symbols of taxes levied by National Security Institute
pizuim = ("","","","") #Symbols of Severity payment Advance Announcement payment not obligable by National Security Institute
HodaaMukdemetHayavBL = ("",) #Symbol pf Advance Announcement payment for the first month wich is taxed by National Security Institute
gmarheshbon = pizuim + HodaaMukdemetHayavBL + ("",) #Symbol of vacation payment
miluim = ("","") #Symbol of Miluim payment
vacationadds = ("","") #payments for work at children holydays
extrahours = ("","") #Symbols of payments for extrahours
expense = ("","") + pubtransport #Symbols of expense reimbursement payments, like monthly return for personal vehicle
gilum = ("","") #Symbols of gross up payments
annualvehicle = lics + instotal + ("","") #symbols of annual reimbursements of vehicle authorization and insurance, including gross-ups to compensate for tax deduction

dbsave = "path to dbsave.db"
draftslib = "path to drafts folder"

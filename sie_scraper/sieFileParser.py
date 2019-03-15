import codecs
import time
from sqlalchemy import *
from headerData import headerData
import periodEndBalance
import verTransData
import yearEndBalance
import otherTagData
import sys
from Email import sendEmail
import re

organization_num = ''

# insert data and delete old data if org_num already exist in the database
def execute(filename, dropbox_file):
    # Function takes two argument filename is path of file on local system and
    # dropbox_file is path of file inside dropbox
    f = codecs.open(filename, encoding='cp437', mode='r')
    #replace multiple blank spaces with single space
    response = (f.read())+" "+"#"
    response = re.sub('\t', ' ', re.sub(' +',' ',response))
    # converting all the text from the file into the list
    split = ((response.replace("  "," ").replace(" ","_")).replace("\n","_")).replace('\r',"").split("_")
    #print split
    org_no =None
    SIETYP = None
    start_date = None
    end_date = None
    global organization_num
    # read organisation number from the file
    for i in range(0, len(split)):
        if (split[i] == "#ORGNR"):
            org_no = str(split[i + 1]).replace('\r',"")
            organization_num = org_no
            print "org no"+ org_no
            break

    for i in range(0, len(split)):
        if (split[i] == "#SIETYP"):
            SIETYP = str(split[i + 1]).replace('\r', "")
            organization_num = org_no
            # print org_no
            break

    for i in range(0, len(split)):
        if (split[i] == "#RAR"):
            print "tested"
            start_date = split[i + 2].strip()
            print start_date
            end_date = split[i + 3].strip()
            break

    # Convert start_date, end_date and today's date into epoch for comparision
    timestruct_start = time.strptime(start_date, "%Y%m%d")
    start_date = time.mktime(timestruct_start)
    #print start_date



    timestruct_end = time.strptime(end_date, "%Y%m%d")
    end_date = time.mktime(timestruct_end)
    #print end_date


    today = time.strftime("%Y%m%d")
    timestruct_today = time.strptime(today, "%Y%m%d")
    today = time.mktime(timestruct_today)
    #print today
    # print "new testeddd"

    # check today's between start date and end date
    if (start_date <= today <= end_date):
        #print "condition true"
        # if file does not contain organization number then send mail
        if (org_no == None):
            message = "The Organization Number is missing from the "+(dropbox_file).encode('utf-8')
            sendEmail(message)
            #sys.exit(0)
        else:
            # list of all the table name in the database
            database_list = ["Account_list(#KONTO)","Closing_balance(#UB)","Closing_balance_obj(#OUB)","Dimension(#DIM)",
                         "Financial_year(#RAR)","Header","Object(#OBJEKT)","Opening_balance(#IB)","Opening_balance_obj(#OIB)",
                         "Period_End_Balance(#PSALDO)","Period_budget_item(#PBUDGET)",
                         "Result(#RES)","SRU_code(#SRU)","Verification_Transaction(#VER/#TRANS)","Sub_Dimension(#UNDERDIM)"]

            # db instance
            db = create_engine("postgresql://fortnoxDB:14kdvKsI7IfeFfwn@35.195.0.180/postgres")
            metadata = MetaData(db)
            #Table object
            db_obj = Table('Header', metadata, autoload=True)
            ins_select = db_obj.select().where(and_(db_obj.c.Org_no == org_no, db_obj.c.SIETYP==SIETYP))
            # check file data already exist in the database or not
            if (len(ins_select.execute().fetchall()) == 0):
                # if data is not present then insert all the data into databse
                print "data is not present"
                insertData(split, metadata, org_no, SIETYP)
            else:
                # delete all the existing data and stored the new data
                print "data is present"
                for i in range(0,len(database_list)):
                    db_obj = Table(database_list[i], metadata, autoload=True)
                    ins = db_obj.delete().where(and_(db_obj.c.Org_no == org_no, db_obj.c.SIETYP==SIETYP))
                    ins.execute()
                insertData(split, metadata, org_no, SIETYP)
    else:
        #print "condiion false"
        message = "File not available for current financial year: " + (dropbox_file).encode('utf-8')
        sendEmail(message)

#insert all the data into the seperate table in the database
def insertData(split, metadata, org_no, SIETYP):
    headerData(split, metadata, org_no, SIETYP)
    #periodEndBalance.periodEndBalanceWithDimObjData(split, metadata, org_no, SIETYP)
    periodEndBalance.periodEndBalanceWithoutDimObjData(split, metadata, org_no, SIETYP)
    #periodEndBalance.periodBudgetItemWithDimObjData(split, metadata, org_no, SIETYP)
    periodEndBalance.periodEndBudgetWithoutDimObjData(split, metadata, org_no, SIETYP)
    periodEndBalance.subDimensionData(split, metadata, org_no, SIETYP)
    yearEndBalance.openingBalanceData(split, metadata, org_no, SIETYP)
    yearEndBalance.openingBalanceObjData(split, metadata, org_no, SIETYP)
    yearEndBalance.closingBalanceData(split, metadata, org_no, SIETYP)
    yearEndBalance.closingBalanceObjData(split, metadata, org_no, SIETYP)
    otherTagData.resultData(split, metadata, org_no, SIETYP)
    otherTagData.financialYearData(split, metadata, org_no, SIETYP)
    otherTagData.accountListData(split, metadata, org_no, SIETYP)
    otherTagData.sruCodeData(split, metadata, org_no, SIETYP)
    otherTagData.dimensionData(split, metadata, org_no, SIETYP)
    otherTagData.objectData(split, metadata, org_no, SIETYP)
    verTransData.verTransData(split, metadata, org_no, SIETYP)



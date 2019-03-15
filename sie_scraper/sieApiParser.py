import requests
import codecs
import time
from sqlalchemy import *
from yearEndBalance import *
import headerData
import periodEndBalance
import verTransData
import yearEndBalance
import otherTagData
from sqlalchemy import *
import traceback
from Email import sendEmail

URL = ""

def send_request(URL, access_token, secret_key):
    # Takes URL (ie. API endpoint), Access token and Secret Key as an argument
    # send request to get response
    try:
        r = requests.get(
            url=URL,
            headers = {
                "Access-Token":access_token,
                "Client-Secret":secret_key,
                "Content-Type":"application/json",
                "Accept":"application/json",
            },
        )
        print(r.status_code)
        if r.status_code != 200:
            message = URL + "\n" + "Incorrect response from API"
            sendEmail(message)
            exit()
        else:
            output = r.content
        # return response received from the API
        return output
        
    except requests.exceptions.RequestException as e:
        print('HTTP Request failed')

#insert all the data into the seperate table in the database
def insertData(split,metadata,org_no,SIETYP):
    headerData.headerData(split, metadata,org_no,SIETYP)
    # periodEndBalance.periodEndBalanceWithoutDimObjData(split, metadata, org_no, SIETYP)
    # periodEndBalance.periodEndBudgetWithoutDimObjData(split, metadata, org_no, SIETYP)
    # periodEndBalance.subDimensionData(split, metadata, org_no, SIETYP)
    # yearEndBalance.openingBalanceData(split, metadata, org_no, SIETYP)
    # yearEndBalance.openingBalanceObjData(split, metadata, org_no, SIETYP)
    # yearEndBalance.closingBalanceData(split, metadata, org_no, SIETYP)
    # yearEndBalance.closingBalanceObjData(split, metadata, org_no, SIETYP)
    # otherTagData.resultData(split, metadata, org_no, SIETYP)
    # otherTagData.financialYearData(split, metadata, org_no, SIETYP)
    # otherTagData.accountListData(split, metadata, org_no, SIETYP)
    # otherTagData.sruCodeData(split, metadata, org_no, SIETYP)
    # otherTagData.dimensionData(split, metadata, org_no, SIETYP)
    # otherTagData.objectData(split, metadata, org_no, SIETYP)
    # verTransData.verTransData(split, metadata, org_no, SIETYP)


def execute():
    # Read API credential from DB.
    db = create_engine("postgresql://fortnoxDB:14kdvKsI7IfeFfwn@35.195.0.180/postgres")
    metadata = MetaData(db)
    db_obj = Table('Api_credential', metadata, autoload=True)
    ins = db_obj.select()
    global URL
    result = ins.execute().fetchall()
    #for loop read all API credential one by one
    for i in range(0, len(result)):
        URL = result[i][0]
        access_token = result[i][1]
        secret_key = result[i][2]
        f_num = int(URL.split("financialyear=",1)[1])
        #for loop to increment financial number
        for num in range(0,1000):
            #print "num is "+str(num)
            #print f_num
            #splitting URL to get financial number out

            financial_num = f_num+num
            URL = URL.split("financialyear=",1)[0]+"financialyear="+str(financial_num)
            print URL


            #Fetch response from api
            response = send_request(URL, access_token, secret_key)
            #print response
            response = codecs.decode(response,'cp437')
            #to check response is blank or not
            
            if "ErrorInformation" in response:
                message = URL +"\n"+response
                sendEmail(message)
                break
            else:
                #convert text response into the list
                split = ((response.replace(" ","_")).replace("\r","").replace("\n","_")).split("_")
                #print split
                org_no = None
                SIETYP = 0
                start_date = None
                end_date = None

                # read organisation number from the API response
                for i in range(0, len(split)):
                    if (split[i] == "#ORGNR"):
                        org_no = str(split[i + 1])
                        
                        #commented code to check length of org_no
                        # count = 0
                        # for c in org_no:
                        #     if c != "e":
                        #         count += 1
                        # print count
                        break

                for i in range(0, len(split)):
                    if (split[i] == "#SIETYP"):
                        SIETYP = str(split[i + 1]).replace('\r', "")
                        break

                for i in range(0, len(split)):
                    if(split[i] == "#RAR"):
                        start_date = split[i+2]
                        end_date = split[i+3]
                        break

                #Convert start_date, end_date and today's date into epoch for comparision
                timestruct_start = time.strptime(start_date, "%Y%m%d")
                start_date = time.mktime(timestruct_start)

                timestruct_end = time.strptime(end_date, "%Y%m%d")
                end_date = time.mktime(timestruct_end)

                today = time.strftime("%Y%m%d")
                timestruct_today = time.strptime(today, "%Y%m%d")
                today = time.mktime(timestruct_today)
                #print "new testeddd"

                #check today's between start date and end date
                if (start_date <= today <= end_date):
                    #print "testedddddd"
                    # if API response does not contain organization number then send mail
                    if (org_no == None):
                        message = "The Organization Number is missing from the API :" + URL
                        sendEmail(message)
                        break
                        # sys.exit(0)
                    else:
                        # list of all the table name in the database
                        database_list = ["Account_list(#KONTO)", "Closing_balance(#UB)", "Closing_balance_obj(#OUB)", "Dimension(#DIM)",
                                         "Financial_year(#RAR)", "Header", "Object(#OBJEKT)", "Opening_balance(#IB)",
                                         "Opening_balance_obj(#OIB)",
                                         "Period_End_Balance(#PSALDO)",
                                         "Period_budget_item(#PBUDGET)",
                                         "Result(#RES)", "SRU_code(#SRU)", "Verification_Transaction(#VER/#TRANS)", "Sub_Dimension(#UNDERDIM)"]

                        # Table object
                        #print split
                        db_obj = Table('Header', metadata, autoload=True)
                        ins_select = db_obj.select().where(and_(db_obj.c.Org_no == org_no))
                        # check file data already exist in the database or not
                        if (len(ins_select.execute().fetchall()) == 0):
                            # if data is not present then insert all the data into databse
                            insertData(split, metadata, org_no, SIETYP)
                            break
                        else:
                            # delete all the existing data and stored the new data
                            for i in range(0, len(database_list)):
                                db_obj = Table(database_list[i], metadata, autoload=True)
                                ins = db_obj.delete().where(db_obj.c.Org_no == org_no)
                                #print "delete data"
                                ins.execute()
                            insertData(split, metadata, org_no, SIETYP)
                            break



if __name__ == '__main__':
    try:
        execute()
    except:
        # message to attach in mail
        message =  URL + "\n\n" + traceback.format_exc()
        # send mail with error info
        sendEmail(message)



from flask import abort, Flask, redirect, render_template, request, session, url_for
import os
import time
import threading
import fileAutomation
import sieFileParser
import datetime
import traceback
from sqlalchemy import *
from Email import sendEmail
import sys

#create object of flask
app = Flask(__name__)
#App Secret key for droppbox application
APP_SECRET = 'qmevdx3rohasue5'

#global filaname list to handle redundant notification from dropbox
filename_list = []

#delete existing data if script breaks
def delExistingData(org_number):
    # list of all the table name in the database
    database_list = ["Account_list(#KONTO)", "Closing_balance(#UB)", "Closing_balance_obj(#OUB)", "Dimension(#DIM)",
                     "Financial_year(#RAR)", "Header", "Object(#OBJEKT)", "Opening_balance(#IB)",
                     "Opening_balance_obj(#OIB)",
                     "Period_End_Balance(#PSALDO)",
                     "Period_budget_item(#PBUDGET)",
                     "Result(#RES)", "SRU_code(#SRU)", "Verification_Transaction(#VER/#TRANS)", "Sub_Dimension(#UNDERDIM)"]

    # db instance
    db = create_engine("postgresql://fortnoxDB:14kdvKsI7IfeFfwn@35.195.0.180/postgres")
    metadata = MetaData(db)
    # Table object
    db_obj = Table('Header', metadata, autoload=True)
    ins_select = db_obj.select().where(and_(db_obj.c.Org_no == org_number))
    print "organization number is "+org_number
    # check file data already exist in the database or not
    if (len(ins_select.execute().fetchall()) != 0):
        print "tested"
        # delete all the existing data and stored the new data
        for i in range(0, len(database_list)):
            db_obj = Table(database_list[i], metadata, autoload=True)
            ins = db_obj.delete().where(db_obj.c.Org_no == org_number)
            ins.execute()


#this function start executing when GET request received from dropbox
@app.route('/webhookEnhanzanew', methods=['GET'])
def challenge():
    '''Respond to the webhook challenge (GET request) by echoing back the challenge parameter.'''
    if request.method == "GET":
        challenge1 = request.args.get('challenge')
        # print "hello"
        return challenge1  # request.args.get('challenge')


#this function start executing when POST request received from dropbox
@app.route('/webhookEnhanzanew', methods=['POST'])
def webhook():
    try:
        #create seperate thread for each notification and execute the automate function
        print "Inside post request"
        threading.Thread(target=fileAutomation.automate()).start()
        return '200 OK'
    except:
        #create unique name by combnining file name and modified date
        global  filename_list
        file_name = fileAutomation.fileName
        mod_date = fileAutomation.mod_date
        unique_name = file_name+mod_date

        # if condition is true which means notification occur first time
        if (unique_name not in filename_list):
            # message to attach in mail
            #print "response to apiiiiiii"
            message = ((fileAutomation.fileName).encode('utf-8'))+ "\n\n" + traceback.format_exc()
            #send mail with error info
            sendEmail(message)
            delExistingData(sieFileParser.organization_num)
            filename_list.append(unique_name)
            #sys.exit(0)

            return "200 OK"
        else:
            delExistingData(sieFileParser.organization_num)
            #print filename_list
            print "Inside Else"
            return "200 OK"




if __name__ == "__main__":
    # create a externaly visible server
    app.run(host='0.0.0.0', port=8082, debug=False)
from sqlalchemy import *
import sqlalchemy

# stored all the data for tag "#RES"
def resultData(split, metadata, org_num, SIETYP):
    db_obj = Table('Result(#RES)', metadata, autoload=True)
    ins = db_obj.insert()
    # check for #RES tag in the .SE file or response from API
    for i in range(0, len(split)):
        if (split[i] == "#RES"):
            print("Inside #RES")
            org_no = org_num
            file_type = SIETYP
            year_no = int(split[i + 1])
            account = int(split[i + 2])
            balance = float(split[i + 3])
            # check quantity field present or not
            #print (year_no,account)
            #print split[i+4]
            if ("#" not in split[i + 4]) and ('' not in split[i+4]):
                quantity = int(split[i + 4])
            else:
                quantity = 0
            # fields stored into the table
            try:
                ins.execute(Org_no=org_no, Year_No=year_no, Account=account, Balance=balance, Quantity=quantity, SIETYP=file_type)
                print("resultData data added in the database")
            except sqlalchemy.exc.IntegrityError :
                print "Result"

# stored all the data for tag "#RAR"
def financialYearData(split, metadata, org_num, SIETYP):
    db_obj = Table('Financial_year(#RAR)', metadata, autoload=True)
    ins = db_obj.insert()
    # check for #RAR tag in the .SE file or response from API
    for i in range(0, len(split)):
        if (split[i] == "#RAR"):
            print("Inside #RAR")
            org_no = org_num
            file_type = SIETYP
            year_no = int(split[i + 1])
            start_date = int(split[i + 2])
            end_date = int(split[i + 3])
            print(org_no, year_no, start_date, end_date)
            # fields stored into the table
            try:
                ins.execute(Org_no=org_no, Year_No=year_no, Start_date=start_date, End_date=end_date, SIETYP=file_type)
                print("financialYearData data added in the database")
            except sqlalchemy.exc.IntegrityError :
                print "Financial_year"

# stored all the data for tag "#KONTO"
def accountListData(split, metadata, org_num, SIETYP):
    db_obj = Table('Account_list(#KONTO)', metadata, autoload=True)
    ins = db_obj.insert()
    # check for #KONTO tag in the .SE file or response from API
    for i in range(0, len(split)):
        if (split[i] == "#KONTO"):
            print("Inside #KONTO")
            org_no = org_num
            file_type = SIETYP
            account_no = int(split[i+1])
            account_name = " "
            for j in range(i + 2, len(split)):
                if "#" not in split[j]:
                    account_name = ((account_name + split[j] + " ").replace('"', ""))
                else:
                    break
            # fields stored into the table
            try:
                ins.execute(Org_no=org_no,Account_no=account_no,Account_name=account_name,SIETYP=file_type)
                print("accountListData data added in the database")
            except sqlalchemy.exc.IntegrityError:
                print "Account_list"

# stored all the data for tag "#SRU"
def sruCodeData(split, metadata, org_num, SIETYP):
    db_obj = Table('SRU_code(#SRU)', metadata, autoload=True)
    ins = db_obj.insert()
    # check for #SRU tag in the .SE file or response from API
    for i in range(0, len(split)):
        if (split[i] == "#SRU"):
            print("Inside #SRU")
            org_no = org_num
            file_type = SIETYP
            account_no = int(split[i+1])
            sru_code = " "
            for j in range(i + 2, len(split)):
                if "#" not in split[j]:
                    sru_code = ((sru_code + split[j] + " ").replace('"', ""))
                else:
                    break
            # fields stored into the table
            try:
                ins.execute(Org_no=org_no,Account_no=account_no,Sru_code=sru_code,SIETYP=file_type)
                print("sruCodeData data added in the database")
            except sqlalchemy.exc.IntegrityError :
                print "SRU_code"

# stored all the data for tag "#DIM"
def dimensionData(split, metadata, org_num, SIETYP):
    db_obj = Table('Dimension(#DIM)', metadata, autoload=True)
    ins = db_obj.insert()
    # check for #DIM tag in the .SE file or response from API
    for i in range(0, len(split)):
        if (split[i] == "#DIM"):
            print("Inside #DIM")
            org_no = org_num
            file_type = SIETYP
            dimension_no = split[i+1].replace('"', "")
            dimension_name = " "
            for j in range(i + 2, len(split)):
                if "#" not in split[j]:
                    dimension_name = ((dimension_name + split[j] + " ").replace('"', ""))
                else:
                    break
            # fields stored into the table
            try:
                ins.execute(Org_no=org_no,Dimension_no=dimension_no,Dimension_name=dimension_name,SIETYP=file_type)
                print("dimensionData data added in the database")
            except sqlalchemy.exc.IntegrityError :
                print "Dimension"

# stored all the data for tag "#OBJEKT"
def objectData(split, metadata, org_num, SIETYP):
    db_obj = Table('Object(#OBJEKT)', metadata, autoload=True)
    ins = db_obj.insert()
    # check for #OBJECT tag in the .SE file or response from API
    for i in range(0, len(split)):
        if (split[i] == "#OBJEKT"):
            print("Inside #OBJEKT")
            org_no = org_num
            file_type = SIETYP
            dimension_no = split[i+1].replace('"', "")
            object_no = split[i+2].replace('"', "")
            object_name = " "
            for j in range(i + 3, len(split)):
                if "#" not in split[j]:
                    object_name = ((object_name + split[j] + " ").replace('"', ""))
                else:
                    break
            # fields stored into the table
            try:
                ins.execute(Org_no=org_no,Dimension_no=dimension_no,Object_no=object_no,Object_name=object_name,SIETYP = file_type)
                print("objectData data added in the database")
            except sqlalchemy.exc.IntegrityError :
                print "Object"


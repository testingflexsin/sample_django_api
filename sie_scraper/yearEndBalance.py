from sqlalchemy import *
import sqlalchemy

# stored all the data for tag "#IB"
def openingBalanceData(split, metadata, org_num, SIETYP):
    db_obj = Table('Opening_balance(#IB)', metadata, autoload=True)
    ins = db_obj.insert()
    # check for #IB tag in the .SE file or response from API
    for i in range(0, len(split)):
        if (split[i] == "#IB"):
            print("Inside #IB")
            org_no = org_num
            file_type = SIETYP
            year_no = int(split[i + 1])
            account = int(split[i + 2])
            balance = float(split[i + 3])
            # check quantity field present or not
            if ("#" not in split[i + 4]) and ('' not in split[i+4]):
                quantity = int(split[i + 4])
            else:
                quantity = 0
            # fields stored into the table
            try:
                ins.execute(Org_no=org_no,SIETYP=file_type,Year_No=year_no, Account=account, Balance=balance, Quantity=quantity)
                print("openingBalanceData data added in the database")
            except sqlalchemy.exc.IntegrityError :
                print "Opening_balance"

# stored all the data for tag "#UB"
def closingBalanceData(split, metadata, org_num, SIETYP):
    db_obj = Table('Closing_balance(#UB)', metadata, autoload=True)
    ins = db_obj.insert()
    # check for #UB tag in the .SE file or response from API
    for i in range(0, len(split)):
        if (split[i] == "#UB"):
            print("Inside #UB")
            org_no = org_num
            file_type = SIETYP
            year_no = int(split[i + 1])
            account = int(split[i + 2])
            balance = float(split[i + 3])
            # check quantity field present or not
            if ("#" not in split[i + 4]) and ('' not in split[i+4]):
                quantity = int(split[i + 4])
            else:
                quantity = 0
            # fields stored into the table
            try:
                ins.execute(Org_no=org_no,SIETYP=file_type,Year_No=year_no, Account=account, Balance=balance, Quantity=quantity)
                print("closingBalanceData data added in the database")
            except sqlalchemy.exc.IntegrityError :
                print "Closing_balance"

# stored all the data for tag "#OIB"
def openingBalanceObjData(split, metadata, org_num, SIETYP):
    db_obj = Table('Opening_balance_obj(#OIB)', metadata, autoload=True)
    ins = db_obj.insert()
    # check for #OIB tag in the .SE file or response from API
    for i in range(0, len(split)):
        if (split[i] == "#OIB"):
            print("Inside #OIB")
            org_no = org_num
            file_type = SIETYP
            year_no = int(split[i + 1])
            account = int(split[i + 2])
            dim_no = ""
            obj_no = ""
            k = 3
            if (split[i + k] != "{}"):
                dim_no = (split[i + 3]).replace('"', "").replace('{', "").replace('\r', "")
                obj_no = (split[i + 4]).replace('"', "").replace('}', "").replace('\r', "")
                k = k + 2
            else:
                k = k + 1

            balance = float(split[i + k])
            # check quantity field present or not
            if ("#" not in split[i + k + 1]) and ('' not in split[i + k + 1]):
                quantity = int(split[i + k + 1])
            else:
                quantity = 0
            # fields stored into the table
            try:
                ins.execute(Org_no=org_no, SIETYP=file_type, Year_No=year_no, Account=account, Dimension_no=dim_no,
                        Obj_no=obj_no,Balance=balance, Quantity=quantity)
                print("openingBalanceObjData data added in the database")
            except sqlalchemy.exc.IntegrityError :
                print "Opening_balance_obj"

# stored all the data for tag "#OUB"
def closingBalanceObjData(split, metadata, org_num, SIETYP):
    db_obj = Table('Closing_balance_obj(#OUB)', metadata, autoload=True)
    ins = db_obj.insert()
    # check for #OUB tag in the .SE file or response from API
    for i in range(0, len(split)):
        if (split[i] == "#OUB"):
            print("Inside #OUB")
            org_no = org_num
            file_type = SIETYP
            year_no = int(split[i + 1])
            account = int(split[i + 2])
            dim_no = ""
            obj_no = ""
            k = 3
            if (split[i + k] != "{}"):
                dim_no = (split[i + 3]).replace('"', "").replace('{', "").replace('\r', "")
                obj_no = (split[i + 4]).replace('"', "").replace('}', "").replace('\r', "")
                k = k + 2
            else:
                k = k + 1

            balance = float(split[i + k])
            # check quantity field present or not
            if ("#" not in split[i + k + 1]) and ('' not in split[i + k + 1]):
                quantity = int(split[i + k + 1])
            else:
                quantity = 0
            # fields stored into the table
            try:
                ins.execute(Org_no=org_no,SIETYP=file_type, Year_No=year_no, Account=account, Dimension_no=dim_no,
                        Obj_no=obj_no,Balance=balance, Quantity=quantity)
                print("closingBalanceObjData data added in the database")
            except sqlalchemy.exc.IntegrityError:
                print "Closing_balance_obj"



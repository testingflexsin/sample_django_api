from sqlalchemy import *
import sqlalchemy

# stored all the data for tag "#PSALDO" which contain object and dimension field
def periodEndBalanceWithoutDimObjData(split, metadata, org_num, SIETYP):
    db_obj = Table('Period_End_Balance(#PSALDO)', metadata, autoload=True)
    ins = db_obj.insert()

    for i in range(0, len(split)):
        # check for #PSALDO tag in the .SE file or response from API
        if (split[i] == "#PSALDO"):
            print("Inside #PSALDO")
            if ((split[i + 4]) != "{}"):
                org_no = org_num
                file_type = SIETYP
                year_no = int(split[i + 1])
                # for j in range()
                period = int(split[i + 2])
                account = int(split[i + 3])
                dim_no = (split[i + 4]).replace('"', "").replace('{', "").replace('\r', "")
                obj_no = (split[i + 5]).replace('"', "").replace('}', "").replace('\r', "")
                Sub_Dim_no = ""
                Sub_Obj_no = ""
                k = 5
                count = 0

                for j in range(k, len(split)):
                    if ((split[i + k + 1] == "}") or ("}" in split[i + k])):
                        if (("}" in split[i + k])):
                            k = k + 1
                            break
                        else:
                            k = k + 2
                            break
                    else:
                        if (count != 1):
                            Sub_Dim_no = (split[i + k + 1]).replace('"', "").replace('}', "").replace('\r', "")
                            if ("}" in split[i + k + 2]):
                                Sub_Obj_no = (split[i + k + 2]).replace('"', "").replace('}', "").replace('\r', "")
                                k = k + 1
                                break
                            else:
                                Sub_Obj_no = (split[i + k + 2]).replace('"', "").replace('}', "").replace('\r', "")
                                k = k + 2
                                count = count + 1
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
                    # print (org_no, file_type, year_no, period, account, dim_no, obj_no, Sub_Dim_no, Sub_Obj_no, balance,
                    #        quantity)
                    ins.execute(Org_no=org_no,Year_No=year_no, Period=period, Account=account,Balance=balance, Quantity=quantity, SIETYP=file_type,
                                Dimension_no=dim_no, Obj_no=obj_no, Sub_Dim_no=Sub_Dim_no, Sub_Obj_no=Sub_Obj_no )
                    print("periodEndBalanceWithoutDimObjData data added in the database")
                except sqlalchemy.exc.IntegrityError:
                    print "psaldo"
                

            else:
                org_no = org_num
                file_type = SIETYP
                year_no = int(split[i + 1])
                period = int(split[i + 2])
                account = int(split[i + 3])
                balance = float(split[i + 5])
                dim_no = ""
                obj_no = ""
                Sub_Dim_no = ""
                Sub_Obj_no = ""
                # check quantity field present or not
                if ("#" not in split[i + 6]) and ('' not in split[i + 6]):
                    quantity = int(split[i + 6])
                else:
                    quantity = 0
                # fields stored into the table
                # print(org_no,file_type,year_no,period,account,balance,quantity)
                try:
                    # print(org_no, file_type, year_no, period, account, balance, quantity, dim_no, obj_no, Sub_Dim_no,
                    #       Sub_Obj_no)
                    ins.execute(Org_no=org_no, Year_No=year_no, Period=period, Account=account, Balance=balance,
                                Quantity=quantity, SIETYP=file_type,Dimension_no=dim_no, Obj_no=obj_no, Sub_Dim_no=Sub_Dim_no, Sub_Obj_no=Sub_Obj_no)
                    print("periodEndBalanceWithoutDimObjData data added in the database")
                except sqlalchemy.exc.IntegrityError:
                    print "psaldo1"
                

# stored all the data for tag "#PSALDO" which does not contain object and dimension field
# def periodEndBalanceWithoutDimObjData(split, metadata, org_num, SIETYP):
#     db_obj = Table('Period_End_Balance_without_Dim_Obj(#PSALDO)', metadata, autoload=True)
#     ins = db_obj.insert()
#
#     for i in range(0, len(split)):
#         # check for #PSALDO tag in the .SE file or response from API
#         if (split[i] == "#PSALDO" and (split[i + 4])== "{}"):
#             org_no = org_num
#             file_type = SIETYP
#             year_no = int(split[i + 1])
#             period = int(split[i + 2])
#             account = int(split[i + 3])
#             balance = float(split[i + 5])
#             # check quantity field present or not
#             if ("#" not in split[i + 6]) and ('' not in split[i+6]):
#                 quantity = int(split[i + 6])
#             else:
#                 quantity = 0
#             # fields stored into the table
#             #print(org_no,file_type,year_no,period,account,balance,quantity)
#             try:
#                 ins.execute(Org_no=org_no,Year_No=year_no, Period=period, Account=account,
#                         Balance=balance, Quantity=quantity,SIETYP=file_type)
#             except sqlalchemy.exc.IntegrityError :
#                 print "psaldo1"

# stored all the data for tag "#PBUDGET" which contain object and dimension field
def periodEndBudgetWithoutDimObjData(split, metadata, org_num, SIETYP):
    db_obj = Table('Period_budget_item(#PBUDGET)', metadata, autoload=True)
    ins = db_obj.insert()

    for i in range(0, len(split)):
        # check for #PBUDGET tag in the .SE file or response from API
        if (split[i] == "#PBUDGET"):
            print("Inside #PBUDGET")
            if ((split[i + 4]) != "{}"):
                org_no = org_num
                file_type = SIETYP
                year_no = int(split[i + 1])
                period = int(split[i + 2])
                account = int(split[i + 3])
                dim_no = (split[i + 4]).replace('"', "").replace('{', "").replace('\r', "")
                obj_no = (split[i + 5]).replace('"', "").replace('}', "").replace('\r', "")
                Sub_Dim_no = ""
                Sub_Obj_no = ""
                k = 5
                count = 0

                for j in range(k, len(split)):
                    if ((split[i + k + 1] == "}") or ("}" in split[i + k])):
                        if (("}" in split[i + k])):
                            k = k + 1
                            break
                        else:
                            k = k + 2
                            break
                    else:
                        if (count != 1):
                            Sub_Dim_no = (split[i + k + 1]).replace('"', "").replace('}', "").replace('\r', "")
                            if ("}" in split[i + k + 1]):
                                Sub_Obj_no = (split[i + k + 2]).replace('"', "").replace('}', "").replace('\r', "")
                                k = k + 1
                                break
                            else:
                                Sub_Obj_no = (split[i + k + 2]).replace('"', "").replace('}', "").replace('\r', "")
                                k = k + 2
                                count = count + 1
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
                    # print(org_no, file_type, year_no, period, account, dim_no, obj_no, Sub_Dim_no, Sub_Obj_no, balance,
                    #       quantity)
                    ins.execute(Org_no=org_no, Year_No=year_no, Period=period, Account=account, Balance=balance,
                                Quantity=quantity, SIETYP=file_type, Dimension_no=dim_no, Obj_no=obj_no,
                                Sub_Dim_no=Sub_Dim_no, Sub_Obj_no=Sub_Obj_no)
                    print("periodEndBudgetWithoutDimObjData data added in the database")
                except sqlalchemy.exc.IntegrityError:
                    print "Period_budget_item_with_dim_obj"
                

            else:
                org_no = org_num
                file_type = SIETYP
                year_no = int(split[i + 1])
                period = int(split[i + 2])
                account = int(split[i + 3])
                balance = float(split[i + 5])
                dim_no = ""
                obj_no = ""
                Sub_Dim_no = ""
                Sub_Obj_no = ""
                # check quantity field present or not

                if ("#" not in split[i + 6]) and ('' not in split[i + 6]):
                    quantity = int(split[i + 6])
                else:
                    quantity = 0
                # fields stored into the table
                try:
                    # print(org_no, file_type, year_no, period, account, dim_no, obj_no, Sub_Dim_no, Sub_Obj_no, balance,
                    #       quantity)
                    ins.execute(Org_no=org_no, Year_No=year_no, Period=period, Account=account, Balance=balance,
                                Quantity=quantity, SIETYP=file_type, Dimension_no=dim_no, Obj_no=obj_no,
                                Sub_Dim_no=Sub_Dim_no, Sub_Obj_no=Sub_Obj_no)
                    print("periodEndBudgetWithoutDimObjData data added in the database")
                except sqlalchemy.exc.IntegrityError:
                    print "Period_budget_item_without_dim_obj"

# stored all the data for tag "#PBUDGET" which does not contain object and dimension field
# def periodEndBudgetWithoutDimObjData(split, metadata, org_num, SIETYP):
#     db_obj = Table('Period_budget_item_without_dim_obj(#PBUDGET)', metadata, autoload=True)
#     ins = db_obj.insert()
#
#     for i in range(0, len(split)):
#         # check for #PBUDGET tag in the .SE file or response from API
#         if (split[i] == "#PBUDGET" and (split[i + 4])== "{}"):
#             org_no = org_num
#             file_type = SIETYP
#             year_no = int(split[i + 1])
#             period = int(split[i + 2])
#             account = int(split[i + 3])
#             balance = float(split[i + 5])
#             # check quantity field present or not
#
#             if ("#" not in split[i + 6]) and ('' not in split[i+6]):
#                 quantity = int(split[i + 6])
#             else:
#                 quantity = 0
#             # fields stored into the table
#             try:
#                 ins.execute(Org_no=org_no, Year_No=year_no, Period=period, Account=account,
#                         Balance=balance, Quantity=quantity, SIETYP=file_type)
#             except sqlalchemy.exc.IntegrityError :
#                 print "Period_budget_item_without_dim_obj"



def subDimensionData(split, metadata, org_num, SIETYP):
    db_obj = Table('Sub_Dimension(#UNDERDIM)', metadata, autoload=True)
    ins = db_obj.insert()

    for i in range(0, len(split)):
        # check for #PSALDO tag in the .SE file or response from API
        if (split[i] == "#UNDERDIM"):
            print("Inside #UNDERDIM")
            org_no = org_num
            file_type = SIETYP
            sub_dim_no = split[i+1]
            sub_dim_name = split[i+2]
            head_dim_no = split[i+3]

            try:
                ins.execute(Org_no=org_no, SIETYP=file_type, Sub_Dim_no=sub_dim_no, Sub_Dim_name=sub_dim_name, Head_Dim_no=head_dim_no)
                print("subDimensionData data added in the database")
            except sqlalchemy.exc.IntegrityError:
                print "subDimensionData"
from sqlalchemy import *
import sqlalchemy
from time import gmtime, strftime
#import fileAutomation

# stored all the Header data into the databse
def headerData(split, metadata, org_no, SIETYP):
    print("Inside header data")
    db_obj = Table('Header_test', metadata, autoload=True)
    ins = db_obj.insert()

    # if any value not present in the file then stored None value in DB
    file_type = 0
    export_software = " "
    file_gen = 0
    comment = " "
    c_id = " "
    c_name = " "
    c_type = " "
    Org_no = " "
    adress = " "
    acc_type = " "
    currency = " "
    b_date = 0

    # traverse complete file to identify each tag in the Header
    for i in range(0, len(split)):
        if (split[i] == "#SIETYP"):
            file_type = SIETYP


        if (split[i] == "#PROGRAM"):
            export_software = "".replace('\r',"")
            for j in range(i+1, len(split)):
                if "#" not in split[j]:
                    export_software = (export_software+split[j]+" ").replace('"',"")
                else:
                    break



        if (split[i] == "#GEN"):
            file_gen = split[i + 1].replace('\r',"")


        comment = " "
        if (split[i] == "#PROSA"):
            comment = "".replace('\r',"")
            for j in range(i + 1, len(split)):
                if "#" not in split[j]:
                    comment = (comment + split[j] + " ").replace('"',"")
                else:
                    break



        if (split[i] == "#FNR"):
            c_id = "".replace('\r',"")
            for j in range(i + 1, len(split)):
                if "#" not in split[j]:
                    c_id = (c_id + split[j] + " ").replace('"',"")
                else:
                    break



        if (split[i] == "#FNAMN"):
            c_name = "".replace('\r',"")
            for j in range(i + 1, len(split)):
                if "#" not in split[j]:
                    c_name = (c_name + split[j] + " ").replace('"',"")
                else:
                    break


        #c_type = None
        if (split[i] == "#FTYP"):
            c_type = "".replace('\r',"")
            for j in range(i + 1, len(split)):
                if "#" not in split[j]:
                    c_type = (c_type + split[j] + " ").replace('"',"")
                else:
                    break



        if (split[i] == "#ORGNR"):
            Org_no = org_no


        if (split[i] == "#ADRESS"):
            #print split[i]
            adress = "".replace('\r',"")
            for j in range(i + 1, len(split)):
                if "#" not in split[j]:
                    adress = (adress + split[j] + " ").replace('"',"")
                    #print adress
                else:
                    break




        if (split[i] == "#OMFATTN"):
            b_date = split[i + 1].replace('\r',"")


        if (split[i] == "#KPTYP"):
            acc_type = "".replace('\r',"")
            for j in range(i + 1, len(split)):
                if "#" not in split[j]:
                    acc_type = (acc_type + split[j] + " ").replace('"',"")
                else:
                    break


        if (split[i] == "#VALUTA"):
            currency = "".replace('\r',"")
            for j in range(i + 1, len(split)):
                if "#" not in split[j]:
                    currency = (currency + split[j] + " ").replace('"',"")
                else:
                    break

    #Stored all the fileds in the table
    try:
        currentDT = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        print(file_type, export_software, file_gen, comment, adress, b_date, acc_type, currency, Org_no, currentDT)
        ins.execute(SIETYP=file_type, Export_software=export_software, File_generated=file_gen,
            Comment=comment, Company_id=c_id, Company_name=c_name, Company_type=c_type,
            Org_no=Org_no, Comapany_address=adress, Balance_date=b_date,
            Account_type=acc_type, Currency=currency,Data_modified_date_time= currentDT)
    except Exception as e:
        print(e)
        print "Header"
    print "Header data added in the database"

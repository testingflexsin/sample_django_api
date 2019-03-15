from sqlalchemy import *
import sqlalchemy

def verTransData(split, metadata, org_num, SIETYP):
    db_obj = Table('Verification_Transaction(#VER/#TRANS)', metadata, autoload=True)
    ins = db_obj.insert()

    for i in range(0, len(split)):

        if (split[i] == "#VER"):
            print("inside #VER")
            org_no = org_num
            file_type=SIETYP
            series = split[i+1]
            ver_no = int(split[i+2].replace('"', ""))
            ver_date = int(split[i+3])
            ver_text = split[i+4].replace('"', "")+" "
            temp_j = 0

            if ( split[i + 6] )=='{':
                ver_text = (split[i + 4].replace('"', "")).replace('-', "")
                #print "testeddd"
                temp_j = i + 4
                #break
            else:
                for j in range(i + 5, len(split)):
                    if (('"' in split[j]) and split[j+2] == '{'):
                        ver_text = (ver_text + split[j] + " ").replace('"', "")
                        temp_j = j
                        break
                        #print ver_text
                    else:
                        ver_text = (ver_text + split[j] + " ").replace('"', "")

            reg_date = split[temp_j+1]
            #sign = split[temp_j+2].replace('"', "")
            sign = " "
            for j in range(temp_j+2, len(split)):
                if "{" not in split[j]:
                    sign = ((sign + split[j] + " ").replace('"', "")).replace('-', "")
                else:
                    break


            for j in range(temp_j + 2, len(split)):
                if (split[j] == "#TRANS"):
                    print("inside #TRANS")
                    acc_num = int(split[j + 1])
                    if (split[j + 2] == '{}'):
                        obj_list = split[j + 2]
                        amount = float(split[j + 3])
                        #print amount
                        if ((((split[j + 4]).replace('"', '')) == '') or ('}' in split[j + 5]) or ('}' in split[j + 4])):
                            transdate = ver_date
                        else:
                            #print split[j+4]
                            transdate = int(split[j + 4])
                            #print transdate
                        transtext = " "
                        for k in range(j+5, len(split)):
                            if (("#" not in split[k]) and ("}" not in split[k])):
                                transtext = ((transtext + split[k] + " "))
                                temp_num = k
                            else:
                                break
                    else:
                        k = 2
                        obj_list = ""
                        for l in range(k, len(split)):
                            if (("}" in split[j + l]) or (split[j + l] == "}")):
                                if ("}" in split[j + l]):
                                    obj_list = obj_list + split[j + l]
                                    k = k + l - 1
                                    break
                                else:
                                    k = k + l
                                    break
                            else:
                                obj_list = obj_list + split[j + l].replace("}", "") + " "

                        amount = float(split[j + k])

                        # print split[j + 5]
                        if ((((split[j + k + 1]).replace('"', '')) == '') or ('}' in split[j + k + 2]) or (
                            '}' in split[j + k + 1])):
                            transdate = ver_date
                        else:
                            transdate = int(split[j + k + 1])
                        transtext = " "
                        for m in range(j + k + 2, len(split)):
                            if (("#" not in split[m]) and ("}" not in split[k])):
                                transtext = (transtext + split[m] + " ")
                                temp_num = m
                            else:
                                break

                    transtext = transtext.partition('"')[-1].rpartition('"')[0]
                    #print(org_no, series, ver_no, ver_date, ver_text, reg_date, sign, acc_num, obj_list,amount,transdate,transtext)
                    try:
                        ins.execute(Org_no=org_no, Series=series, Verification_no=ver_no, Verification_date=ver_date,
                            Verification_text=ver_text,Registration_date=reg_date,Sign=sign,Account_no=acc_num,
                            Object_list=obj_list,Amount=amount,Transaction_date=transdate,Transaction_text=transtext, SIETYP=file_type)
                        print("added verTransData data")
                    except sqlalchemy.exc.IntegrityError:
                        print("in except")
                if (split[j] == '}'):
                    break
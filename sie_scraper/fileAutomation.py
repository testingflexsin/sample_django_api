import dropbox
import codecs
from sqlalchemy import *
from random import randint
from sieFileParser import execute
import traceback
from Email import sendEmail
import threading

# gloabal variable which stored the executing filename and modified date
fileName = ""
mod_date = ""

def automate():
    #Dropbox Access Token
    Access_token = "bxF9lwCOxeAAAAAAAAAAGh3cYRIUEJjuhBEY2fxHQx7AdvaypVYN8K9c4rgQhbtA"

    #client object for dropbox
    client = dropbox.client.DropboxClient(Access_token)

    # DB connection URL form with "postgresql://userid:password@Hostname:port_number/dbName"
    db = create_engine("postgresql://fortnoxDB:14kdvKsI7IfeFfwn@35.195.0.180/postgres")
    metadata = MetaData(db)
    #create object of table
    db_obj = Table('File_history', metadata, autoload=True)
    ins_insert = db_obj.insert()

    #stored all the files information inside "/Enhanza-SIE/"
    folder_metadata = client.metadata('/Enhanza/')
    #Total file count in the parent folder i.e. (/Enhanza-SIE/)
    Total_folder = len(folder_metadata["contents"])

    # Traverse each folder in the parent folder
    for i in range(0,Total_folder):

        folder_files = client.metadata(folder_metadata["contents"][i]["path"])
        Total_folder_files = len(folder_files["contents"])
        # Traverse each file inside sub-folder of parent folder
        for j in range(0,Total_folder_files):
            file_name = folder_files["contents"][j]["path"]
            #file_name = file_name.encode('cp437')
            global fileName, mod_date
            fileName = file_name
            modified_date = folder_files["contents"][j]["modified"]
            mod_date = modified_date
            ins_select = db_obj.select().where(and_(db_obj.c.File_name == file_name,
                                                db_obj.c.Modified_date == modified_date))

            # check file is not present in the database
            if(len(ins_select.execute().fetchall()) == 0):
                f, metadata = client.get_file_and_metadata(file_name)
                random_no = randint(0,100)
                #read file from dropbox and stord into local system
                output_file = "/home/ubuntu/se_files/"+str(random_no)+"downloaded.SE"
                out = open(output_file, 'wb')
                out.write(f.read())
                out.close()
                # execute funtion read the content from the file and stored into the databse
                print "calling execute statement"
                execute(output_file,file_name)
                #stored the filename and modified date into the database
                ins_insert.execute(File_name=folder_files["contents"][j]["path"],Modified_date=folder_files["contents"][j]["modified"])



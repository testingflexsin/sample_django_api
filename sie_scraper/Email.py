import smtplib
import codecs
server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
#Next, log in to the server

def sendEmail(msg):
    #takes one argument message ie. get attached to the body of mail
    #specify username, password and (TO) recipient address
    FROM = 'mayur.dhote@rudderanalytics.com'
    psswd = 'mmmqwe@123'
    TO = ["mayur.dhote@rudderanalytics.com"]
    server.login(FROM, psswd)
    #specify subject for the mail
    SUBJECT = "SIE DATA ETL ERROR"
    #BODY = codecs.decode(msg, 'cp437')
    TEXT = msg

    #Prepare actual message
    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)

    #Send the mail
    server.sendmail(FROM, TO, message)
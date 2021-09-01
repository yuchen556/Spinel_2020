import ssl
import smtplib

def mail_sending():
    # 发送邮件开始
    smtp_server = 'smtp.sina.com'
    port = 465
    sender = 'yuchen556@sina.com'
    # password = input('Enter your password here: ')
    receiver = "556wangzhen@163.com"
    # receiver = 'zhen.wang@joinus-tech.com'
    message = "Subject: Passed_Spinel_Test_{}!\r\nThis message was sent from Python!\r\nFrom: {}\r\nTo: {}".format("spinel_sn", sender, receiver)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender, 'cd443ab65c8e8431')
        print("Passed, mailed!")
        server.sendmail(sender, receiver, message)
    # 发送邮件结束

mail_sending()
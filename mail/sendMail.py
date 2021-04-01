# -*- codeing = utf-8 -*-
# @Time : 2021/4/1 10:27
# @Author : 水印红枫
# @Software: PyCharm

from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

host_server = 'smtp.qq.com'
send_mail = '2294211995@qq.com'
pwd = "ijaqieveffeqdjij"

receiver_mail = '18860360510@163.com'

mail_title = 'python发送'
mail_content = '<p>标题</p>' \
               '<div>内容</div>'

msg = MIMEMultipart()
msg["Subject"] = Header(mail_title, 'utf-8')
msg['From'] = send_mail
msg['To'] = Header("测试邮箱", 'utf-8')
msg.attach(MIMEText(mail_content, 'html', 'utf-8'))

try:
    smtp = SMTP_SSL(host_server)
    smtp.ehlo(host_server)
    smtp.login(send_mail, pwd)
    smtp.sendmail(send_mail, receiver_mail, msg.as_string())
    smtp.quit()
    print("发送成功")
except Exception as error:
    print(error)


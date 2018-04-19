# 人丑就要多学习
def send_email(msg_from, sqm, msg_to, content):
    import smtplib
    from email.mime.text import MIMEText
    # 发送方邮箱
    # msg_from = '616169921@qq.com'
    msg_from = msg_from
    # 密码,这里获取的 客户端授权码,这里的每个管理着的授权码是不一样的
    # passwd = 'efvgaelwdsaybdae'
    passwd = sqm
    # 收件人
    # msg_to = '923103984@qq.com'
    msg_to = msg_to
    # 设置邮件主题
    subject = '若谷集团发送邮件'
    # 正题
    content = content
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to

    # 发送邮件
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print("发送成功")
        return "发送成功"

    except:
        print("发送失败")
        return "发送失败"

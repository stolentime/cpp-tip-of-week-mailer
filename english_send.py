import json
import random
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def main():
    # 1. 读取英语短句库
    with open('english_tips.json', 'r', encoding='utf-8') as f:
        tips = json.load(f)

    tip = random.choice(tips)

    # 2. 获取环境变量
    sender_email = os.environ['EMAIL_USER']
    receiver_emails = [email.strip() for email in os.environ['RECIPIENT_EMAILS'].split(',')]
    password = os.environ['EMAIL_APP_PASSWORD']

    # 3. 创建邮件
    message = MIMEMultipart("alternative")
    message["Subject"] = f"📘 每日英语一句 #{tip['id']}"
    message["From"] = sender_email
    message["To"] = ', '.join(receiver_emails)

    # 4. 纯文本版本（简洁）
    text = f"""
每日英语一句 #{tip['id']}:

{tip['sentence']}
— {tip['translation']}

📝 {tip.get('note', '')}
"""

    # 5. HTML 版本（美观）
    html = f"""
    <html>
      <body>
        <h2>📘 每日英语一句 #{tip['id']}</h2>
        <p><b>{tip['sentence']}</b></p>
        <p><i>{tip['translation']}</i></p>
        <hr>
        <p><small>📝 {tip.get('note', '')}</small></p>
      </body>
    </html>
    """

    # 6. 添加两个版本（邮件客户端会自动选最佳显示）
    message.attach(MIMEText(text, "plain"))
    message.attach(MIMEText(html, "html"))

    # 7. 发送邮件
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_emails, message.as_string())

    print(f"✅ 邮件已发送：英语短句 #{tip['id']}")

if __name__ == "__main__":
    main()
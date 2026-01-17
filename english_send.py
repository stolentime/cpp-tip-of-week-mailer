# send_tip.py
import json
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def main():
    # 读取 Tips
    with open('english_tips.json', 'r', encoding='utf-8') as f:
        tips = json.load(f)

    tip = random.choice(tips)

    # 邮件配置
    sender_email = os.environ['EMAIL_USER']
    receiver_emails = [email.strip() for email in os.environ['RECIPIENT_EMAIL'].split(',')]
    password = os.environ['EMAIL_APP_PASSWORD']

    # 创建邮件
    message = MIMEMultipart("alternative")
    message["Subject"] = f"📘 每日英语一句 #{tip['id']}"
    #message["Subject"] = f"📚 C++ Tip of the Week #{tip['id']}: {tip['title']}"
    message["From"] = sender_email
    message["To"] = ', '.join(receiver_emails)

    # 纯文本版本
    text = f"""
Hi!

Here's your weekly C++ tip from Google's "Tips of the Week" series:

📌 Tip #{tip['id']}: {tip['title']}
📅 Published: {tip['date']}
🔗 Read full tip: {tip['url']}

Happy coding!
— Your C++ Learning Bot
    """

    # HTML 版本（可选，更美观）
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

    # 添加两个版本
    message.attach(MIMEText(text, "plain"))
    message.attach(MIMEText(html, "html"))

    # 发送邮件
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_emails, message.as_string())

    print(f"✅ Email sent: Tip #{tip['id']}")

if __name__ == "__main__":
    main()
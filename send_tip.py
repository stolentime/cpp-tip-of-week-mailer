# send_tip.py
import json
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def main():
    # 读取 Tips
    with open('tips.json', 'r', encoding='utf-8') as f:
        tips = json.load(f)

    tip = random.choice(tips)

    # 邮件配置
    sender_email = os.environ['EMAIL_USER']
    receiver_email = os.environ['RECIPIENT_EMAIL']
    password = os.environ['EMAIL_APP_PASSWORD']

    # 创建邮件
    message = MIMEMultipart("alternative")
    message["Subject"] = f"📚 C++ Tip of the Week #{tip['id']}: {tip['title']}"
    message["From"] = sender_email
    message["To"] = receiver_email

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
        <h2>📚 C++ Tip of the Week</h2>
        <p>Hi!</p>
        <p>Here's your weekly C++ tip from Google's <em>"Tips of the Week"</em> series:</p>
        <div style="background:#f5f5f5; padding:15px; border-left:4px solid #4CAF50; margin:20px 0;">
          <h3>📌 Tip #{tip['id']}: {tip['title']}</h3>
          <p><strong>📅 Published:</strong> {tip['date']}</p>
          <p><a href="{tip['url']}" style="color:#1a73e8;">🔗 Read the full tip on Abseil.io</a></p>
        </div>
        <p>Happy coding!<br>— Your C++ Learning Bot</p>
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
        server.sendmail(sender_email, receiver_email, message.as_string())

    print(f"✅ Email sent: Tip #{tip['id']}")

if __name__ == "__main__":
    main()
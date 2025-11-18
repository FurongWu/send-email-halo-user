import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import time
import ssl

def read_config(config_file_path="email_config.txt"):
    """
    从配置文件读取所有配置
    """
    try:
        config = {}
        with open(config_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    config[key] = value
        return config
    except Exception as e:
        print(f"读取配置文件时出错: {e}")
        return None

def read_emails_from_file(filename="emails.txt"):
    """
    从文件读取邮箱列表，一行一个地址
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            emails = [line.strip() for line in f if line.strip()]
        return emails
    except Exception as e:
        print(f"读取邮箱文件时出错: {e}")
        return []

def read_content_from_file(filename):
    """
    从文件读取邮件内容
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        print(f"读取邮件内容文件时出错: {e}")
        return None

def send_email(sender_email, sender_password, recipient_email, subject, content, smtp_server="smtp.rongtech.top", smtp_port=25):
    """
    发送邮件给单个收件人
    """
    try:
        # 创建邮件对象
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = Header(subject, 'utf-8')
        
        # 添加邮件正文
        msg.attach(MIMEText(content, 'plain', 'utf-8'))
        
        # 创建安全上下文 - 禁用证书验证
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        # 连接SMTP服务器并发送邮件
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # 尝试使用STARTTLS
            server.starttls(context=context)
            
            # 登录邮箱
            server.login(sender_email, sender_password)
            
            # 发送邮件
            server.sendmail(sender_email, recipient_email, msg.as_string())
            
        print(f"成功发送邮件给 {recipient_email}")
        return True
        
    except Exception as e:
        print(f"发送邮件给 {recipient_email} 时出错: {e}")
        return False

def main():
    # 读取配置
    config = read_config()
    if not config:
        print("无法读取配置文件，请检查 email_config.txt 文件")
        return
    
    # 检查必要配置项
    required_keys = ['sender_email', 'sender_password', 'subject', 'content_file']
    for key in required_keys:
        if key not in config:
            print(f"配置文件中缺少必要的配置项: {key}")
            return
    
    # 读取邮件内容
    content = read_content_from_file(config['content_file'])
    if content is None:
        print("无法读取邮件内容文件")
        return
    
    # 读取收件人邮箱列表
    recipient_emails = read_emails_from_file("emails.txt")
    if not recipient_emails:
        print("未找到收件人邮箱列表，请确保 emails.txt 文件存在且包含邮箱地址")
        return
    
    # 获取SMTP配置
    smtp_server = config.get('smtp_server', 'smtp.rongtech.top')
    smtp_port = int(config.get('smtp_port', 25))
    
    print(f"找到 {len(recipient_emails)} 个收件人邮箱")
    print(f"邮件主题: {config['subject']}")
    print(f"SMTP服务器: {smtp_server}:{smtp_port}")
    print("开始发送邮件...")
    
    # 逐个发送邮件给每个收件人
    successful_emails = 0
    total_emails = len(recipient_emails)
    
    for i, recipient_email in enumerate(recipient_emails, 1):
        print(f"发送第 {i}/{total_emails} 封邮件给: {recipient_email}")
        
        success = send_email(
            sender_email=config["sender_email"],
            sender_password=config["sender_password"],
            recipient_email=recipient_email,
            subject=config["subject"],
            content=content,
            smtp_server=smtp_server,
            smtp_port=smtp_port
        )
        
        if success:
            successful_emails += 1
            print(f"第 {i} 封邮件发送成功")
        else:
            print(f"第 {i} 封邮件发送失败")
        
        # 添加延迟，避免发送过快被限制
        if i < total_emails:  # 如果不是最后一封邮件
            time.sleep(2)
    
    print(f"\n邮件发送任务完成，成功发送 {successful_emails}/{total_emails} 封邮件")

if __name__ == "__main__":
    main()

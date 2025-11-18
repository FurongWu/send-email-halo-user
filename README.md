# send-email-halo-user
给halo用户发送邮件,单发邮件，每个用户一封，邮件内容相同。邮件服务器不加密
##确保以下文件在同一目录下：
send_email.py- 发送邮件脚本
get-all-emails.py - 获取所有用户的邮箱地址
token.txt halo的api认证令牌
email_config.txt- 邮件配置
email_content.txt- 邮件内容
emails.txt- 收件人列表（每行一个邮箱地址）,允许get-all-email.py获取
##运行步骤
0、删除emails.txt文件
1、先在Halo后台获取到自己的api令牌放入token.txt文件中
2、填写email_config.txt- 邮件配置、email_content.txt- 邮件内容
3、修改get-all-emails.py中url成你自己的网站域名
4、运行get-all-emails.py获取所有用户邮箱地址，会自动写入当前目录下的emails.txt文件中
5、运行send_email.py- 发送邮件

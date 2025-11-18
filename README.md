# send-email-halo-user
给halo用户发送邮件,单发邮件，每个用户一封，邮件内容相同。邮件服务器不加密
## 确保以下文件在同一目录下：
<br>
token.txt halo的api认证令牌<br>
get-all-emails.py - 获取所有用户的邮箱地址<br>
emails.txt- 收件人列表（每行一个邮箱地址）,运行get-all-email.py获取<br>
email_config.txt- 邮件配置<br>
email_content.txt- 邮件内容<br>
send_email.py- 发送邮件脚本<br>

## 运行步骤
<br>
先将项目下载到本地，配置好python环境
<br>
1、删除emails.txt文件<br>
2、先在Halo后台获取到自己的api令牌放入token.txt文件中<br>
3、填写email_config.txt- 邮件配置、email_content.txt- 邮件内容<br>
4、修改get-all-emails.py中url成你自己的网站域名<br>
5、运行get-all-emails.py获取所有用户邮箱地址，会自动写入当前目录下的emails.txt文件中<br>
6、运行send_email.py- 发送邮件<br>

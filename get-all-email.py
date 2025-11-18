import requests
import time

def read_token_from_file(file_path):
    """
    从文本文件中读取 Bearer Token
    """
    try:
        with open(file_path, 'r') as file:
            token = file.read().strip()  # 读取并去除首尾空白字符
        return token
    except FileNotFoundError:
        print(f"错误：找不到文件 {file_path}")
        return None
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return None

def get_all_emails(base_url, token_file_path, delay=0.1):
    """
    获取所有用户的 email 地址
    """
    # 从文件读取 Token
    token = read_token_from_file(token_file_path)
    if token is None:
        return []
    
    # 设置请求头
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {token}'
    }
    
    all_emails = []
    page = 1
    size = 20  # 每页大小，可以根据需要调整
    
    while True:
        # 构建请求URL，添加分页参数
        url = f"{base_url}?page={page}&size={size}"
        
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code != 200:
                print(f"请求失败，状态码: {response.status_code}")
                break
                
            data = response.json()
            
            # 提取当前页的所有 email
            for user in data["items"]:
                email = user["spec"]["email"]
                all_emails.append(email)
                print(f"找到 email: {email}")
            
            # 检查是否还有下一页
            if data.get("last", False) or page >= data.get("totalPages", page):
                break
                
            page += 1
            
            # 添加延迟避免请求过快
            time.sleep(delay)
            
        except Exception as e:
            print(f"处理第 {page} 页时出错: {e}")
            break
    
    return all_emails

# 使用示例
if __name__ == "__main__":
    # API 配置
    base_url = "https://rongtech.top/api/v1alpha1/users"  # 请确认这是正确的用户API端点
    token_file_path = "token.txt"  # 存储 Token 的文件路径
    
    # 获取所有 email
    all_emails = get_all_emails(base_url, token_file_path)
    
    print(f"\n总共找到 {len(all_emails)} 个 email 地址:")
    for email in all_emails:
        print(email)
    
    # 可选：将结果保存到文件
    if all_emails:
        with open("emails.txt", "w") as f:
            for email in all_emails:
                f.write(email + "\n")
        print(f"\n结果已保存到 emails.txt 文件")

#!/usr/bin/env python3
"""
测试Server酱消息发送
"""

import requests
from datetime import datetime, date
import os

# 从环境变量或直接设置SendKey
SERVERCHAN_SENDKEY = os.environ.get('SERVERCHAN_SENDKEY', '')

if not SERVERCHAN_SENDKEY:
    print("错误：未配置 SERVERCHAN_SENDKEY")
    print("\n请按以下方式配置：")
    print("方式1: export SERVERCHAN_SENDKEY='你的SendKey'")
    print("方式2: 在此脚本中直接设置 SERVERCHAN_SENDKEY 变量")
    exit(1)

def test_send():
    """发送测试消息"""
    today = date.today()
    weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    
    title = "📈 A股开盘提醒 - 测试消息"
    desp = f"""### 📈 A股开盘提醒

这是一条测试消息，如果你收到此消息，说明配置成功！

---

**测试信息：**
- 发送时间：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}
- 日期：{today.strftime('%Y年%m月%d日')}
- 星期：{weekday_names[today.weekday()]}

---

> 如果看到这条消息，说明Server酱配置正确~
"""
    
    url = f"https://sctapi.ftqq.com/{SERVERCHAN_SENDKEY}.send"
    data = {
        "title": title,
        "desp": desp
    }
    
    print(f"正在发送测试消息...")
    print(f"SendKey: {SERVERCHAN_SENDKEY[:8]}...{SERVERCHAN_SENDKEY[-4:]}")
    
    try:
        response = requests.post(url, data=data, timeout=10)
        result = response.json()
        
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应内容: {result}")
        
        if result.get('code') == 0:
            print("\n✅ 测试消息发送成功！请查看微信消息。")
        else:
            print(f"\n❌ 发送失败: {result.get('message', '未知错误')}")
    except Exception as e:
        print(f"\n❌ 请求出错: {e}")

if __name__ == "__main__":
    test_send()

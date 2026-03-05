#!/usr/bin/env python3
"""
A股开盘日提醒程序
在每个A股开盘日（周一至周五，排除法定节假日）发送提醒
"""

import schedule
import time
import requests
from datetime import datetime, date
from pathlib import Path
import os

# 配置信息 - Server酱
# 获取方式：https://sct.ftqq.com/ 登录后获取 SendKey
SERVERCHAN_SENDKEY = os.environ.get('SERVERCHAN_SENDKEY', 'SCT318726TCY3poDav82mT2yeYkAFp8YXR')  # Server酱 SendKey

# A股2026年已知的休市日期（需要根据实际情况更新）
# 包括春节、清明、五一、端午、中秋、国庆等假期
HOLIDAYS_2026 = {
    # 元旦
    date(2026, 1, 1), date(2026, 1, 2), date(2026, 1, 3),
    # 春节 (1月28日-2月4日)
    date(2026, 1, 28), date(2026, 1, 29), date(2026, 1, 30), date(2026, 1, 31),
    date(2026, 2, 1), date(2026, 2, 2), date(2026, 2, 3), date(2026, 2, 4),
    # 清明节 (4月4日-6日)
    date(2026, 4, 4), date(2026, 4, 5), date(2026, 4, 6),
    # 劳动节 (5月1日-5日)
    date(2026, 5, 1), date(2026, 5, 2), date(2026, 5, 3), date(2026, 5, 4), date(2026, 5, 5),
    # 端午节 (5月31日-6月2日)
    date(2026, 5, 31), date(2026, 6, 1), date(2026, 6, 2),
    # 中秋节+国庆节 (10月1日-7日)
    date(2026, 10, 1), date(2026, 10, 2), date(2026, 10, 3), date(2026, 10, 4),
    date(2026, 10, 5), date(2026, 10, 6), date(2026, 10, 7),
}

def is_trading_day(check_date: date = None) -> bool:
    """
    判断是否为A股交易日
    - 周一至周五
    - 非法定节假日
    """
    if check_date is None:
        check_date = date.today()
    
    # 周末不交易
    if check_date.weekday() >= 5:  # 5=周六, 6=周日
        return False
    
    # 节假日不交易
    if check_date in HOLIDAYS_2026:
        return False
    
    return True


def send_serverchan(title: str, content: str):
    """通过Server酱发送微信消息"""
    if not SERVERCHAN_SENDKEY:
        print("未配置Server酱 SendKey，跳过微信提醒")
        return False
    
    url = f"https://sctapi.ftqq.com/{SERVERCHAN_SENDKEY}.send"
    data = {
        "title": title,
        "desp": content
    }
    
    try:
        response = requests.post(url, data=data, timeout=10)
        result = response.json()
        if result.get('code') == 0:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Server酱消息发送成功")
            return True
        else:
            print(f"Server酱消息发送失败: {result}")
            return False
    except Exception as e:
        print(f"发送Server酱消息出错: {e}")
        return False


def send_notification():
    """发送提醒通知（桌面通知 + Server酱微信）"""
    today = date.today()
    weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    
    title = "📈 A股开盘提醒"
    message = f"今天是{weekday_names[today.weekday()]}，A股正常交易！记得查看行情~"
    
    # macOS 桌面通知
    os.system(f'''osascript -e 'display notification "{message}" with title "{title}"' ''')
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {title}: {message}")
    
    # 发送Server酱微信提醒
    desp = f"""### 📈 A股开盘提醒

{message}

---

**详细信息：**
- 日期：{today.strftime('%Y年%m月%d日')}
- 星期：{weekday_names[today.weekday()]}
- 状态：交易日

---

> 记得查看行情哦~"""
    send_serverchan(title, desp)


def check_and_remind():
    """检查是否为交易日并发送提醒"""
    if is_trading_day():
        send_notification()
    else:
        today = date.today()
        weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 今天是{weekday_names[today.weekday()]}，非交易日")


def main():
    print("=" * 50)
    print("A股开盘日提醒程序已启动")
    print("=" * 50)
    print("提醒方式：桌面通知 + Server酱微信推送")
    print("提醒时间：每个交易日 9:00 和 13:00")
    print("按 Ctrl+C 退出程序")
    print("=" * 50)
    print("\n配置说明：")
    print("1. 访问 https://sct.ftqq.com/ 获取 SendKey")
    print("2. 设置环境变量: export SERVERCHAN_SENDKEY='你的SendKey'")
    print("3. 或直接在代码中修改 SERVERCHAN_SENDKEY")
    print("=" * 50)
    
    # 设置提醒时间
    # 开盘前提醒
    schedule.every().day.at("09:00").do(check_and_remind)
    # 午盘前提醒
    schedule.every().day.at("13:00").do(check_and_remind)
    
    # 启动时立即检查一次
    check_and_remind()
    
    # 持续运行
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次


if __name__ == "__main__":
    main()

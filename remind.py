#!/usr/bin/env python3
"""
A股开盘日提醒程序 - GitHub Actions 版本
"""

import requests
from datetime import datetime, date
import os

# 配置信息
SERVERCHAN_SENDKEY = os.environ.get('SERVERCHAN_SENDKEY', '')

# A股2026年休市日期
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
    """判断是否为A股交易日"""
    if check_date is None:
        check_date = date.today()

    if check_date.weekday() >= 5:
        return False

    if check_date in HOLIDAYS_2026:
        return False

    return True


def send_serverchan(title: str, content: str):
    """通过Server酱发送微信消息"""
    if not SERVERCHAN_SENDKEY:
        print("未配置Server酱 SendKey")
        return False

    url = f"https://sctapi.ftqq.com/{SERVERCHAN_SENDKEY}.send"
    data = {"title": title, "desp": content}

    try:
        response = requests.post(url, data=data, timeout=10)
        result = response.json()
        if result.get('code') == 0:
            print(f"Server酱消息发送成功")
            return True
        else:
            print(f"Server酱消息发送失败: {result}")
            return False
    except Exception as e:
        print(f"发送消息出错: {e}")
        return False


def main():
    today = date.today()
    weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']

    print(f"检查日期: {today} ({weekday_names[today.weekday()]})")

    if not is_trading_day():
        print("非交易日，跳过提醒")
        return

    title = "📈 A股开盘提醒"
    message = f"今天是{weekday_names[today.weekday()]}，A股正常交易！记得查看行情~"

    desp = f"""### 📈 A股开盘提醒

{message}

---

**详细信息：**
- 日期：{today.strftime('%Y年%m月%d日')}
- 星期：{weekday_names[today.weekday()]}
- 状态：交易日

---

> 记得查看行情哦~"""

    print(f"发送提醒: {message}")
    send_serverchan(title, desp)


if __name__ == "__main__":
    main()

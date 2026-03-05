# A股开盘提醒程序

自动在每个A股交易日发送微信和桌面通知提醒。

## 功能特点

- 自动判断A股交易日（周一至周五，排除法定节假日）
- 支持桌面通知（macOS）
- 支持微信提醒（通过Server酱推送）
- 包含2026年A股休市日期

## 安装

```bash
pip install -r requirements.txt
```

## 配置 Server酱

### 1. 获取 SendKey

1. 访问 [Server酱官网](https://sct.ftqq.com/)
2. 使用微信扫码登录
3. 在「SendKey」页面复制你的 SendKey

### 2. 配置方式

**方式A：环境变量（推荐）**

```bash
export SERVERCHAN_SENDKEY="SCTxxxxxxxxxxxxxxxxxx"
```

**方式B：直接修改代码**

在 `stock_reminder.py` 中修改：

```python
SERVERCHAN_SENDKEY = "SCTxxxxxxxxxxxxxxxxxx"  # 替换为你的SendKey
```

## 运行

```bash
# 前台运行
python stock_reminder.py

# 后台运行
nohup python stock_reminder.py > reminder.log 2>&1 &
```

## 提醒时间

- 开盘前：9:00
- 午盘前：13:00

## 消息效果

Server酱会将消息推送到你的微信，格式如下：

```
📈 A股开盘提醒

今天是周一，A股正常交易！记得查看行情~

详细信息：
- 日期：2026年03月05日
- 星期：周四
- 状态：交易日
```

## 自定义

### 修改提醒时间

在 `main()` 函数中修改：

```python
schedule.every().day.at("09:00").do(check_and_remind)  # 开盘前
schedule.every().day.at("13:00").do(check_and_remind)  # 午盘前
schedule.every().day.at("14:30").do(check_and_remind)  # 尾盘前（可添加）
```

### 更新休市日期

在 `HOLIDAYS_2026` 中添加或修改日期。

## 注意事项

- 需要程序持续运行
- Server酱免费版每天限额5条消息（足够使用）
- 休市日期需根据证监会公告定期更新

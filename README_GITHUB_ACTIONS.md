# A股开盘提醒

自动在每个A股交易日发送微信提醒（通过 GitHub Actions + Server酱）

## 功能特点

- 完全免费，无需服务器
- 自动判断交易日（周一至周五，排除节假日）
- 微信推送提醒

## 部署步骤

### 1. 创建 GitHub 仓库

```bash
# 初始化 git
git init

# 添加文件
git add .

# 提交
git commit -m "初始化A股提醒程序"

# 关联远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/你的仓库名.git

# 推送
git push -u origin main
```

### 2. 配置 SendKey

1. 进入 GitHub 仓库页面
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. Name: `SERVERCHAN_SENDKEY`
5. Value: `SCT318726TCY3poDav82mT2yeYkAFp8YXR`
6. 点击 **Add secret**

### 3. 启用 Actions

1. 进入仓库的 **Actions** 页面
2. 如果提示启用，点击 **I understand my workflows, go ahead and enable them**

### 4. 测试运行

1. 进入 **Actions** 页面
2. 选择 **A股开盘提醒** workflow
3. 点击 **Run workflow** → **Run workflow**
4. 查看运行日志

## 提醒时间

- 开盘前：北京时间 9:00
- 午盘前：北京时间 13:00

## 注意事项

- GitHub Actions 使用 UTC 时间，已配置为对应的北京时间
- cron 表达式 `0 1 * * 1-5` 表示 UTC 1:00（北京时间 9:00），周一至周五
- 免费版 GitHub Actions 每月有 2000 分钟额度，足够使用

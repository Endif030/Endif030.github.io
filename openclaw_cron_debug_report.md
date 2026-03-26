# OpenClaw 定时任务调试完整报告

## 一、环境信息

| 项目 | 值 |
|------|-----|
| OpenClaw版本 | 2026.2.26 |
| 操作系统 | OpenCloudOS 9.4 |
| 内核版本 | 6.6.117-45.1.oc9.x86_64 |
| 时区 | Asia/Beijing (CST, +0800) |
| 调用模型 | kimi-coding/k2p5 |
| 腾讯云环境 | 轻量应用服务器 |
| Gateway状态 | local, reachable 35ms, PID 437637 |

## 二、调试过程

### 第一轮测试 - openclaw cron 命令

**测试1**: openclaw cron add --session isolated --announce --channel feishu
- 结果: 失败，消息未收到
- 任务ID: 20c8cacd-3802-4ca5-90c1-f6c0814963b3

**测试2**: 添加 --to 参数
- 结果: 失败，消息未收到
- 任务ID: 016191cf-984d-4a5b-a9ea-3dc2162c0827

**测试3**: 添加 --best-effort-deliver 参数
- 结果: 失败，消息未收到
- 任务ID: 23dba658-123d-4e42-8b3f-05363af50acd

发现: cron任务执行后从列表消失，但消息未投递

### 第二轮测试 - sessions_spawn 手动触发

**测试4**: openclaw sessions spawn --mode run --message
- 结果: 成功收到消息
- 结论: sessions_spawn 可以正常工作，openclaw cron 有bug

### 第三轮测试 - 系统crontab + sessions_spawn

**方案A测试1**: 系统crontab + 脚本调用 openclaw sessions spawn
- 脚本: /tmp/a_stock_report.sh
- 执行时间: 00:33
- 结果: 失败
- 错误: openclaw: command not found (PATH问题)

**方案A测试2**: 修正脚本使用完整路径
- openclaw路径: /root/.local/share/pnpm/openclaw
- 执行时间: 00:59
- 结果: 失败

**方案A测试3**: 简单提醒测试
- 内容: 0000088888
- 执行时间: 01:05
- 结果: 失败

## 三、关键发现

1. openclaw cron 命令存在bug: 无论怎么配置都无法发送消息
2. sessions_spawn 手动触发正常: 可以成功发送消息
3. 系统crontab执行了但消息未收到: 任务在cron日志中显示执行，但消息未投递
4. openclaw cron 参数兼容性问题:
   - --post-to-main: 参数不存在
   - --deliver: 已废弃，建议用 --announce
   - --announce: 投递机制失效

## 四、配置文件

~/.openclaw/config.yaml:
devices:
  autoApprove:
    - "cli:*"

~/.openclaw/devices/paired.json:
- CLI设备已批准
- 无待审批设备

## 五、最终测试脚本

#!/bin/bash
export HOME=/root
export PATH=/root/.nvm/versions/node/v22.22.0/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
cd /root/.openclaw/workspace
/root/.local/share/pnpm/openclaw sessions spawn --mode run --message "请使用 message 工具发送：[内容]"

## 六、问题总结

- Gateway运行正常
- 自动批准配置生效
- sessions_spawn 手动执行成功
- openclaw cron 命令有bug
- 系统crontab + sessions_spawn 组合未成功

## 七、建议

1. 检查 crontab 环境变量是否正确传递
2. 检查 sessions spawn 在cron环境中是否有权限问题
3. 考虑使用其他定时方案或等待OpenClaw修复

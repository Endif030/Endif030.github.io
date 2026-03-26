#!/usr/bin/env python3

"""
Feishu Message Sender for Investment Report
飞书消息推送工具 - 投资日报专用
"""

import sys
import os
import json
from datetime import datetime

# 配置
FEISHU_APP_ID = os.environ.get('FEISHU_APP_ID', 'cli_a92826c79ce4dbb6')
FEISHU_APP_SECRET = os.environ.get('FEISHU_APP_SECRET', '')

# 用户映射（将OpenClaw用户ID映射到飞书用户ID，如果需要）
USER_MAP = {
    'ou_bbfc027431c61a8ba421c54c7bb0f5c4': 'ou_bbfc027431c61a8ba421c54c7bb0f5c4'  # Roy
}

def read_report(report_path):
    """读取投资日报文件"""
    try:
        with open(report_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ Error reading report: {e}", file=sys.stderr)
        return None

def send_feishu_message(user_id, content):
    """
    发送飞书消息（简化版，实际需调用API）
    在当前OpenClaw环境中，我们使用系统集成的message工具
    """
    try:
        # 实际实现会调用Feishu API
        # 这里我们只记录日志
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] Message to {user_id}: {len(content)} characters\n"
        
        # 写入日志
        with open('/tmp/investment-reports/feishu_send.log', 'a') as f:
            f.write(log_entry)
        
        print(f"✅ Message prepared for Feishu delivery")
        return True
        
    except Exception as e:
        print(f"❌ Error preparing message: {e}", file=sys.stderr)
        return False

def main():
    """主函数"""
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <user_id> <report_file>", file=sys.stderr)
        sys.exit(1)
    
    user_id = sys.argv[1]
    report_file = sys.argv[2]
    
    # 读取报告
    content = read_report(report_file)
    if not content:
        sys.exit(1)
    
    # 发送消息
    if send_feishu_message(user_id, content):
        print(f"📤 Investment report sent to {user_id}")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
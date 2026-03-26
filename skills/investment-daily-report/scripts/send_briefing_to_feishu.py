#!/usr/bin/env python3
"""
飞书简报推送脚本
使用OpenClaw环境变量发送消息到飞书
"""

import sys
import os
import json
import requests
from datetime import datetime

# Feishu API配置
FEISHU_APP_ID = os.environ.get('FEISHU_APP_ID', 'cli_a92826c79ce4dbb6')
FEISHU_APP_SECRET = os.environ.get('FEISHU_APP_SECRET', '')

# 目标用户（Roy的飞书ID）
TARGET_USER = 'ou_bbfc027431c61a8ba421c54c7bb0f5c4'

def get_tenant_access_token():
    """获取飞书tenant access token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {"Content-Type": "application/json"}
    payload = {
        "app_id": FEISHU_APP_ID,
        "app_secret": FEISHU_APP_SECRET
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        data = response.json()
        if data.get("code") == 0:
            return data.get("tenant_access_token")
        else:
            print(f"❌ 获取token失败: {data}")
            return None
    except Exception as e:
        print(f"❌ 请求token失败: {e}")
        return None

def send_message_to_user(token, user_id, content):
    """发送文本消息给用户"""
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    
    # 截取简报前3000字符（飞书限制）
    truncated_content = content[:3000] + "..." if len(content) > 3000 else content
    
    payload = {
        "receive_id": user_id,
        "msg_type": "text",
        "content": json.dumps({"text": truncated_content})
    }
    
    params = {"receive_id_type": "open_id"}
    
    try:
        response = requests.post(url, json=payload, headers=headers, params=params, timeout=15)
        data = response.json()
        if data.get("code") == 0:
            print(f"✅ 简报推送成功！")
            return True
        else:
            print(f"❌ 推送失败: {data}")
            return False
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <briefing_file>", file=sys.stderr)
        sys.exit(1)
    
    briefing_file = sys.argv[1]
    
    # 读取简报内容
    try:
        with open(briefing_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ 读取简报失败: {e}", file=sys.stderr)
        sys.exit(1)
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 开始推送简报...")
    
    # 如果没有配置app_secret，使用简化方式通知
    if not FEISHU_APP_SECRET:
        print("⚠️ FEISHU_APP_SECRET未配置，简报已生成但未推送")
        print(f"📄 简报位置: {briefing_file}")
        # 写入待推送队列
        queue_file = f"/tmp/feishu_send_queue_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(queue_file, 'w') as f:
            f.write(f"user:{TARGET_USER}\nfile:{briefing_file}")
        print(f"📤 已加入推送队列: {queue_file}")
        sys.exit(0)
    
    # 获取token并发送
    token = get_tenant_access_token()
    if token:
        if send_message_to_user(token, TARGET_USER, content):
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()

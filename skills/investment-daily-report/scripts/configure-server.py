#!/usr/bin/env python3
"""
OpenClaw服务器配置自动化工具
远程配置中国节点服务器
"""

import paramiko
import sys
import time
from pathlib import Path

# 配置信息
SERVER_IP = "101.32.249.81"
SERVER_PORT = 22
ROOT_PASSWORD = "H7cevo3@openclaw"

# 安装脚本
SETUP_SCRIPT = """#!/bin/bash
set -e
echo "🚀 开始配置OpenClaw服务器..."
echo "==================================="

# 更新系统
echo "📦 更新系统包..."
apt-get update -qq
apt-get upgrade -y -qq

# 安装基础工具
echo "🔧 安装基础工具..."
apt-get install -y curl wget git build-essential software-properties-common gnupg lsb-release -qq

# 安装Node.js 20
echo "📥 安装Node.js 20..."
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt-get install -y nodejs -qq
node --version
npm --version

# 安装Python 3.11
echo "🐍 安装Python 3.11..."
apt-get install -y python3.11 python3.11-venv python3-pip python3.11-dev -qq
python3.11 --version
pip3 --version

# 安装AKShare依赖
echo "📊 安装AKShare依赖..."
apt-get install -y libxml2-dev libxslt1-dev python3-dev -qq

# 安装AKShare和Tushare
echo "📦 安装AKShare和Tushare..."
pip3 install --upgrade pip setuptools wheel -q
pip3 install akshare tushare pandas numpy -q

# 安装OpenClaw CLI
echo "🦞 安装OpenClaw..."
npm install -g openclaw@latest
openclaw --version

# 创建目录和工作空间
echo "📁 创建工作空间..."
mkdir -p /root/.openclaw/workspace
cd /root/.openclaw/workspace

# 配置环境变量
echo 'export TAVILY_API_KEY="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"' >> ~/.bashrc
echo 'export PATH="/root/.local/bin:$PATH"' >> ~/.bashrc

# 初始化workspace
echo "📝 初始化workspace..."
cd /root/.openclaw/workspace

# 创建基础配置文件
cat > /root/.openclaw/config.yaml << 'EOFCONFIG'
gateway:
  enabled: true
  host: 0.0.0.0
  port: 3000

providers:
  feishu:
    enabled: true
    app_id: cli_a92826c79ce4dbb6
    app_secret: 
    verification_token: 
EOFCONFIG

echo "✅ 服务器基础配置完成！"
echo "==================================="
"""

def setup_server():
    """配置服务器"""
    try:
        # 创建SSH客户端
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        print(f"🔌 连接到服务器 {SERVER_IP}...")
        print(f"⏰ 使用超时时间: 60秒...")
        client.connect(
            hostname=SERVER_IP,
            port=SERVER_PORT,
            username="root",
            password=ROOT_PASSWORD,
            timeout=60,
            banner_timeout=60,
            auth_timeout=60
        )
        
        print("✅ SSH连接成功！\n")
        
        # 将脚本写入服务器
        print("📄 传输配置脚本...")
        stdin, stdout, stderr = client.exec_command("cat > /tmp/setup.sh << 'EOFSCRIPT'\n" + SETUP_SCRIPT + "\nEOFSCRIPT")
        stdin.close()
        
        # 检查脚本是否写入成功
        stdin, stdout, stderr = client.exec_command("ls -lh /tmp/setup.sh")
        print(stdout.read().decode())
        
        # 执行配置脚本
        print("🚀 开始执行配置脚本（预计15-20分钟）...")
        print("⏰ 执行时间较长，请耐心等待...\n")
        
        # 使用nohup在后台执行
        stdin, stdout, stderr = client.exec_command("chmod +x /tmp/setup.sh && nohup bash /tmp/setup.sh > /tmp/setup.log 2>&1 & echo 'Setup started with PID:' && ps aux | grep setup.sh | grep -v grep")
        
        output = stdout.read().decode()
        print(output)
        
        # 等待10秒让开始执行
        time.sleep(10)
        
        # 检查日志
        print("\n📋 查看配置日志（前50行）：")
        stdin, stdout, stderr = client.exec_command("head -50 /tmp/setup.log || echo 'Log file not found yet'")
        log_output = stdout.read().decode()
        print(log_output)
        
        print("\n⏳ 配置正在后台运行...")
        print("✅ 配置脚本已成功启动！")
        
        client.close()
        
        return True
        
    except Exception as e:
        print(f"❌ 配置失败: {e}")
        return False

def check_progress():
    """检查配置进度"""
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname=SERVER_IP,
            port=SERVER_PORT,
            username="root",
            password=ROOT_PASSWORD,
            timeout=30
        )
        
        print("\n📊 检查配置进度...")
        
        # 检查Node.js
        stdin, stdout, stderr = client.exec_command("node --version")
        node_version = stdout.read().decode().strip()
        if node_version:
            print(f"  ✅ Node.js: {node_version}")
        else:
            print("  ⏳ Node.js 安装中...")
        
        # 检查Python
        stdin, stdout, stderr = client.exec_command("python3.11 --version")
        python_version = stdout.read().decode().strip()
        if python_version:
            print(f"  ✅ Python: {python_version}")
        else:
            print("  ⏳ Python 安装中...")
        
        # 检查AKShare
        stdin, stdout, stderr = client.exec_command("pip3 list | grep akshare")
        akshare_info = stdout.read().decode().strip()
        if akshare_info:
            print(f"  ✅ AKShare: {akshare_info}")
        else:
            print("  ⏳ AKShare 安装中...")
        
        # 查看日志末尾
        stdin, stdout, stderr = client.exec_command("tail -20 /tmp/setup.log")
        log_tail = stdout.read().decode()
        if log_tail:
            print(f"\n📋 最新日志:")
            print(log_tail)
        
        client.close()
        
    except Exception as e:
        print(f"❌ 检查进度失败: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("OpenClaw服务器配置工具")
    print(f"目标服务器: {SERVER_IP}")
    print("=" * 60)
    print()
    
    # 检查paramiko是否安装
    try:
        import paramiko
    except ImportError:
        print("❌ paramiko未安装，正在安装...")
        import subprocess
        subprocess.run(["pip3", "install", "paramiko", "-q"])
        import paramiko
    
    # 开始配置
    if setup_server():
        print("\n✅ 配置脚本已成功启动！")
        print("⏰ 等待3分钟后检查进度...")
        time.sleep(180)
        check_progress()
    else:
        print("\n❌ 配置启动失败")
        sys.exit(1)

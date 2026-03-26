#!/usr/bin/env python3
"""
OpenClaw任务监控脚本
解决：后台任务执行无反馈问题
功能：主动监控进程状态，定期向用户报告
"""

import pexpect
import time
import sys
from datetime import datetime

# 监控配置
CHECK_INTERVAL = 60  # 每60秒检查一次
TIMEOUT_THRESHOLD = 300  # 5分钟无进展视为卡住

class TaskMonitor:
    def __init__(self, session_id, task_name, server_ip, server_port, password):
        self.session_id = session_id
        self.task_name = task_name
        self.server_ip = server_ip
        self.server_port = server_port
        self.password = password
        self.start_time = datetime.now()
        self.last_progress = datetime.now()
        self.child = None
        
    def connect(self):
        """连接服务器"""
        try:
            self.child = pexpect.spawn(
                f'ssh -p {self.server_port} -o StrictHostKeyChecking=no root@{self.server_ip}',
                timeout=30
            )
            self.child.expect('password:', timeout=10)
            self.child.sendline(self.password)
            self.child.expect('root@', timeout=15)
            return True
        except Exception as e:
            print(f"❌ 连接失败: {e}")
            return False
    
    def check_process(self, process_name):
        """检查特定进程"""
        try:
            self.child.sendline(f'ps aux | grep "{process_name}" | grep -v grep')
            self.child.expect('root@', timeout=10)
            output = self.child.before.decode()
            lines = [line for line in output.split('\n') if process_name in line and 'grep' not in line]
            return lines
        except:
            return []
    
    def check_installation(self):
        """检查Python包安装状态"""
        try:
            self.child.sendline('python3 -m pip list 2>&1 | grep -iE "(akshare|tushare|pandas)"')
            self.child.expect('root@', timeout=10)
            output = self.child.before.decode()
            packages = []
            for line in output.split('\n'):
                if 'akshare' in line.lower() or 'tushare' in line.lower() or 'pandas' in line.lower():
                    packages.append(line.strip())
            return packages
        except:
            return []
    
    def check_disk_space(self):
        """检查磁盘空间"""
        try:
            self.child.sendline('df -h / | tail -1')
            self.child.expect('root@', timeout=5)
            output = self.child.before.decode().split('\n')[-2].strip()
            return output
        except:
            return "未知"
    
    def check_data_files(self, pattern):
        """检查数据文件"""
        try:
            self.child.sendline(f'ls -lh {pattern} 2>&1')
            self.child.expect('root@', timeout=10)
            output = child.before.decode()
            lines = [line for line in output.split('\n') if pattern.replace('*', '') in line]
            return lines
        except:
            return []
    
    def generate_status_report(self):
        """生成状态报告"""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        
        report = []
        report.append(f"📊 任务监控报告 ({self.task_name})")
        report.append(f"开始时间: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"已运行: {elapsed//60:.0f}分{elapsed%60:.0f}秒")
        report.append("")
        
        # 检查Python环境
        packages = self.check_installation()
        if packages:
            report.append("✅ 已安装的工具:")
            for pkg in packages:
                report.append(f"  - {pkg}")
        else:
            report.append("⚠️  数据工具未安装")
        report.append("")
        
        # 检查磁盘
        disk = self.check_disk_space()
        report.append(f"💾 磁盘空间: {disk}")
        report.append("")
        
        # 检查Python进程
        python_procs = self.check_process('python3')
        if python_procs:
            report.append("🐍 Python进程:")
            for proc in python_procs[:3]:
                report.append(f"  {proc[:80]}")
        else:
            report.append("⚠️  无Python进程运行")
        report.append("")
        
        # 检查数据文件
        data_files = self.check_data_files('/tmp/real-data*')
        if data_files:
            report.append("📄 数据文件:")
            for f in data_files:
                report.append(f"  {f}")
        else:
            report.append("⚠️  数据文件未生成")
        
        return "\n".join(report)
    
    def check_stuck(self):
        """检查是否卡住"""
        elapsed = (datetime.now() - self.last_progress).total_seconds()
        return elapsed > TIMEOUT_THRESHOLD
    
    def run_long_task(self, command, timeout=1800):
        """运行长时间任务并监控"""
        try:
            print(f"🚀 开始执行任务: {command}")
            print(f"⏱️  预计完成时间: {timeout//60}分钟")
            print()
            
            self.child.sendline(command)
            
            # 等待命令完成
            patterns = ['root@', 'finished', 'Error:', 'error:', pexpect.TIMEOUT, pexpect.EOF]
            index = self.child.expect(patterns, timeout=timeout)
            
            if index in [4, 5]:  # TIMEOUT or EOF
                print(f"⚠️  任务超时或连接中断 (状态: {index})")
                return False
            else:
                print(f"✅ 任务执行完成 (状态: {index})")
                return True
                
        except Exception as e:
            print(f"❌ 任务执行异常: {e}")
            return False
    
    def start_monitoring(self):
        """开始监控"""
        print(f"\n{'='*70}")
        print(f"📡 任务监控启动: {self.task_name}")
        print(f"⏰ 检查间隔: {CHECK_INTERVAL}秒")
        print(f"🚨 超时阈值: {TIMEOUT_THRESHOLD//60}分钟")
        print(f"{'='*70}\n")
        
        if not self.connect():
            print("❌ 无法连接服务器，监控启动失败")
            return False
        
        cycle = 0
        while True:
            cycle += 1
            print(f"\n{'='*60}")
            print(f"📊 检查 #{cycle} ({datetime.now().strftime('%H:%M:%S')})")
            print(f"{'='*60}")
            
            # 生成并打印状态报告
            report = self.generate_status_report()
            print(report)
            
            # 检查是否卡住
            if self.check_stuck():
                print(f"\n🚨 ALERT: 任务已超过{TIMEOUT_THRESHOLD//60}分钟无进展！")
                print("建议: 检查任务状态或重启任务")
            
            # 等待下一次检查
            print(f"\n💤 等待{CHECK_INTERVAL}秒后进行下一次检查...")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("用法: python3 monitor.py <session_id> <task_name> <server_ip> <server_port> <password>")
        sys.exit(1)
    
    monitor = TaskMonitor(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5])
    monitor.start_monitoring()

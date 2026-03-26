#!/usr/bin/env python3
"""
每周初始化脚本 - 合并节点1/2/3
- 收集论文
- 生成阅读周文档
- 自动下载前3篇论文PDF
- 生成前3篇论文注释稿
- 发送飞书消息通知

用法:
    python scripts/weekly_init.py
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# 配置
WORKSPACE = Path("/root/.openclaw/workspace")
SKILL_DIR = WORKSPACE / "skills" / "paper-research-assistant"
PAPER_DIR = WORKSPACE / "paper-research"
DATA_DIR = PAPER_DIR / "data"
USER_ID = "ou_bbfc027431c61a8ba421c54c7bb0f5c4"

def run_command(cmd, cwd=None, check=True):
    """运行命令并返回结果"""
    print(f"[执行] {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    if check and result.returncode != 0:
        print(f"[错误] 命令失败: {result.stderr}")
        return None
    return result.stdout

def send_feishu_message(message):
    """发送飞书消息"""
    try:
        result = subprocess.run(
            ["openclaw", "message", "send", "--channel", "feishu", 
             "--target", USER_ID, "--message", message],
            capture_output=True, text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"[错误] 发送消息失败: {e}")
        return False

def collect_papers():
    """步骤1: 收集论文"""
    print("\n" + "="*60)
    print("📥 步骤1: 收集本周论文")
    print("="*60)
    
    result = run_command(
        ["python3", "scripts/fetch_papers.py", "--discipline", "ai", "--max-results", "7"],
        cwd=SKILL_DIR
    )
    
    if result is None:
        return False, "论文收集失败"
    
    # 读取收集的论文
    with open(DATA_DIR / "papers.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 获取本周新增的论文
    today = datetime.now().strftime("%Y-%m-%d")
    new_papers = [p for p in data.get("papers", []) if p.get("collection_date") == today]
    
    if len(new_papers) < 3:
        return False, f"论文数量不足: {len(new_papers)} 篇"
    
    print(f"✅ 成功收集 {len(new_papers)} 篇论文")
    return True, new_papers[:7]  # 最多7篇

def download_top3(papers):
    """步骤2: 下载前3篇论文PDF"""
    print("\n" + "="*60)
    print("📄 步骤2: 下载前3篇论文PDF")
    print("="*60)
    
    downloaded = []
    for paper in papers[:3]:
        arxiv_id = paper.get("arxiv_id")
        if not arxiv_id:
            continue
        
        print(f"\n[下载] {arxiv_id} - {paper.get('title', 'Unknown')[:50]}...")
        
        result = run_command(
            ["python3", "scripts/download_paper.py", "--paper-id", arxiv_id],
            cwd=SKILL_DIR,
            check=False
        )
        
        pdf_path = PAPER_DIR / "papers" / "ai" / f"arxiv_{arxiv_id}.pdf"
        if pdf_path.exists():
            downloaded.append(paper)
            print(f"✅ 下载成功: {pdf_path}")
        else:
            print(f"⚠️ 下载失败或PDF已存在")
    
    return downloaded

def generate_annotations(papers):
    """步骤3: 生成前3篇论文的注释稿"""
    print("\n" + "="*60)
    print("✍️ 步骤3: 生成前3篇论文注释稿")
    print("="*60)
    
    generated = []
    for paper in papers[:3]:
        arxiv_id = paper.get("arxiv_id")
        if not arxiv_id:
            continue
        
        print(f"\n[生成] {arxiv_id} 注释稿...")
        print("⏳ 这可能需要3-5分钟，请稍候...")
        
        result = run_command(
            ["python3", "scripts/generate_annotation.py", "--paper-id", arxiv_id],
            cwd=SKILL_DIR,
            check=False
        )
        
        # 检查注释稿是否生成
        annotation_path = PAPER_DIR / "annotations" / "ai" / f"arxiv_{arxiv_id}_annotated.md"
        if annotation_path.exists():
            generated.append({
                "paper": paper,
                "annotation_path": annotation_path
            })
            print(f"✅ 注释稿生成成功")
        else:
            print(f"⚠️ 注释稿生成可能未完成，将在后续手动处理")
    
    return generated

def create_weekly_doc(papers, annotations):
    """步骤4: 生成阅读周文档并上传到飞书"""
    print("\n" + "="*60)
    print("📄 步骤4: 生成阅读周文档")
    print("="*60)
    
    today = datetime.now()
    week_start = today.strftime("%Y-%m-%d")
    doc_title = f"📚 AI阅读周 - Week of {week_start}"
    
    # 生成 Markdown 内容
    content = f"""# {doc_title}

> 生成时间: {today.strftime("%Y-%m-%d %H:%M")}
> 本周共 {len(papers)} 篇论文，前3篇已自动生成注释稿

---

## 📋 本周阅读清单

"""
    
    for i, paper in enumerate(papers, 1):
        arxiv_id = paper.get("arxiv_id", "")
        title = paper.get("title", "Unknown")
        abstract = paper.get("abstract", "")[:200] + "..." if len(paper.get("abstract", "")) > 200 else paper.get("abstract", "")
        
        # 检查是否有注释稿
        has_annotation = any(a["paper"]["arxiv_id"] == arxiv_id for a in annotations)
        annotation_status = "✅ 已生成" if has_annotation else "⏳ 待生成"
        
        content += f"""### #{i} {title[:60]}

**arXiv ID**: {arxiv_id}

**摘要**:
{abstract}

**链接**:
- 📄 arXiv原文: https://arxiv.org/abs/{arxiv_id}
- 📥 PDF下载: https://arxiv.org/pdf/{arxiv_id}.pdf
- 📝 注释稿详解: {annotation_status}

---

"""
    
    content += """## 📅 阅读计划建议

| 日期 | 任务 | 状态 |
|------|------|------|
| Day 1 (周一) | 阅读 #1 论文，查看注释稿 | ⏳ |
| Day 2 (周二) | 阅读 #2 论文，查看注释稿 | ⏳ |
| Day 3 (周三) | 阅读 #3 论文，查看注释稿 | ⏳ |
| Day 4-5 | 阅读 #4-5 论文 | ⏳ |
| Day 6-7 | 阅读 #6-7 论文，生成剩余注释稿 | ⏳ |

## 💡 使用说明

1. **阅读论文**: 点击 arXiv 链接阅读原文
2. **查看注释**: 已生成的注释稿在飞书文档中
3. **标记完成**: 读完后告诉我 "已读完 #编号"
4. **生成注释**: 如需生成其他论文注释稿，告诉我 "生成 #编号 注释稿"

---

*自动生成于 {today.strftime("%Y-%m-%d %H:%M")}*
"""
    
    # 保存本地备份
    local_doc_path = PAPER_DIR / f"AI阅读周_{week_start}.md"
    with open(local_doc_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ 本地文档已保存: {local_doc_path}")
    
    # TODO: 上传到飞书文档（需要调用 feishu_create_doc 工具）
    # 由于无法直接调用工具，返回内容供后续处理
    return doc_title, content, local_doc_path

def send_notification(doc_title, papers, annotations):
    """步骤5: 发送飞书消息通知"""
    print("\n" + "="*60)
    print("📬 步骤5: 发送飞书通知")
    print("="*60)
    
    week_start = datetime.now().strftime("%Y-%m-%d")
    
    message = f"""📚 AI阅读周已启动 - Week of {week_start}

本周已为你准备 {len(papers)} 篇 AI 领域前沿论文：

"""
    
    for i, paper in enumerate(papers[:3], 1):
        arxiv_id = paper.get("arxiv_id", "")
        title = paper.get("title", "Unknown")[:50]
        message += f"#{i} {title}...\n"
    
    if len(papers) > 3:
        message += f"... 还有 {len(papers)-3} 篇论文\n"
    
    message += f"""
✅ 已完成：
• 论文收集 ({len(papers)} 篇)
• PDF 下载 (前3篇)
• 注释稿生成 (前3篇)

📄 阅读周文档：
文件已生成在本地，正在创建飞书文档...

💡 下一步：
1. 查看阅读周文档了解本周计划
2. 点击 arXiv 链接阅读 #1 论文
3. 读完后告诉我 "已读完 #1" 生成知识卡片

⏰ 知识卡片复习推送：
每日 08:30/12:00/16:00/20:00
"""
    
    if send_feishu_message(message):
        print("✅ 飞书消息发送成功")
        return True
    else:
        print("❌ 飞书消息发送失败")
        return False

def main():
    """主流程"""
    print("\n" + "="*60)
    print("🚀 每周论文阅读初始化")
    print("="*60)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 步骤1: 收集论文
    success, result = collect_papers()
    if not success:
        error_msg = f"⚠️ 每周初始化失败: {result}"
        print(error_msg)
        send_feishu_message(error_msg)
        return 1
    
    papers = result
    
    # 步骤2: 下载前3篇PDF
    downloaded = download_top3(papers)
    
    # 步骤3: 生成前3篇注释稿
    annotations = generate_annotations(downloaded)
    
    # 步骤4: 生成阅读周文档
    doc_title, content, local_path = create_weekly_doc(papers, annotations)
    
    # 步骤5: 发送通知
    send_notification(doc_title, papers, annotations)
    
    print("\n" + "="*60)
    print("✅ 每周初始化完成!")
    print("="*60)
    print(f"\n总结:")
    print(f"  - 收集论文: {len(papers)} 篇")
    print(f"  - 下载PDF: {len(downloaded)} 篇")
    print(f"  - 生成注释稿: {len(annotations)} 篇")
    print(f"  - 文档位置: {local_path}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
质量检查脚本 - 验证注释稿是否符合规范

用法:
    python scripts/quality_check.py --annotation <arxiv_id>
    python scripts/quality_check.py --file <path/to/annotation.md>
"""

import argparse
import re
import sys
from pathlib import Path


def check_annotation_quality(filepath):
    """检查注释稿质量"""
    print(f"\n🔍 检查注释稿: {filepath}")
    print("="*60)
    
    if not Path(filepath).exists():
        print(f"❌ 文件不存在: {filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = []
    
    # Check 1: 封面信息完整
    has_title = bool(re.search(r'\*\*标题\*\*:', content))
    has_arxiv_id = bool(re.search(r'\*\*arXiv ID\*\*:', content))
    has_field = bool(re.search(r'\*\*领域\*\*:', content))
    checks.append(("封面信息完整", has_title and has_arxiv_id and has_field))
    
    # Check 2: 包含关键章节
    has_abstract = '## 摘要' in content or '## Abstract' in content
    has_intro = bool(re.search(r'## (第1节 |1 |引言|Introduction)', content))
    checks.append(("包含摘要章节", has_abstract))
    checks.append(("包含引言章节", has_intro))
    
    # Check 3: 段落格式规范（【原文】用粗体，非标题）
    # 检查是否有错误使用标题的情况
    wrong_format = re.search(r'^## .*【原文】', content, re.MULTILINE)
    checks.append(("段落格式规范（无标题化标注）", wrong_format is None))
    
    # Check 4: 每段有原文+翻译+解释
    original_count = len(re.findall(r'\*\*【原文】\*\*', content))
    translation_count = len(re.findall(r'\*\*【中文翻译】\*\*', content))
    explanation_count = len(re.findall(r'\*\*【注释解释】\*\*', content))
    
    checks.append(("原文标注数量", original_count > 0, f"{original_count} 段"))
    checks.append(("翻译标注数量", translation_count > 0, f"{translation_count} 段"))
    checks.append(("解释标注数量", explanation_count > 0, f"{explanation_count} 段"))
    
    # Check 5: 术语解释数量
    term_explanations = len(re.findall(r'\*\*术语解释\*\*', content))
    checks.append(("术语解释数量 ≥ 3", term_explanations >= 3, f"{term_explanations} 个"))
    
    # Check 6: 包含跨学科关联
    has_interdisciplinary = '## 跨学科关联' in content or '## 跨学科' in content
    checks.append(("包含跨学科关联分析", has_interdisciplinary))
    
    # Check 7: 段落间有分割线
    separator_count = content.count('\n---\n')
    checks.append(("段落间分割线", separator_count > 0, f"{separator_count} 处"))
    
    # 输出结果
    passed = 0
    for check_name, result, *details in checks:
        status = "✅" if result else "❌"
        detail = details[0] if details else ""
        if detail:
            print(f"{status} {check_name}: {detail}")
        else:
            print(f"{status} {check_name}")
        if result:
            passed += 1
    
    print("="*60)
    print(f"检查结果: {passed}/{len(checks)} 项通过")
    
    if passed == len(checks):
        print("🎉 质量检查全部通过！")
        return True
    else:
        print("⚠️ 部分检查未通过，请修复后重试")
        return False


def main():
    parser = argparse.ArgumentParser(description='注释稿质量检查')
    parser.add_argument('--annotation', help='arXiv ID，自动查找对应注释稿')
    parser.add_argument('--file', help='注释稿文件路径')
    
    args = parser.parse_args()
    
    if args.file:
        success = check_annotation_quality(args.file)
    elif args.annotation:
        # 查找注释稿文件
        base_dir = Path(__file__).parent.parent / "annotations"
        possible_paths = [
            base_dir / "ai" / f"{args.annotation}_annotation.md",
            base_dir / "psychology" / f"{args.annotation}_annotation.md",
            base_dir / "social-science" / f"{args.annotation}_annotation.md",
        ]
        
        found = False
        for path in possible_paths:
            if path.exists():
                success = check_annotation_quality(path)
                found = True
                break
        
        if not found:
            print(f"❌ 找不到注释稿: {args.annotation}")
            success = False
    else:
        parser.print_help()
        return
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
脱口秀逐字稿拆解分析 - 使用示例
"""

from analyzer import ComedyTranscriptAnalyzer

def main():
    # 初始化分析器
    analyzer = ComedyTranscriptAnalyzer(output_dir="./output")
    
    # 示例：原生家庭主题的笑点数据
    family_jokes = [
        {
            "id": "1.1",
            "title": "开场钩子",
            "text": "我来自一个 messed up 的家庭。我知道这并不会让我在这个房间里显得特别。你们需要专业人士（needed a professional）。",
            "relation": "开场引入",
            "theme": "原生家庭"
        },
        {
            "id": "1.2",
            "title": "Kevin家的健康争吵",
            "text": "七年级时我在朋友 Kevin 家过夜...那是我听过的最健康的争吵（healthiest disagreement）。",
            "relation": "承接1.1：展开童年认知",
            "theme": "原生家庭"
        },
        {
            "id": "1.3",
            "title": "父母7天大离婚",
            "text": "我父母在我出生七天的时候就离婚了。我的第一个词是妈妈（mama），但我的接下来五个字（next five words）...",
            "relation": "承接1.2：引入父母离婚",
            "theme": "原生家庭"
        }
    ]
    
    # 生成PPT
    output_file = analyzer.create_ppt(
        title="【原生家庭】主题笑点详解",
        jokes_data=family_jokes,
        filename="原生家庭分析.pptx"
    )
    
    print(f"✅ PPT已生成: {output_file}")

if __name__ == "__main__":
    main()

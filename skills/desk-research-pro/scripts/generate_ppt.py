#!/usr/bin/env python3
"""
桌面研究PPT生成脚本 - 专业版
参照毕马威/艾瑞/灼识/国金证券研报质量标准
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE
from pptx.chart.data import ChartData
from typing import List, Dict, Any, Tuple, Optional
import json

# ========== 标准配色方案 ==========
# 基于毕马威/艾瑞/灼识咨询研报标准
COLORS = {
    "dark_blue": RGBColor(0, 51, 102),      # 深海蓝 - 主色
    "tech_blue": RGBColor(0, 112, 192),     # 科技蓝 - 辅助
    "orange": RGBColor(255, 127, 39),       # 活力橙 - 强调
    "green": RGBColor(0, 176, 80),          # 绿色 - 正向
    "purple": RGBColor(112, 48, 160),       # 紫色 - AI/科技
    "dark_gray": RGBColor(64, 64, 64),      # 深灰 - 正文
    "light_gray": RGBColor(128, 128, 128),  # 浅灰 - 次要
    "white": RGBColor(255, 255, 255),       # 白色
    "bg_light": RGBColor(245, 248, 252),    # 浅蓝灰 - 卡片背景
    "table_header": RGBColor(0, 51, 102),   # 表头色
    "table_odd": RGBColor(250, 250, 250),   # 斑马纹-奇数行
    "table_even": RGBColor(255, 255, 255),  # 斑马纹-偶数行
}

# ========== 字体标准 ==========
FONTS = {
    "title": ("Microsoft YaHei", 28, True, COLORS["dark_blue"]),
    "subtitle": ("Microsoft YaHei", 20, False, COLORS["tech_blue"]),
    "heading": ("Microsoft YaHei", 16, True, COLORS["dark_blue"]),
    "body": ("Microsoft YaHei", 12, False, COLORS["dark_gray"]),
    "caption": ("Microsoft YaHei", 10, False, COLORS["light_gray"]),
    "source": ("Microsoft YaHei", 9, False, COLORS["light_gray"]),
}

# ========== 基础函数 ==========

def create_presentation() -> Presentation:
    """创建符合标准的PPT基础结构"""
    prs = Presentation()
    prs.slide_width = Inches(13.333)  # 16:9比例
    prs.slide_height = Inches(7.5)
    return prs

def add_text_box(slide, text: str, left: float, top: float, 
                 width: float, height: float, 
                 font_name: str = "Microsoft YaHei",
                 font_size: int = 12,
                 color: RGBColor = COLORS["dark_gray"], 
                 bold: bool = False,
                 align: int = PP_ALIGN.LEFT,
                 line_spacing: float = 1.0) -> Any:
    """添加文本框"""
    shape = slide.shapes.add_textbox(
        Inches(left), Inches(top), 
        Inches(width), Inches(height)
    )
    tf = shape.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.name = font_name
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.alignment = align
    if line_spacing != 1.0:
        p.line_spacing = line_spacing
    return shape

def add_data_source(slide, source: str, left: float = 0.6, bottom: float = 6.8):
    """添加数据来源标注（右下角）"""
    add_text_box(
        slide, f"数据来源：{source}", 
        left, bottom, 12, 0.3,
        font_size=9, color=COLORS["light_gray"], align=PP_ALIGN.RIGHT
    )

def add_page_number(slide, number: int):
    """添加页码（右下角）"""
    add_text_box(
        slide, str(number),
        12.5, 7.0, 0.6, 0.3,
        font_size=10, color=COLORS["light_gray"]
    )

def add_title_line(slide, left: float = 0.6, top: float = 1.25, 
                   width: float = 2, color: RGBColor = COLORS["dark_blue"]):
    """添加装饰线条"""
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 
        Inches(left), Inches(top), 
        Inches(width), Pt(3)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = color
    line.line.fill.background()
    return line

# ========== 页面类型函数 ==========

def add_cover_slide(prs: Presentation, title: str, subtitle: str = "", 
                    date: str = "") -> Any:
    """添加封面页（专业简洁风格）"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 左侧装饰条
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 
        Inches(0), Inches(2.2), 
        Inches(0.3), Inches(3.0)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = COLORS["dark_blue"]
    bar.line.fill.background()
    
    # 主标题
    add_text_box(
        slide, title,
        0.8, 2.4, 11.5, 1.2,
        font_size=40, bold=True, color=COLORS["dark_blue"]
    )
    
    # 副标题
    if subtitle:
        add_text_box(
            slide, subtitle,
            0.8, 3.8, 11.5, 0.6,
            font_size=20, color=COLORS["tech_blue"]
        )
    
    # 日期
    if date:
        add_text_box(
            slide, date,
            0.8, 5.5, 11.5, 0.4,
            font_size=14, color=COLORS["light_gray"]
        )
    
    add_page_number(slide, 1)
    return slide

def add_toc_slide(prs: Presentation, items: List[str]) -> Any:
    """添加目录页"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 标题
    add_text_box(
        slide, "目录",
        0.6, 0.5, 12, 0.8,
        font_size=28, bold=True, color=COLORS["dark_blue"]
    )
    add_title_line(slide)
    
    # 目录项
    y = 1.8
    for i, item in enumerate(items, 1):
        num = f"{i:02d}"
        # 编号
        add_text_box(
            slide, num,
            0.8, y, 0.8, 0.5,
            font_size=20, bold=True, color=COLORS["tech_blue"]
        )
        # 文字
        add_text_box(
            slide, item,
            1.6, y, 8, 0.5,
            font_size=16, color=COLORS["dark_gray"]
        )
        y += 0.85
    
    add_page_number(slide, 2)
    return slide

def add_content_slide(prs: Presentation, title: str, 
                      bullets: List[str],
                      data_source: str = "",
                      note_box: Optional[Dict] = None) -> Any:
    """
    添加标准内容页
    
    Args:
        title: 页面标题
        bullets: bullet points列表
        data_source: 数据来源
        note_box: 底部注释框内容 {"title": str, "content": str}
    """
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 标题
    add_text_box(
        slide, title,
        0.6, 0.5, 12, 0.8,
        font_size=22, bold=True, color=COLORS["dark_blue"]
    )
    add_title_line(slide)
    
    # Bullet points
    y = 1.6
    for bullet in bullets:
        add_text_box(
            slide, "• " + bullet,
            0.8, y, 11.5, 0.5,
            font_size=13, color=COLORS["dark_gray"],
            line_spacing=1.3
        )
        y += 0.55
    
    # 注释框（可选）
    if note_box:
        box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(0.8), Inches(4.4), Inches(11.5), Inches(2.2)
        )
        box.fill.solid()
        box.fill.fore_color.rgb = COLORS["bg_light"]
        box.line.color.rgb = COLORS["tech_blue"]
        
        add_text_box(
            slide, note_box.get("title", ""),
            1.0, 4.6, 11, 0.4,
            font_size=14, bold=True, color=COLORS["dark_blue"]
        )
        add_text_box(
            slide, note_box.get("content", ""),
            1.0, 5.05, 10.5, 1.4,
            font_size=11, color=COLORS["dark_gray"],
            line_spacing=1.3
        )
    
    if data_source:
        add_data_source(slide, data_source)
    
    return slide

def add_data_cards_slide(prs: Presentation, title: str,
                         cards: List[Tuple[str, str, str, RGBColor]],
                         notes: str = "",
                         big_number: Optional[Tuple[str, str]] = None,
                         data_source: str = "") -> Any:
    """
    添加数据卡片页（用于市场规模等核心数据）
    
    Args:
        title: 页面标题
        cards: [(数值, 标签, 颜色), ...] 最多3个卡片
        notes: 底部说明文字
        big_number: (大数字, 说明) 可选
        data_source: 数据来源
    """
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 标题
    add_text_box(
        slide, title,
        0.6, 0.5, 12, 0.8,
        font_size=20, bold=True, color=COLORS["dark_blue"]
    )
    add_title_line(slide)
    
    # 数据卡片
    x_positions = [0.6, 4.7, 8.8]
    for i, (value, label, color) in enumerate(cards[:3]):
        x = Inches(x_positions[i])
        
        # 卡片背景
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            x, Inches(1.5), Inches(3.8), Inches(1.6)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = color
        card.line.fill.background()
        
        # 数值
        add_text_box(
            slide, value,
            x_positions[i] + 0.2, 1.75, 3.4, 0.7,
            font_size=26, bold=True, color=COLORS["white"],
            align=PP_ALIGN.CENTER
        )
        
        # 标签
        add_text_box(
            slide, label,
            x_positions[i] + 0.2, 2.5, 3.4, 0.4,
            font_size=11, color=COLORS["white"],
            align=PP_ALIGN.CENTER
        )
    
    # 说明文字
    if notes:
        add_text_box(
            slide, notes,
            0.6, 3.3, 12, 0.8,
            font_size=11, color=COLORS["dark_gray"],
            line_spacing=1.3
        )
    
    # 底部大数字
    if big_number:
        number, desc = big_number
        add_text_box(
            slide, number,
            0.6, 4.3, 12, 1.0,
            font_size=44, bold=True, color=COLORS["dark_blue"]
        )
        add_text_box(
            slide, desc,
            0.6, 5.2, 12, 0.5,
            font_size=12, color=COLORS["dark_gray"]
        )
    
    if data_source:
        add_data_source(slide, data_source, bottom=6.6)
    
    return slide

def add_comparison_slide(prs: Presentation, title: str,
                         headers: List[str],
                         rows: List[List[str]],
                         data_source: str = "") -> Any:
    """
    添加对比表格页
    
    Args:
        title: 页面标题
        headers: 表头列表
        rows: 数据行列表
        data_source: 数据来源
    """
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 标题
    add_text_box(
        slide, title,
        0.6, 0.5, 12, 0.8,
        font_size=20, bold=True, color=COLORS["dark_blue"]
    )
    add_title_line(slide)
    
    # 表格（使用文本框模拟）
    col_widths = [12 / len(headers)] * len(headers)
    y = 1.5
    
    # 表头
    x = 0.6
    for i, header in enumerate(headers):
        # 表头背景
        header_bg = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(x), Inches(y), 
            Inches(col_widths[i] - 0.1), Inches(0.5)
        )
        header_bg.fill.solid()
        header_bg.fill.fore_color.rgb = COLORS["table_header"]
        header_bg.line.fill.background()
        
        add_text_box(
            slide, header,
            x + 0.05, y + 0.1, col_widths[i] - 0.2, 0.4,
            font_size=12, bold=True, color=COLORS["white"],
            align=PP_ALIGN.CENTER
        )
        x += col_widths[i]
    
    # 数据行
    y += 0.55
    for row_idx, row in enumerate(rows[:8]):  # 最多8行
        bg_color = COLORS["table_odd"] if row_idx % 2 == 0 else COLORS["table_even"]
        x = 0.6
        
        for i, cell in enumerate(row):
            # 行背景
            row_bg = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                Inches(x), Inches(y),
                Inches(col_widths[i] - 0.1), Inches(0.45)
            )
            row_bg.fill.solid()
            row_bg.fill.fore_color.rgb = bg_color
            row_bg.line.fill.background()
            
            add_text_box(
                slide, str(cell),
                x + 0.05, y + 0.05, col_widths[i] - 0.2, 0.4,
                font_size=10, color=COLORS["dark_gray"]
            )
            x += col_widths[i]
        
        y += 0.5
    
    if data_source:
        add_data_source(slide, data_source, bottom=6.8)
    
    return slide

def add_case_cards_slide(prs: Presentation, title: str,
                         cases: List[Dict[str, Any]],
                         data_source: str = "") -> Any:
    """
    添加案例卡片页
    
    Args:
        title: 页面标题
        cases: [{"name": str, "product": str, "points": [str], "color": RGBColor}, ...]
        data_source: 数据来源
    """
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    
    # 标题
    add_text_box(
        slide, title,
        0.6, 0.5, 12, 0.8,
        font_size=20, bold=True, color=COLORS["dark_blue"]
    )
    add_title_line(slide)
    
    # 案例卡片（2x2布局）
    positions = [(0.6, 1.4), (6.8, 1.4), (0.6, 4.0), (6.8, 4.0)]
    
    for i, case in enumerate(cases[:4]):
        x, y = positions[i]
        color = case.get("color", COLORS["tech_blue"])
        
        # 卡片背景
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(x), Inches(y), Inches(6), Inches(2.3)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = COLORS["bg_light"]
        card.line.color.rgb = color
        
        # 企业名
        add_text_box(
            slide, case["name"],
            x + 0.2, y + 0.15, 5.5, 0.4,
            font_size=14, bold=True, color=color
        )
        
        # 产品名
        if case.get("product"):
            add_text_box(
                slide, case["product"],
                x + 0.2, y + 0.5, 5.5, 0.35,
                font_size=11, color=COLORS["dark_gray"]
            )
        
        # 要点
        points_text = "\n".join([f"• {p}" for p in case.get("points", [])])
        add_text_box(
            slide, points_text,
            x + 0.2, y + 0.85, 5.5, 1.4,
            font_size=10, color=COLORS["dark_gray"],
            line_spacing=1.2
        )
    
    if data_source:
        add_data_source(slide, data_source, bottom=6.6)
    
    return slide

# ========== 主生成函数 ==========

def generate_professional_ppt(
    topic: str,
    subtitle: str = "",
    output_file: Optional[str] = None,
    slides_config: List[Dict] = None
) -> str:
    """
    生成专业级研究报告PPT
    
    Args:
        topic: 报告主题
        subtitle: 副标题
        output_file: 输出文件路径
        slides_config: 幻灯片配置列表
    
    Returns:
        输出文件路径
    """
    prs = create_presentation()
    
    # 默认幻灯片配置
    if slides_config is None:
        slides_config = [
            {"type": "cover"},
            {"type": "toc"},
            {"type": "content"},
        ]
    
    # 生成幻灯片
    for i, config in enumerate(slides_config):
        slide_type = config.get("type")
        
        if slide_type == "cover":
            add_cover_slide(prs, topic, subtitle, config.get("date", ""))
        
        elif slide_type == "toc":
            add_toc_slide(prs, config.get("items", []))
        
        elif slide_type == "content":
            add_content_slide(
                prs,
                config.get("title", ""),
                config.get("bullets", []),
                config.get("source", ""),
                config.get("note_box")
            )
        
        elif slide_type == "data_cards":
            add_data_cards_slide(
                prs,
                config.get("title", ""),
                config.get("cards", []),
                config.get("notes", ""),
                config.get("big_number"),
                config.get("source", "")
            )
        
        elif slide_type == "comparison":
            add_comparison_slide(
                prs,
                config.get("title", ""),
                config.get("headers", []),
                config.get("rows", []),
                config.get("source", "")
            )
        
        elif slide_type == "cases":
            add_case_cards_slide(
                prs,
                config.get("title", ""),
                config.get("cases", []),
                config.get("source", "")
            )
    
    # 保存
    if output_file is None:
        output_file = f"{topic}_研究报告.pptx"
    
    prs.save(output_file)
    print(f"✅ 专业级PPT已生成: {output_file}")
    return output_file

# ========== 使用示例 ==========

if __name__ == "__main__":
    # 示例：生成一份大模型金融应用报告PPT
    slides = [
        {
            "type": "cover",
            "date": "2026年3月"
        },
        {
            "type": "toc",
            "items": [
                "研究背景与方法论",
                "金融行业大模型应用现状",
                "传媒行业大模型应用现状",
                "标杆案例深度解析",
                "发展趋势与展望"
            ]
        },
        {
            "type": "data_cards",
            "title": "金融大模型市场：高速增长，2024年规模预计超38亿元",
            "cards": [
                ("26.46亿元", "2024年市场规模", COLORS["dark_blue"]),
                ("140%+", "2024年增长率", COLORS["tech_blue"]),
                ("310亿元", "2029年预测规模", COLORS["orange"])
            ],
            "notes": "• 2019-2024年CAGR达111.99%，2025-2029年预计CAGR为65.65%\n• MaaS模式占主导（约60%），预计2026年标准化产品份额将提升至70%+",
            "big_number": ("3万亿元", "大模型驱动的商业模式预计到2030年为金融业带来的增量商业价值"),
            "source": "头豹研究院、沙利文、公开资料整理，2024-2025"
        }
    ]
    
    generate_professional_ppt(
        "大模型在金融与传媒行业的应用研究",
        "市场现状、标杆案例与发展趋势分析",
        "/tmp/demo_report.pptx",
        slides
    )

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib import font_manager
import numpy as np

# 添加中文字体
font_path = '/tmp/NotoSansCJKsc-Regular.otf'
font_manager.fontManager.addfont(font_path)
plt.rcParams['font.family'] = 'Noto Sans CJK SC'
plt.rcParams['axes.unicode_minus'] = False

# 主题配色 - 清新色系
colors = {
    '原生家庭': '#7EB5A6',
    '恋爱女友': '#6B9BD1', 
    '表演生涯': '#90C8AC',
    '性身体': '#F4D03F',
    '生死心理': '#F1948A',
    '社会观察': '#AED6F1'
}

# 中文笑点数据
themes = {
    '原生家庭': [
        ("1.1 开场钩子", "都出身 messed up\n需要专业人士"),
        ("1.2 Kevin家", "最健康的争吵\n我听过"),
        ("1.3 7天离婚", "第一句 mama\n接下来五个字..."),
        ("1.4 家庭结构", "四个同父异母\n所以两个"),
        ("1.5 36楼", "烂地基的楼\n36层安全吗"),
        ("1.6 继父命名", "德语词形容\n睡过我妈的人"),
        ("1.7 糖爹", "他买单 =\n我的糖爹"),
        ("1.8 婚姻建议", "用舌头拼字母\n延长了六年"),
        ("1.9 妈妈约会", "你也想睡我妈"),
        ("1.10 互相伤害", "她是喷子\n互相伤害啊 mommy"),
        ("1.11 前男友", "他不能硬...\n原来是全身"),
        ("1.12 哲学梗", "电车难题\n original driver"),
        ("1.13 狗抚养权", "Reggie 宁愿\n被安乐死"),
        ("1.14 不如狗", "我多希望\n自己是博美"),
        ("1.15 糖果 trick", "自动信任她\n像恋童癖"),
        ("1.16 万圣节 callback", "万圣节就\n依恋女人"),
        ("1.17 爸爸出轨", "非伦理非一夫一妻\n当年说她疯了"),
        ("1.18 继母嫉妒", "通心粉项链\n假装漂亮睡我爸"),
        ("1.19 女友替代妈", "女友就是\n替代妈妈用的"),
        ("1.20 瑜伽反击", "你是瑜伽老师\n去操自己吧"),
        ("1.21 黑料威胁", "一张 IG 就能\ncancel 我"),
        ("1.22 爸爸帅", "你爸真帅\n好像我欠解释"),
        ("1.23 收养谣言", "我爸传的\n我是收养"),
        ("1.24 手工课老师", "睡了我老师\n但手工课不重要"),
        ("1.25 意大利家训", "家庭是一切\n+ 你妈是婊子"),
        ("1.26 遗嘱 callback", "像生前一样\n在我演出"),
        ("1.27 Venmo", "紧急情况\n还发 Venmo"),
        ("1.28 Epstein", "你约会对象\n像爱泼斯坦"),
        ("1.29 资本主义", "这是资本主义\n甜心"),
        ("1.30 非法移民", "拜金女像非法移民\n不做我们要的工作"),
        ("1.31 假心脏骤停", "假装心脏骤停\n逃避电话"),
        ("1.32 DraftKings", "爸爸手术\n我们下注"),
        ("1.33 手术成功", "回到50岁\n医院有人生他女友"),
        ("1.34 试镜 callback", "我哭了\n因为我试镜落选"),
    ],
    '恋爱女友': [
        ("2.1 免责声明", "不用真名\n叫她 women"),
        ("2.2 犹太女友", "女人都是犹太人"),
        ("2.3 Hasidic", "还没读完 Torah\n就买服装"),
        ("2.4 色盲", "我看不见鼻子"),
        ("2.5 文化犹太人", "肠胃问题压力\n但没有上帝安慰"),
        ("2.6 逾越节", "从英雄到\n弱不禁风"),
        ("2.7 迈阿密", "像沙漠...\n犹太人一直夸张"),
        ("2.8 六百万", "让我的人民走\n这里有六百万"),
        ("2.9 友谊秘诀", "维持友谊的秘诀\n是恨同性恋"),
        ("2.10 我的那个人", "你是我的人\n最后但并非最不重要"),
        ("2.11 星巴克分手", "不该带观众来"),
        ("2.12 纹身Larry", "我死去的\n朋友 Larry"),
        ("2.13 专场换纹身", "专场赢不回 Laura\n第二天就去掉"),
        ("2.14 被 peg", "她看到纹身不想口\n我希望被 peg 停止"),
        ("2.15 夜惊症", "两种精神疾病的\n唯一受害者"),
        ("2.16 强奸犯类比", "像强奸犯问\n你爽吗"),
        ("2.17 孩子问题", "怎么处理\n你的遗体"),
        ("2.18 袋鼠", "像问我要袋鼠\n不知道怎么打"),
        ("2.19 狼人", "像和狼人约会\n注射月亮"),
        ("2.20 科学奇迹", "女人工作\n需要多少科学奇迹"),
        ("2.21 胚胎裁决", "两个裁决后\n女友成19个孩子的妈"),
        ("2.22 镜子床", "证明她占了\n超过一半"),
        ("2.23 看片搜索", "搜像我女友\n的女人"),
    ],
    '表演生涯': [
        ("3.1 剧场孩子", "聋人都说\n闭嘴"),
        ("3.2 变装比赛", "John Mulaney\n只对舞台上瘾"),
        ("3.3 音乐剧学位", "想象力博士"),
        ("3.4 会计课", "第一堂课\n如何领失业救济"),
        ("3.5 三重威胁", "威胁三:\n我很烦"),
        ("3.6 20万学费", "这笑话花我\n20万美元"),
        ("3.7 华尔街之狼", "为了角色\n当了12年服务员"),
        ("3.8 群演", "家具\n但有梦想"),
        ("3.9 离梦想近", "像一生挚爱\n被小李子操"),
        ("3.10 首演夜", "水仙花\n爸爸过敏"),
    ],
    '性身体': [
        ("4.1 腿控", "这傻国家\n这样量腿"),
        ("4.2 英尺", "某人的脚\n用来量重要东西"),
        ("4.3 马用手", "英尺 手\n试过鸡巴吗"),
        ("4.4 厘米起源", "于是有了\n厘米"),
        ("4.5 六英寸", "我只想要\n六英寸"),
        ("4.6 美元钞票", "鸡巴拍华盛顿\n脸几小时"),
        ("4.7 华盛顿", "我不能撒谎\n你差一美元"),
        ("4.8 特朗普", "放一美元上\n他会说 huge"),
        ("4.9 高中剧场", "我要吸多少鸡巴\n才能吸到逼"),
        ("4.10 NYU三人行", "我是直男\n但能让你爽"),
        ("4.11 口交技巧", "蜘蛛侠\n仪仗队"),
        ("4.12 孤独", "我太孤独了\n blackout"),
        ("4.13 谣言红利", "从没得到过\n这么多逼"),
    ],
    '生死心理': [
        ("5.1 自杀开头", "没有好理由"),
        ("5.2 地狱", "你会下地狱"),
        ("5.3 宗教", "需要相信有比\n活着更糟的"),
        ("5.4 免责声明", "他们今晚\n不在"),
        ("5.5 短信", "我爱你\n对不起 再见"),
        ("5.6 语音信箱", "更新你的\n语音信箱"),
        ("5.7 通灵师", "死我成\n电影明星前"),
        ("5.8 867-5309", "我很好\n你呢"),
        ("5.9 美国医疗", "不给人医保\n就是安乐死"),
        ("5.10 医疗CEO", "想当医疗\nCEO"),
        ("5.11 38岁半", "给千禧一代\n点期待"),
        ("5.12 半条命", "看了一半\n想继续吗"),
        ("5.13 12个梗", "一个集体\n自杀梗"),
        ("5.14 创作需要", "我创作上\n需要他们"),
        ("5.15 喜剧后果", "现在他们想\n自杀了"),
    ],
    '社会观察': [
        ("6.1 进步语言", "这不好笑"),
        ("6.2 术语", "不好笑了"),
        ("6.3 普选", "我要赢\n普选"),
        ("6.4 中间派伪装", "用中间派\n语言伪装"),
        ("6.5 希特勒", "希特勒也支持\n全民医保"),
        ("6.6 免费大学", "链接到我的\n网站"),
        ("6.7 延迟", "光年前的\n过去"),
        ("6.8 SVU", "全家都能看的\n强奸娈童"),
        ("6.9 尸体", "在滴吗"),
        ("6.10 CSAM", "单手打字\n太长了"),
        ("6.11 邮件", "我刚跟你说了\n别用那词"),
    ]
}

# 创建图形
fig, ax = plt.subplots(1, 1, figsize=(44, 72))
ax.set_xlim(0, 100)
ax.set_ylim(0, 155)
ax.axis('off')

# 标题
ax.text(50, 152, "Tom Segura - Thief of Joy | 笑点结构流程图", 
        fontsize=26, fontweight='bold', ha='center', va='top')
ax.text(50, 149, "106个笑点 | 6个主题 | Callback 与承接关系", fontsize=14, 
        ha='center', va='top', style='italic', color='#555')

# 图例
legend_y = 146
ax.text(8, legend_y, "主题:", fontsize=12, fontweight='bold', va='center')
legend_items = list(themes.keys())
for i, name in enumerate(legend_items):
    color = colors[name]
    rect = FancyBboxPatch((16 + i*13.5, legend_y-1.5), 2.5, 2.5, 
                           boxstyle="round,pad=0.08", 
                           facecolor=color, edgecolor='#333', linewidth=1)
    ax.add_patch(rect)
    ax.text(19 + i*13.5, legend_y-0.2, name, fontsize=10, ha='left', va='center', fontweight='bold')

# 布局参数
y_start = 141
box_width = 13.5
box_height = 4
spacing_x = 15.5
spacing_y = 4.8

# 按列布局 - 6列
columns = list(themes.keys())
x_positions = [3.5, 19, 34.5, 50, 65.5, 81]

# 存储每个框的中心位置用于连线
all_boxes = {}

# 绘制每个主题
for col_idx, theme in enumerate(columns):
    x = x_positions[col_idx]
    color = colors[theme]
    jokes = themes[theme]
    
    # 主题标题
    y_pos = y_start
    ax.text(x + box_width/2, y_pos + 1.5, f"【{theme}】", fontsize=13, 
            fontweight='bold', ha='center', va='bottom', color='#333')
    y_pos -= 2.5
    
    # 绘制每个笑点框
    for i, (title, text) in enumerate(jokes):
        box_y = y_pos - box_height
        
        # 绘制圆角矩形
        rect = FancyBboxPatch((x, box_y), box_width, box_height,
                               boxstyle="round,pad=0.12",
                               facecolor=color, edgecolor='#444', 
                               linewidth=1.2, alpha=0.88)
        ax.add_patch(rect)
        
        # 标题
        ax.text(x + box_width/2, y_pos - 0.6, title, fontsize=9,
                fontweight='bold', ha='center', va='top', color='#222')
        
        # 文本内容
        ax.text(x + box_width/2, y_pos - 1.7, text, fontsize=8,
                ha='center', va='top', color='#333', wrap=True,
                linespacing=1.15)
        
        # 记录位置
        center_x = x + box_width/2
        center_y = y_pos - box_height/2
        all_boxes[title] = (center_x, center_y, theme, i)
        
        y_pos -= spacing_y
        
    # 在主题内画连接箭头（承接关系）
    for i in range(len(jokes) - 1):
        y1 = y_start - 2.5 - box_height/2 - i*spacing_y
        y2 = y1 - spacing_y + box_height + 0.2
        ax.annotate('', xy=(x + box_width/2, y2), 
                   xytext=(x + box_width/2, y1 - 0.3),
                   arrowprops=dict(arrowstyle='->', color='#555', lw=1.2, alpha=0.6))

# 画跨主题的callback连线
# 1.15 糖果 -> 1.16 万圣节
if "1.15 糖果 trick" in all_boxes and "1.16 万圣节 callback" in all_boxes:
    x1, y1, _, _ = all_boxes["1.15 糖果 trick"]
    x2, y2, _, _ = all_boxes["1.16 万圣节 callback"]
    ax.annotate('', xy=(x2, y2 + box_height/2 + 0.3), xytext=(x1, y1 - box_height/2 - 0.3),
               arrowprops=dict(arrowstyle='->', color='#C0392B', lw=1.8, ls='--',
                             connectionstyle="arc3,rad=0.2"))
    mid_x = (x1 + x2) / 2 + 2
    mid_y = (y1 + y2) / 2
    ax.text(mid_x, mid_y, 'callback', fontsize=7, color='#C0392B', rotation=90, va='center')

# 2.13 专场换纹身 -> 标题 Theme Callback
if "2.13 专场换纹身" in all_boxes:
    x1, y1, _, _ = all_boxes["2.13 专场换纹身"]
    ax.annotate('', xy=(x1, y1 - box_height/2 - 0.5), xytext=(50, 152.5),
               arrowprops=dict(arrowstyle='->', color='#C0392B', lw=2, ls='--',
                             connectionstyle="arc3,rad=0.4"))
    ax.text(42, 148, '专场名 callback', fontsize=8, color='#C0392B', fontweight='bold')

# 添加说明
ax.text(50, 1.5, "—— 实线箭头：主题内承接  |  - - - 虚线箭头：跨主题 Callback", 
        fontsize=12, ha='center', style='italic', color='#666')

plt.tight_layout()
plt.savefig('/root/.openclaw/workspace/transcripts/Thief_of_Joy_中文流程图_v2.png', 
            dpi=200, bbox_inches='tight', facecolor='white', edgecolor='none')
print("✅ 中文流程图已生成 (带字体)")

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 主题配色 - 清新色系
colors = {
    '原生家庭': '#7EB5A6',      # 清新青绿
    '恋爱/女友': '#6B9BD1',      # 清新蓝
    '表演生涯': '#90C8AC',      # 薄荷绿
    '性/身体': '#F4D03F',        # 明亮金黄
    '生死/心理': '#F1948A',      # 柔和珊瑚
    '社会观察': '#AED6F1'        # 浅天蓝
}

# 笑点数据 - 按主题分组
themes = {
    '原生家庭': [
        ("1.1 开场钩子", "fucked up family...\nYou needed a professional"),
        ("1.2 Kevin家争吵", "healthiest disagreement\nI ever heard"),
        ("1.3 7天离婚", "first word mama,\nnext five words..."),
        ("1.4 家庭结构", "four half siblings.\nSo two total"),
        ("1.5 36楼烂地基", "fucked up foundation...\n36th floor?"),
        ("1.6 ex-stepdad命名", "German word for man\nwho used to fuck my mom"),
        ("1.7 sugar daddy", "technically makes him\nmy sugar daddy"),
        ("1.8 婚姻建议", "spelling the alphabet\nwith your tongue"),
        ("1.9 妈妈约会", "Just in case you\nwant to fuck my mom"),
        ("1.10 互相伤害", "she's a squirter...\nTwo can play, mommy"),
        ("1.11 前男友不举", "meant his whole body"),
        ("1.12 trolley problem", "original driver for\nthe trolley problem"),
        ("1.13 狗抚养权", "Reggie would prefer\nto be put down"),
        ("1.14 不如狗", "if only I'd been\na Pomeranian"),
        ("1.15 糖果trick", "like a pedophile"),
        ("1.16 万圣节", "overly attached to\nwomen every Halloween"),
        ("1.17 爸爸出轨", "non-ethical non-monogamy"),
        ("1.18 继母儿子", "macaroni necklace...\nfuck my dad?"),
        ("1.19 女友替代妈", "That's what my\ngirlfriend is for"),
        ("1.20 瑜伽反击", "you're a yoga teacher.\nGo fuck yourself"),
        ("1.21 黑料威胁", "canceled with one\nInstagram post"),
        ("1.22 爸爸帅", "your dad's really\ngood looking"),
        ("1.23 收养谣言", "my dad started it"),
        ("1.24 手工课老师", "those grades don't matter"),
        ("1.25 意大利家训", "Male tua madre...\nnice ring to it"),
        ("1.26 遗嘱", "just like when\nyou were alive"),
        ("1.27 Venmo", "sent my dad\na Venmo request"),
        ("1.28 Epstein", "reminds me of\nJeffrey Epstein"),
        ("1.29 劳动价值", "It's called capitalism,\nsweetheart"),
        ("1.30 非法移民", "not taking the jobs\nany of us want"),
        ("1.31 假心脏骤停", "pretended to go into\ncardiac arrest"),
        ("1.32 DraftKings", "placed our bets"),
        ("1.33 手术成功", "someone is delivering\nhis next girlfriend"),
        ("1.34 试镜梗", "auditioned to\nplay the son"),
    ],
    '恋爱/女友': [
        ("2.1 免责声明", "let's just call her women"),
        ("2.2 犹太女友", "Women are Jewish"),
        ("2.3 Hasidic", "finish that before\nyou buy the costume"),
        ("2.4 免责声明2", "I don't see noses"),
        ("2.5 文化犹太人", "without the sweet\ncomfort of God"),
        ("2.6 逾越节", "from heroes to frail"),
        ("2.7 迈阿密", "Jews exaggerating\nentire time?"),
        ("2.8 6百万人", "let my people go...\n6 million people"),
        ("2.9 友谊秘诀", "hating gay people"),
        ("2.10 第一任关系", "you're my person...\nlast but not least"),
        ("2.11 星巴克分手", "shouldn't have brought\nan audience"),
        ("2.12 纹身Larry", "my dead friend, Larry"),
        ("2.13 专场换纹身", "if that doesn't\nwin Laura back"),
        ("2.14 peg", "stopped trying to\npeg me"),
        ("2.15 夜惊症", "only victim of both\nour disorders"),
        ("2.16 强奸犯类比", "like a rapist asking..."),
        ("2.17 孩子反问", "What do you plan on\ndoing with your remains?"),
        ("2.18 袋鼠", "like asking for\na kangaroo"),
        ("2.19 狼人", "dating a werewolf\ninjecting the moon"),
        ("2.20 科学奇迹", "scientific miracles\nfor a woman to work"),
        ("2.21 胚胎裁决", "mother of 19"),
        ("2.22 镜子床", "proving she's taking\nmore than half"),
        ("2.23 看片搜索", "women who look\nlike my girlfriend"),
    ],
    '表演生涯': [
        ("3.1 剧场孩子", "deaf people: shut up"),
        ("3.2 变装比赛", "John Mulaney...\naddicted to stage"),
        ("3.3 音乐剧学位", "PhD in imagination"),
        ("3.4 会计课", "how to file\nfor unemployment"),
        ("3.5 triple threat", "Threat three:\nI'm annoying"),
        ("3.6 20万学费", "That joke cost\nme $200,000"),
        ("3.7 华尔街之狼", "waiter for 12 years"),
        ("3.8 extra work", "furniture,\nbut with dreams"),
        ("3.9 靠近梦想", "getting fucked by\nLeonardo DiCaprio"),
        ("3.10 首演夜", "daffodils...\ndad is allergic"),
    ],
    '性/身体': [
        ("4.1 legs guy", "only way to measure\nlegs in this country"),
        ("4.2 英尺荒谬", "some guy's foot once"),
        ("4.3 马用手", "Feet, hands...\ntried cocks?"),
        ("4.4 阴茎测量史", "that's how we\ngot the centimeter"),
        ("4.5 6英寸", "All I ever wanted"),
        ("4.6 美元钞票", "dick slapping\nGeorge Washington"),
        ("4.7 华盛顿", "cannot tell a lie.\nYou're a buck short"),
        ("4.8 特朗普", "he'd be like, 'huge'"),
        ("4.9 高中剧场", "whose dick do I have\nto suck to get pussy?"),
        ("4.10 NYU三人行", "I'm straight but\nI can make you feel..."),
        ("4.11 口交技巧", "Spider-Man,\nstep team"),
        ("4.12 孤独时刻", "I am so lonely.\nBlackout"),
        ("4.13 谣言受益", "never gotten so\nmuch pussy"),
    ],
    '生死/心理': [
        ("5.1 自杀开头", "no good arguments?"),
        ("5.2 地狱", "You'll go to hell"),
        ("5.3 宗教理解", "something worse\nthan staying alive"),
        ("5.4 免责声明", "none of them\nare here tonight"),
        ("5.5 自杀短信", "I love you,\nI'm sorry, goodbye"),
        ("5.6 语音信箱", "update your voicemail"),
        ("5.7 通灵师", "Why kill myself\nbefore I'm a movie star?"),
        ("5.8 867-5309", "I'm great,\nhow are you?"),
        ("5.9 美国医疗", "not giving\npeople healthcare"),
        ("5.10 医疗CEO", "become a\nhealthcare CEO"),
        ("5.11 38岁半", "give millennials\nsomething to look forward"),
        ("5.12 生命预期", "you've seen half,\nwant to continue?"),
        ("5.13 12个梗", "one mass\nsuicide joke"),
        ("5.14 创作需要", "I need them\ncreatively"),
        ("5.15 喜剧演员", "So now they\nwant to kill themselves"),
    ],
    '社会观察': [
        ("6.1 进步语言", "that's not funny"),
        ("6.2 术语", "stopped\ngetting laughs"),
        ("6.3 反击", "I have to win\nthe popular vote"),
        ("6.4 左派伪装", "disguised in\ncentrist language"),
        ("6.5 Bernie", "Adolf Hitler...\nnot for everybody"),
        ("6.6 免费大学", "link to\nmy website"),
        ("6.7 喜剧延迟", "light years\nin the past"),
        ("6.8 SVU", "fun for the\nwhole family"),
        ("6.9 尸体反应", "Is it fucking dripping?"),
        ("6.10 CSAM", "lot to type\nwith one hand"),
        ("6.11 邮件", "what the fuck did I\njust tell you?"),
    ]
}

# 创建图形
fig, ax = plt.subplots(1, 1, figsize=(48, 72))
ax.set_xlim(0, 100)
ax.set_ylim(0, 150)
ax.axis('off')

# 标题
ax.text(50, 147, "Tom Segura - Thief of Joy", fontsize=32, fontweight='bold', 
        ha='center', va='top')
ax.text(50, 144, "笑点结构流程图 | Joke Structure Flowchart", fontsize=18, 
        ha='center', va='top', style='italic', color='#555')

# 图例
legend_y = 141
ax.text(5, legend_y, "Legend:", fontsize=14, fontweight='bold')
legend_items = [
    ('原生家庭', colors['原生家庭']),
    ('恋爱/女友', colors['恋爱/女友']),
    ('表演生涯', colors['表演生涯']),
    ('性/身体', colors['性/身体']),
    ('生死/心理', colors['生死/心理']),
    ('社会观察', colors['社会观察']),
]
for i, (name, color) in enumerate(legend_items):
    rect = FancyBboxPatch((15 + i*13, legend_y-1.5), 3, 2.5, 
                           boxstyle="round,pad=0.1", 
                           facecolor=color, edgecolor='#333', linewidth=1)
    ax.add_patch(rect)
    ax.text(18.5 + i*13, legend_y-0.2, name, fontsize=10, ha='left', va='center')

# 布局参数
y_start = 135
box_width = 18
box_height = 3.5
spacing_x = 20
spacing_y = 4.5

# 按列布局 - 每列一个主题
columns = list(themes.keys())
x_positions = [5, 22, 39, 56, 73, 90]  # 6列，对应6个主题

# 绘制每个主题
callbacks = []
for col_idx, theme in enumerate(columns):
    x = x_positions[col_idx]
    color = colors[theme]
    jokes = themes[theme]
    
    # 主题标题
    y_pos = y_start
    ax.text(x + box_width/2, y_pos + 2, f"【{theme}】", fontsize=16, 
            fontweight='bold', ha='center', va='bottom', color='#333')
    y_pos -= 3
    
    # 绘制每个笑点框
    box_positions = []  # 记录位置用于连线
    for i, (title, text) in enumerate(jokes):
        # 绘制圆角矩形
        rect = FancyBboxPatch((x, y_pos - box_height), box_width, box_height,
                               boxstyle="round,pad=0.15",
                               facecolor=color, edgecolor='#333', 
                               linewidth=1.5, alpha=0.85)
        ax.add_patch(rect)
        
        # 标题
        ax.text(x + box_width/2, y_pos - 0.6, title, fontsize=10,
                fontweight='bold', ha='center', va='top', color='#222')
        
        # 文本内容
        ax.text(x + box_width/2, y_pos - 1.8, text, fontsize=8,
                ha='center', va='top', color='#444', wrap=True,
                linespacing=1.3)
        
        box_positions.append((x + box_width/2, y_pos - box_height/2, title))
        y_pos -= spacing_y
        
        # 检查是否需要callback
        if '万圣节' in title or '糖果' in title:
            callbacks.append((title, x + box_width/2, y_pos + spacing_y - box_height/2))
    
    # 在主题内画连接箭头（表示承接）
    for i in range(len(box_positions) - 1):
        x1, y1, _ = box_positions[i]
        x2, y2, _ = box_positions[i + 1]
        arrow = FancyArrowPatch((x1, y1 - box_height/2), (x2, y2 + box_height/2),
                               arrowstyle='->', mutation_scale=15, 
                               color='#666', linewidth=1, alpha=0.6)
        ax.add_patch(arrow)

# 画跨主题的callback连线
# 1.15 糖果 -> 1.16 万圣节
ax.annotate('', xy=(8 + box_width/2, 135 - 3 - 14*spacing_y + box_height/2),
            xytext=(8 + box_width/2, 135 - 3 - 15*spacing_y + box_height/2 + 2),
            arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=2, ls='--'))
ax.text(8 + box_width/2 + 1, 135 - 3 - 14.5*spacing_y, 'callback', 
        fontsize=8, color='#E74C3C', rotation=90, va='center')

# 2.17 专场 -> 标题 Thief of Joy 的主题callback
ax.annotate('', xy=(28 + box_width/2, 135 - 3 - 12*spacing_y + box_height/2),
            xytext=(50, 145),
            arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=2, ls='--',
                          connectionstyle="arc3,rad=0.3"))
ax.text(40, 140, 'theme callback', fontsize=8, color='#E74C3C')

# 添加说明
ax.text(50, 5, "→ 实线箭头：承接关系 | → 虚线箭头：Callback 呼应 | 颜色：主题分区", 
        fontsize=12, ha='center', style='italic', color='#666')

plt.tight_layout()
plt.savefig('/root/.openclaw/workspace/transcripts/Thief_of_Joy_Flowchart.png', 
            dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
print("✅ 流程图已生成: Thief_of_Joy_Flowchart.png")

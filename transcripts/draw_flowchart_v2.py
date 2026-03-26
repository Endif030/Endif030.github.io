import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# 设置字体
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# 主题配色 - 清新色系
colors = {
    'Family': '#7EB5A6',      # 青绿
    'GF/Jewish': '#6B9BD1',   # 蓝
    'Career': '#90C8AC',      # 薄荷绿
    'Sex/Body': '#F4D03F',    # 金黄
    'Death': '#F1948A',       # 珊瑚
    'Social': '#AED6F1'       # 天蓝
}

# 简化版笑点数据 - 按主题分组
themes = {
    'Family': [
        ("1.1 Opening", "fucked up family...\nYou needed a professional"),
        ("1.2 Kevin's house", "healthiest disagreement\nI ever heard"),
        ("1.3 7-day divorce", "first word mama,\nnext five words..."),
        ("1.4 Family math", "four half siblings.\nSo two total"),
        ("1.5 36th floor", "fucked up foundation...\n36th floor?"),
        ("1.6 Ex-stepdad", "German word for man\nwho used to fuck my mom"),
        ("1.7 Sugar daddy", "technically makes him\nmy sugar daddy"),
        ("1.8 Marriage advice", "spelling alphabet\nwith your tongue"),
        ("1.9 Mom dating", "in case you want\nto fuck my mom"),
        ("1.10 Mutual roast", "she's a squirter...\nTwo can play, mommy"),
        ("1.11 Ex-boyfriend", "meant his whole body"),
        ("1.12 Trolley problem", "original driver for\nthe trolley problem"),
        ("1.13 Dog custody", "Reggie would prefer\nto be put down"),
        ("1.14 Pomeranian", "if only I'd been\na Pomeranian"),
        ("1.15 Candy trick", "like a pedophile"),
        ("1.16 Halloween", "overly attached to\nwomen every Halloween"),
        ("1.17 Dad cheating", "non-ethical\nnon-monogamy"),
        ("1.18 Stepmom's son", "macaroni necklace...\nfuck my dad?"),
        ("1.19 GF replaces mom", "That's what my\ngirlfriend is for"),
        ("1.20 Yoga clapback", "you're a yoga teacher.\nGo fuck yourself"),
        ("1.21 Cancel threat", "canceled with one\nInstagram post"),
        ("1.22 Hot dad", "your dad's really\ngood looking"),
        ("1.23 Adoption rumor", "my dad started it"),
        ("1.24 Arts teacher", "those grades\ndon't matter"),
        ("1.25 Italian dad", "Male tua madre...\nnice ring to it"),
        ("1.26 Will testament", "just like when\nyou were alive"),
        ("1.27 Venmo", "sent my dad\na Venmo request"),
        ("1.28 Epstein", "reminds me of\nJeffrey Epstein"),
        ("1.29 Capitalism", "It's called capitalism,\nsweetheart"),
        ("1.30 Immigrants", "not taking jobs\nwe want to do"),
        ("1.31 Fake arrest", "pretended cardiac\narrest"),
        ("1.32 DraftKings", "placed our bets"),
        ("1.33 Surgery success", "delivering his\nnext girlfriend"),
        ("1.34 Audition", "auditioned to\nplay the son"),
    ],
    'GF/Jewish': [
        ("2.1 Disclaimer", "let's just call\nher 'women'"),
        ("2.2 Women=Jewish", "Women are Jewish"),
        ("2.3 Hasidic", "finish that before\nyou buy costume"),
        ("2.4 I don't see noses", "I don't see noses"),
        ("2.5 Cultural Jew", "without sweet\ncomfort of God"),
        ("2.6 Passover", "heroes to frail"),
        ("2.7 Miami", "Jews exaggerating\nentire time?"),
        ("2.8 6 million", "let my people go...\n6 million people"),
        ("2.9 Friendship key", "hating gay people"),
        ("2.10 My person", "you're my person...\nlast but not least"),
        ("2.11 Starbucks", "shouldn't have\nbrought audience"),
        ("2.12 Tattoo Larry", "my dead friend,\nLarry"),
        ("2.13 Special deal", "if that doesn't\nwin Laura back"),
        ("2.14 Pegging", "stopped trying\nto peg me"),
        ("2.15 Night terrors", "victim of both\nour disorders"),
        ("2.16 Rapist analogy", "like a rapist\nasking..."),
        ("2.17 Kids question", "doing with\nyour remains?"),
        ("2.18 Kangaroo", "like asking\nfor a kangaroo"),
        ("2.19 Werewolf", "dating werewolf\ninjecting the moon"),
        ("2.20 Science miracles", "miracles for woman\nto have career"),
        ("2.21 Alabama ruling", "mother of 19"),
        ("2.22 Mirror bed", "she's taking\nmore than half"),
        ("2.23 Porn search", "women who look\nlike my girlfriend"),
    ],
    'Career': [
        ("3.1 Theater kid", "deaf people:\nshut the fuck up"),
        ("3.2 Drag show", "John Mulaney...\naddicted to stage"),
        ("3.3 Musical degree", "PhD in imagination"),
        ("3.4 Accounting", "file for\nunemployment"),
        ("3.5 Triple threat", "Threat three:\nI'm annoying"),
        ("3.6 $200k", "That joke cost\nme $200,000"),
        ("3.7 Wolf of WS", "waiter for\n12 years"),
        ("3.8 Extra work", "furniture,\nbut with dreams"),
        ("3.9 So close", "getting fucked by\nLeonardo DiCaprio"),
        ("3.10 Opening night", "daffodils...\ndad is allergic"),
    ],
    'Sex/Body': [
        ("4.1 Legs guy", "measure legs\nin this country"),
        ("4.2 Feet system", "some guy's foot"),
        ("4.3 Horses", "Feet, hands...\ntried cocks?"),
        ("4.4 Centimeter", "how we got\nthe centimeter"),
        ("4.5 6 inches", "All I ever wanted"),
        ("4.6 Dollar bill", "dick slapping\nWashington"),
        ("4.7 Washington", "cannot tell lie.\nYou're a buck short"),
        ("4.8 Trump", "he'd be like,\n'huge'"),
        ("4.9 High school", "whose dick to suck\nto get pussy?"),
        ("4.10 NYU 3-way", "I'm straight but\nI can make you..."),
        ("4.11 Techniques", "Spider-Man,\nstep team"),
        ("4.12 Lonely", "I am so lonely.\nBlackout"),
        ("4.13 Rumor bonus", "never gotten so\nmuch pussy"),
    ],
    'Death': [
        ("5.1 Suicide", "no good arguments?"),
        ("5.2 Hell", "You'll go to hell"),
        ("5.3 Religion", "worse than\nstaying alive"),
        ("5.4 Disclaimer", "none of them\nare here tonight"),
        ("5.5 Text", "I love you,\ngoodbye"),
        ("5.6 Voicemail", "update your\nvoicemail"),
        ("5.7 Psychic", "before I'm\na movie star?"),
        ("5.8 867-5309", "I'm great,\nhow are you?"),
        ("5.9 US healthcare", "not giving\npeople healthcare"),
        ("5.10 CEO", "become a\nhealthcare CEO"),
        ("5.11 38.5 years", "millennials\nlook forward"),
        ("5.12 Half life", "seen half,\nwant to continue?"),
        ("5.13 12 jokes", "one mass\nsuicide joke"),
        ("5.14 Creative need", "I need them\ncreatively"),
        ("5.15 Comedy result", "now they want\nto kill themselves"),
    ],
    'Social': [
        ("6.1 Progressive", "that's not funny"),
        ("6.2 Terminology", "stopped\ngetting laughs"),
        ("6.3 Popular vote", "win the\npopular vote"),
        ("6.4 Centrist", "disguised in\ncentrist language"),
        ("6.5 Bernie", "Hitler...\nnot for everybody"),
        ("6.6 Free college", "link to\nmy website"),
        ("6.7 Delay", "light years\nin the past"),
        ("6.8 SVU", "fun for the\nwhole family"),
        ("6.9 Dead body", "Is it dripping?"),
        ("6.10 CSAM", "lot to type\nwith one hand"),
        ("6.11 Email", "what the fuck did I\njust tell you?"),
    ]
}

# 创建更大的图形
fig, ax = plt.subplots(1, 1, figsize=(40, 64))
ax.set_xlim(0, 100)
ax.set_ylim(0, 160)
ax.axis('off')

# 标题
ax.text(50, 157, "Tom Segura - Thief of Joy | Joke Structure Flowchart", 
        fontsize=28, fontweight='bold', ha='center', va='top')
ax.text(50, 154, "106 Jokes | 6 Themes | Callbacks & Connections", fontsize=16, 
        ha='center', va='top', style='italic', color='#555')

# 图例
legend_y = 151
legend_items = [
    ('Family', colors['Family']),
    ('GF/Jewish', colors['GF/Jewish']),
    ('Career', colors['Career']),
    ('Sex/Body', colors['Sex/Body']),
    ('Death/Mental', colors['Death']),
    ('Social', colors['Social']),
]
for i, (name, color) in enumerate(legend_items):
    rect = FancyBboxPatch((12 + i*14, legend_y-2), 3, 3, 
                           boxstyle="round,pad=0.1", 
                           facecolor=color, edgecolor='#333', linewidth=1)
    ax.add_patch(rect)
    ax.text(15.5 + i*14, legend_y-0.5, name, fontsize=11, ha='left', va='center', fontweight='bold')

# 布局参数 - 更大的盒子
y_start = 146
box_width = 14
box_height = 4.2
spacing_x = 16
spacing_y = 5.2

# 按列布局
columns = list(themes.keys())
x_positions = [5, 21, 37, 53, 69, 85]

# 绘制每个主题
for col_idx, theme in enumerate(columns):
    x = x_positions[col_idx]
    color = colors[theme]
    jokes = themes[theme]
    
    # 主题标题
    y_pos = y_start
    ax.text(x + box_width/2, y_pos + 2, theme, fontsize=14, 
            fontweight='bold', ha='center', va='bottom', color='#333')
    y_pos -= 3
    
    # 绘制每个笑点框
    for i, (title, text) in enumerate(jokes):
        # 绘制圆角矩形
        rect = FancyBboxPatch((x, y_pos - box_height), box_width, box_height,
                               boxstyle="round,pad=0.15",
                               facecolor=color, edgecolor='#333', 
                               linewidth=1.5, alpha=0.85)
        ax.add_patch(rect)
        
        # 标题 - 更大
        ax.text(x + box_width/2, y_pos - 0.7, title, fontsize=10,
                fontweight='bold', ha='center', va='top', color='#222')
        
        # 文本内容 - 更大
        ax.text(x + box_width/2, y_pos - 2.0, text, fontsize=9,
                ha='center', va='top', color='#444', wrap=True,
                linespacing=1.2)
        
        y_pos -= spacing_y
        
    # 在主题内画连接箭头（表示承接）
    y_pos = y_start - 3 - box_height/2
    for i in range(len(jokes) - 1):
        y1 = y_pos - i*spacing_y
        y2 = y_pos - (i+1)*spacing_y + box_height + 0.3
        ax.annotate('', xy=(x + box_width/2, y2), xytext=(x + box_width/2, y1),
                   arrowprops=dict(arrowstyle='->', color='#666', lw=1.2, alpha=0.5))

# 画跨主题的callback连线（简化版）
# 1.15 Candy -> 1.16 Halloween (within Family, already connected)
# 2.13 Special -> Title (arc)
ax.annotate('', xy=(21 + box_width/2, 146 - 3 - 12*spacing_y + box_height/2),
            xytext=(50, 155),
            arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=2.5, ls='--',
                          connectionstyle="arc3,rad=0.3"))
ax.text(36, 151, 'THEME CALLBACK', fontsize=9, color='#E74C3C', fontweight='bold')

# 添加说明
ax.text(50, 2, "→ Solid arrows: Sequential flow  |  → Dashed arrows: Callback connections", 
        fontsize=14, ha='center', style='italic', color='#666')
ax.text(50, 0.5, "Thief of Joy = Special title callback from joke 2.13", 
        fontsize=11, ha='center', color='#E74C3C')

plt.tight_layout()
plt.savefig('/root/.openclaw/workspace/transcripts/Thief_of_Joy_Flowchart_v2.png', 
            dpi=200, bbox_inches='tight', facecolor='white', edgecolor='none')
print("✅ Optimized flowchart saved: Thief_of_Joy_Flowchart_v2.png")

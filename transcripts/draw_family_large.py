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

# 原生家庭主题的详细笑点数据
family_jokes = [
    ("1.1 开场钩子", "我来自一个 messed up 的家庭。我知道这并不会让我在这个房间里显得特别。我猜你们大多数人也都来自 messed up 的家庭，因为想想看，来自健康家庭的人，他们在外面。和朋友们一起欢笑。但不，不是你们。你们需要专业人士（needed a professional）。"),
    ("1.2 Kevin家的健康争吵", "当你还是个孩子的时候，你不会意识到你的家庭 messed up，因为那就是你所知道的一切。对我来说，那是七年级。我在朋友 Kevin 家过夜，Kevin 的爸爸走进客厅说：嘿，今晚谁想看《加勒比海盗》？然后 Kevin 的妈妈跑进来，说：绝对不行，那对他们来说太成熟了。Kevin 爸爸说：但我真的很想看。Kevin 妈妈说：我想你会没事的 Kirk。然后 Kevin 说：我很抱歉让你看到这一幕。那是我听过的最健康的争吵（healthiest disagreement）。"),
    ("1.3 父母7天大离婚", "我父母在我出生七天的时候就离婚了。所以像大多数孩子一样，我的第一个词是妈妈（mama），但我的接下来五个字（next five words），是她让我告诉你的（told me to tell you）。\n【梗：mama + next five words 连读像是 mama told me to tell you】"),
    ("1.4 家庭结构混乱", "我妈离过两次婚，我爸离过三次婚，我有四个同父异母的弟弟妹妹（four younger half siblings）。所以总共两个（So two total）。\n【梗：四个同父异母，但从完整家庭角度算两个】"),
    ("1.5 36楼烂地基", "我现在36岁了。很多人都觉得，到了36岁，你应该停止把你所有的问题都归咎于父母了。好吧，让我问你这个问题：如果你在一栋地基烂掉的楼（fucked up foundation）里，你觉得在36层（36th floor）会更安全吗？是的，我也不这么认为。"),
    ("1.6 ex-stepdad的尴尬命名", "上个月我和前继父一起吃饭。这种关系没有一个方便的称呼，因为它本不应该存在。我不知道哪个更好：前继父（former stepdad），还是那个下台的父亲（the dad who stepped down）。我敢肯定德语里一定有个词来形容一个曾经操我妈的男人。"),
    ("1.7 ex-stepdad是sugar daddy", "我们仍然花时间在一起的唯一原因是他为每顿饭买单，从技术上讲，这让他成为我的糖爹（sugar daddy），如果非要这么说的话。"),
    ("1.8 给继父的婚姻建议", "我记得有一次在高中，我继父开车送我。他们肯定刚吵过架，因为他问我：我怎么才能让你妈妈开心？但在那个年龄，我对女人的唯一了解来自互联网。所以我说：我不知道。你试过用舌头拼字母表吗（spelling the alphabet with your tongue）？我延长了那段婚姻六年。"),
    ("1.9 妈妈在eHarmony", "但他们现在离婚了。现在我妈在 eHarmony 上。万一你也想操我妈呢（Just in case you want to fuck my mom）。"),
    ("1.10 妈妈的约会反馈", "她最近和一个男人约会。我问她，约会怎么样？她说：这么说吧，我们在身体上很兼容（physically compatible）。我说：这么说吧，下次别说了。怎么样？"),
    ("1.11 和妈妈的互相伤害", "然后她问我，你女朋友怎么样？我说：嗯，她是个喷子（she's a squirter），但我们还能维持（keeping afloat）。互相伤害啊，妈咪（Two can play this game, mommy）。"),
    ("1.12 妈妈只约会年长男性", "我妈只约会比她年长的男人。所以她很快就快没选择了（running out of options）。"),
    ("1.13 前男友不举", "她向我抱怨她上一个男朋友硬不起来（couldn't get it up）。当我见到他时，我意识到她指的是他的整个身体。\n【梗：get it up 通常指勃起，但这里指全身瘫痪】"),
    ("1.14 有钱老男友的电车难题", "她和一个男人约会。我真的很喜欢这个男人，因为他很有钱。我猜他就是电车难题（trolley problem）的原版司机。\n【梗：为了钱可以牺牲母亲，就像电车难题中选择撞谁】"),
    ("1.15 狗的共同抚养", "分手非常复杂，因为他们一起领养了一只狗。这只可爱的小狗叫 Reggie。我妈告诉我，他们决定尝试共同抚养（shared custody）这只狗。我告诉她，我说：我敢肯定 Reggie 宁愿被安乐死（prefer to be put down）。"),
    ("1.16 Reggie的焦虑和妈妈约会", "但她说，他们这样做是为了 Reggie。我妈说，她注意到每当她约会后带新男人回公寓时，Reggie 都会变得非常焦虑和不舒服（anxious and uncomfortable）。所以现在她只在 Reggie 去他爸爸家时才去约会。我说：哦，我要是只博美犬（Pomeranian）就好了。"),
    ("1.17 爸爸的糖果trick", "我爸经常约会。经常到他都有技巧了。每当他把新女人带进我的生活时，首先他会去 CVS，买一大堆糖果（shitload of candy）。他会把糖果给那个女人，然后她再给我。所以我就会自动信任她，你知道，就像恋童癖一样（like a pedophile）。"),
    ("1.18 万圣节后遗症", "而且这招很管用。我到现在每到万圣节（Halloween）还会对女人过度依恋（overly attached）。\n【callback：承接上一条糖果梗，万圣节会收到糖果】"),
    ("1.19 爸爸出轨的术语", "但每段关系都会结束，因为我爸会出轨。他相信的现在应该叫做非伦理非一夫一妻制（non-ethical non-monogamy）。我们当时不用这些术语。相反，他说：她疯了，儿子（she just went crazy, son）。"),
    ("1.20 遇到ex-stepmom", "我小时候我爸再婚了，我和继母很亲近。当然，我们年龄相仿。我们离婚后没有保持联系，但几年前，我在一家杂货店。我转进麦片 aisle，看到我前继母（ex-step-mom）和一个小男孩一起挑麦片。感觉就像遇到了前女友（running into an ex-girlfriend）。"),
    ("1.21 对继母新儿子的嫉妒", "说实话，我当时就想：Belinda，这他妈是谁（who the fuck is this）？她说：这是我儿子 Tommy。我说：嘿，伙计。她还戴着我母亲节给她做的通心粉项链（macaroni necklace）吗？还是你只是在假装它很漂亮好操我爸？我希望你喜欢二手货，你这个小婊子（you little bitch）。"),
    ("1.22 女友替代妈妈", "我有两个继母，我和她们都很亲近，但方式不同。我从来没有把她们看作是我亲生母亲的替代品（replacement）。那是我女朋友的作用（That's what my girlfriend is for）。"),
    ("1.23 妈妈当瑜伽老师反击", "当我对事业感到沮丧时，我妈会对我说：你是个演员（you're an actor）。你为什么不演得不那么沮丧呢（act like you're not depressed）？\n所以我说：妈，你是个瑜伽老师（you're a yoga teacher）。你为什么不自己去操自己呢（go fuck yourself）？"),
    ("1.24 妈妈握有黑料", "我讲太多关于我妈的笑话时要小心，因为她还留着我高中《一千零一夜》（Arabian Nights）演出的所有照片。她可以用一条 Instagram 帖子 cancel 我。如果我太过分，她只会打：你永远是我的小阿里巴巴（you'll always be my little Alibaba）。"),
    ("1.25 爸爸长得帅", "我觉得如果你知道我爸也很帅（hot），他的很多行为就更有意义了。我知道我说这个听起来很奇怪，但操你。我必须面对这个。人们见到我爸，他们会说：你爸真帅（your dad's really good looking）。好像我欠他们一个解释似的（Like I owe them an explanation）。"),
    ("1.26 爸爸传谣言", "我记得我爸有一次来初中接我——我的意思是就一次（I mean once）——然后我年级里就开始传谣言说我一定是领养的（adopted）。这真的很伤人，因为那是我爸传的谣言。"),
    ("1.27 爸爸睡了手工课老师", "这是真事。我爸，我爸曾经睡了我八年级的艺术和手工老师（arts and crafts teacher）。我非常生气，因为那些成绩不重要（those grades don't matter）。"),
    ("1.28 要求爸爸睡代数老师", "他觉得很愧疚。他说：我怎么才能补偿你？我说：你可以操我78岁的代数老师 Breyer 先生（Mr. Breyer）。"),
    ("1.29 意大利爸爸的家训", "我爸是意大利人。所以他总是告诉我：儿子，记住，la famiglia è tutto（家庭就是一切）。Male tua madre è una puttana（你妈妈是婊子）。\n我现在还是不知道第二部分是什么意思，但听起来真好听（nice ring to it）。"),
    ("1.30 爸爸心脏病-遗嘱事件", "去年我爸心脏病发作。他想让我下去，好让我看看他的遗嘱（will）。他说：我想让你知道，如果在我到之前出了什么事，我会在你所有演出中以 spirit 的形式出现。我说：哦，就像你生前一样（just like when you were alive）。"),
    ("1.31 Venmo请求", "所以我买了下一班飞机。我给我爸发了一个 Venmo 请求（Venmo request）。"),
    ("1.32 爸爸的新女友年龄差", "我爸对我说：儿子，你不明白，当我约会同龄的女人时，这让我想起我的死亡（mortality）。我说：好吧，当我看到你约会的女人时，这让我想起 Jeffrey Epstein。"),
    ("1.33 爸爸把遗产给新女友", "他想向全家宣布，他要把三分之一的遗产（a third of his estate）给这个新女友。我能看出我妹妹很生气。所以我低声对她说：现在你知道你出生的时候我是什么感受了（now you know how I felt when you were born）。"),
    ("1.34 爸爸的劳动价值论", "我不得不向她解释：亲爱的，我爸71岁了。如果你给一个71岁的人吹箫（suck a 71 year old's dick），你就能进遗嘱。这叫资本主义（capitalism），亲爱的。我们在干嘛呢？"),
]

# 创建图形 - 更大的画布
fig, ax = plt.subplots(1, 1, figsize=(20, 180))
ax.set_xlim(0, 60)
ax.set_ylim(0, 360)
ax.axis('off')

# 标题 - 更大字体
title_y = 356
ax.text(30, title_y, "【原生家庭】主题笑点详解", fontsize=48, fontweight='bold', ha='center', va='top', color='#1A5276')
ax.text(30, title_y - 6, "Tom Segura - Thief of Joy | 共34个笑点", fontsize=28, ha='center', va='top', color='#2874A6')
ax.text(30, title_y - 12, "括号内为英文原文 | 蓝色箭头=承接 | 红色虚线=Callback", fontsize=18, ha='center', va='top', color='#5D6D7E', style='italic')

# 布局参数 - 更大的模块和字体
box_width = 54
x_center = 30
y_start = title_y - 20
line_height = 0.9  # 每行文字高度
char_per_line = 32  # 每行字符数

# 计算每个模块的实际高度
module_data = []
y_pos = y_start

for joke_id, joke_title, joke_text in [(j[0].split()[0], j[0].split()[1], j[1]) for j in family_jokes]:
    # 计算标题高度
    title_height = 1.5
    
    # 计算文本需要多少行
    text_len = len(joke_text)
    lines_needed = max(3, text_len // char_per_line + joke_text.count('\n') + 2)
    text_height = lines_needed * line_height + 1
    
    # 总高度
    total_height = title_height + text_height + 0.5
    
    # 记录数据
    module_data.append({
        'id': joke_id,
        'title': joke_title,
        'text': joke_text,
        'y_top': y_pos,
        'y_bottom': y_pos - total_height,
        'height': total_height,
        'x_center': x_center
    })
    
    # 更新下一个模块的顶部位置（加上间距）
    y_pos = y_pos - total_height - 2

# 绘制每个模块
for i, mod in enumerate(module_data):
    # 绘制圆角矩形
    rect = FancyBboxPatch((mod['x_center'] - box_width/2, mod['y_bottom']), box_width, mod['height'],
                           boxstyle="round,pad=0.2",
                           facecolor='#A2D9CE', edgecolor='#1A5276', 
                           linewidth=4, alpha=0.95)
    ax.add_patch(rect)
    
    # 编号和标题 - 放大两倍的字体
    ax.text(mod['x_center'] - box_width/2 + 1, mod['y_top'] - 1, f"{mod['id']} {mod['title']}", 
            fontsize=22, fontweight='bold', ha='left', va='top', color='#154360')
    
    # 文本内容 - 放大两倍的字体
    ax.text(mod['x_center'] - box_width/2 + 1, mod['y_top'] - 3, mod['text'], fontsize=18,
            ha='left', va='top', color='#1A5276', wrap=True,
            linespacing=1.5)

# 画承接箭头 - 连接模块底部到下一个模块顶部
for i in range(len(module_data) - 1):
    current = module_data[i]
    next_mod = module_data[i + 1]
    
    # 从当前模块底部向下0.5，连接到下一个模块顶部向上0.5
    ax.annotate('', 
               xy=(next_mod['x_center'], next_mod['y_top'] + 0.5), 
               xytext=(current['x_center'], current['y_bottom'] - 0.5),
               arrowprops=dict(arrowstyle='->', color='#2980B9', lw=4,
                             connectionstyle="arc3,rad=0"))

# 标注callback关系 (1.17 到 1.18)
callback_idx_17 = 16  # 1.17
callback_idx_18 = 17  # 1.18

mod_17 = module_data[callback_idx_17]
mod_18 = module_data[callback_idx_18]

ax.annotate('', 
           xy=(mod_18['x_center'] + box_width/2 - 3, mod_18['y_top'] + 1), 
           xytext=(mod_17['x_center'] + box_width/2 - 3, mod_17['y_bottom'] - 1),
           arrowprops=dict(arrowstyle='->', color='#C0392B', lw=5, ls='--',
                         connectionstyle="arc3,rad=0.2"))
ax.text(mod_17['x_center'] + box_width/2 + 2, (mod_17['y_bottom'] + mod_18['y_top'])/2, 'callback', 
        fontsize=14, color='#C0392B', fontweight='bold', rotation=90, va='center')

# 添加说明
ax.text(30, 3, "—— 蓝色实线：承接关系  |  红色虚线：Callback 呼应  |  （）内为英文原文", 
        fontsize=18, ha='center', style='italic', color='#555')

plt.tight_layout()
plt.savefig('/root/.openclaw/workspace/transcripts/Thief_of_Joy_原生家庭_大字版.png', 
            dpi=200, bbox_inches='tight', facecolor='white', edgecolor='none')
print("✅ 大字版原生家庭主题图已生成")
print(f"模块数量: {len(module_data)}")

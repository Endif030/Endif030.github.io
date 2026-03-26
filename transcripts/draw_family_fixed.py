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

# 原生家庭主题的详细笑点数据（含完整中文译文+必要的英文原文）
family_jokes = [
    {
        "id": "1.1",
        "title": "开场钩子",
        "text": "我来自一个 messed up 的家庭。我知道这并不会让我在这个房间里显得特别。我猜你们大多数人也都来自 messed up 的家庭，因为想想看，来自健康家庭的人，他们在外面。和朋友们一起欢笑。但不，不是你们。你们需要专业人士（needed a professional）。"
    },
    {
        "id": "1.2", 
        "title": "Kevin家的健康争吵",
        "text": "当你还是个孩子的时候，你不会意识到你的家庭 messed up，因为那就是你所知道的一切。但然后会有一个时刻，你意识到一切都不太对劲。对我来说，那是七年级。我在朋友 Kevin 家过夜...\\n\\nKevin 的爸爸走进客厅说：嘿，今晚谁想看《加勒比海盗》？然后 Kevin 的妈妈跑进来，说：绝对不行，那对他们来说太成熟了。Kevin 爸爸说：但我真的很想看《加勒比海盗》。Kevin 妈妈说：我想你会没事的 Kirk。然后 Kevin 说：我很抱歉让你看到这一幕。那是我听过的最健康的争吵（healthiest disagreement）。"
    },
    {
        "id": "1.3",
        "title": "父母7天大离婚",
        "text": "我父母在我出生七天的时候就离婚了。所以像大多数孩子一样，我的第一个词是妈妈（mama），但我的接下来五个字（next five words），是她让我告诉你的（told me to tell you）。\\n\\n【梗：mama 和 next five words 连读像是 mama told me to tell you，暗示妈妈让婴儿传话给爸爸】"
    },
    {
        "id": "1.4",
        "title": "家庭结构混乱",
        "text": "我妈离过两次婚，我爸离过三次婚，我有四个同父异母的弟弟妹妹（four younger half siblings）。所以总共两个（So two total）。\\n\\n【梗：四个同父异母的兄弟姐妹，但从完整家庭角度算两个】"
    },
    {
        "id": "1.5",
        "title": "36楼烂地基",
        "text": "我现在36岁了。很多人都觉得，到了36岁，你应该停止把你所有的问题都归咎于父母了。好吧，让我问你这个问题：如果你在一栋地基烂掉的楼（fucked up foundation）里，你觉得在36层（36th floor）会更安全吗？\\n\\n是的，我也不这么认为。"
    },
    {
        "id": "1.6",
        "title": "ex-stepdad的尴尬命名",
        "text": "上个月我和前继父一起吃饭。这种关系没有一个方便的称呼，因为它本不应该存在。我不知道哪个更好：前继父（former stepdad），还是那个下台的父亲（the dad who stepped down）。\\n\\n我敢肯定德语里一定有个词来形容一个曾经操我妈的男人。"
    },
    {
        "id": "1.7",
        "title": "ex-stepdad是sugar daddy",
        "text": "我们仍然花时间在一起的唯一原因是他为每顿饭买单，从技术上讲，这让他成为我的糖爹（sugar daddy），如果非要这么说的话。"
    },
    {
        "id": "1.8",
        "title": "给继父的婚姻建议",
        "text": "我记得有一次在高中，我继父开车送我。他们肯定刚吵过架什么的，因为他问我：我怎么才能让你妈妈开心？但在那个年龄，我对女人的唯一了解来自互联网。所以我说：我不知道。你试过用舌头拼字母表吗（spelling the alphabet with your tongue）？\\n\\n我延长了那段婚姻六年。"
    },
    {
        "id": "1.9",
        "title": "妈妈在eHarmony",
        "text": "但他们现在离婚了。现在我妈在 eHarmony 上。万一你也想操我妈呢（Just in case you want to fuck my mom）。"
    },
    {
        "id": "1.10",
        "title": "妈妈的约会反馈",
        "text": "她最近和一个男人约会。我问她，约会怎么样？她说：这么说吧，我们在身体上很兼容（physically compatible）。我说：这么说吧，下次别说了。怎么样？"
    },
    {
        "id": "1.11",
        "title": "和妈妈的互相伤害",
        "text": "然后她问我，你女朋友怎么样？我说：嗯，她是个喷子（she's a squirter），但我们还能维持（keeping afloat）。互相伤害啊，妈咪（Two can play this game, mommy）。"
    },
    {
        "id": "1.12",
        "title": "妈妈只约会年长男性",
        "text": "我妈只约会比她年长的男人。所以她很快就快没选择了（running out of options）。"
    },
    {
        "id": "1.13",
        "title": "前男友不举",
        "text": "她向我抱怨她上一个男朋友硬不起来（couldn't get it up）。当我见到他时，我意识到她指的是他的整个身体。\\n\\n【梗：get it up 通常指勃起，但这里指全身瘫痪】"
    },
    {
        "id": "1.14",
        "title": "有钱老男友的电车难题",
        "text": "她和一个男人约会。我真的很喜欢这个男人，因为他很有钱。我猜他就是电车难题（trolley problem）的原版司机。\\n\\n【梗：为了钱可以牺牲母亲，就像电车难题中选择撞谁】"
    },
    {
        "id": "1.15",
        "title": "狗的共同抚养",
        "text": "分手非常复杂，因为他们一起领养了一只狗。这只可爱的小狗叫 Reggie。我妈告诉我，他们决定尝试共同抚养（shared custody）这只狗。我告诉她，我说：我敢肯定 Reggie 宁愿被安乐死（prefer to be put down）。"
    },
    {
        "id": "1.16",
        "title": "Reggie的焦虑和妈妈约会",
        "text": "但她说，他们这样做是为了 Reggie。我妈说，她注意到每当她约会后带新男人回公寓时，Reggie 都会变得非常焦虑和不舒服（anxious and uncomfortable）。所以现在她只在 Reggie 去他爸爸家时才去约会。我说：哦，我要是只博美犬（Pomeranian）就好了。"
    },
    {
        "id": "1.17",
        "title": "爸爸的糖果trick",
        "text": "我爸经常约会。经常到他都有技巧了。每当他把新女人带进我的生活时，首先他会去 CVS，买一大堆糖果（shitload of candy）。他会把糖果给那个女人，然后她再给我。所以我就会自动信任她，你知道，就像恋童癖一样（like a pedophile）。"
    },
    {
        "id": "1.18",
        "title": "万圣节后遗症",
        "text": "而且这招很管用。我到现在每到万圣节（Halloween）还会对女人过度依恋（overly attached）。\\n\\n【callback：承接上一条糖果梗，万圣节会收到糖果】"
    },
    {
        "id": "1.19",
        "title": "爸爸出轨的术语",
        "text": "但每段关系都会结束，因为我爸会出轨。他相信的现在应该叫做非伦理非一夫一妻制（non-ethical non-monogamy）。我们当时不用这些术语。相反，他说：她疯了，儿子（she just went crazy, son）。"
    },
    {
        "id": "1.20",
        "title": "遇到ex-stepmom",
        "text": "我小时候我爸再婚了，我和继母很亲近。当然，我们年龄相仿。我们离婚后没有保持联系，但几年前，我在一家杂货店。我转进麦片 aisle，看到我前继母（ex-step-mom）和一个小男孩一起挑麦片。感觉就像遇到了前女友（running into an ex-girlfriend）。"
    },
    {
        "id": "1.21",
        "title": "对继母新儿子的嫉妒",
        "text": "说实话，我当时就想：Belinda，这他妈是谁（who the fuck is this）？她说：这是我儿子 Tommy。我说：嘿，伙计。她还戴着我母亲节给她做的通心粉项链（macaroni necklace）吗？还是你只是在假装它很漂亮好操我爸？我希望你喜欢二手货，你这个小婊子（you little bitch）。"
    },
    {
        "id": "1.22",
        "title": "女友替代妈妈",
        "text": "我有两个继母，我和她们都很亲近，但方式不同。我从来没有把她们看作是我亲生母亲的替代品（replacement）。那是我女朋友的作用（That's what my girlfriend is for）。"
    },
    {
        "id": "1.23",
        "title": "妈妈当瑜伽老师反击",
        "text": "当我对事业感到沮丧时，我妈会对我说：你是个演员（you're an actor）。你为什么不演得不那么沮丧呢（act like you're not depressed）？\\n\\n所以我说：妈，你是个瑜伽老师（you're a yoga teacher）。你为什么不自己去操自己呢（go fuck yourself）？"
    },
    {
        "id": "1.24",
        "title": "妈妈握有黑料",
        "text": "我讲太多关于我妈的笑话时要小心，因为她还留着我高中《一千零一夜》（Arabian Nights）演出的所有照片。她可以用一条 Instagram 帖子 cancel 我。如果我太过分，她只会打：你永远是我的小阿里巴巴（you'll always be my little Alibaba）。"
    },
    {
        "id": "1.25",
        "title": "爸爸长得帅",
        "text": "我觉得如果你知道我爸也很帅（hot），他的很多行为就更有意义了。我知道我说这个听起来很奇怪，但操你。我必须面对这个。人们见到我爸，他们会说：你爸真帅（your dad's really good looking）。好像我欠他们一个解释似的（Like I owe them an explanation）。"
    },
    {
        "id": "1.26",
        "title": "爸爸传谣言",
        "text": "我记得我爸有一次来初中接我——我的意思是就一次（I mean once）——然后我年级里就开始传谣言说我一定是领养的（adopted）。这真的很伤人，因为那是我爸传的谣言。"
    },
    {
        "id": "1.27",
        "title": "爸爸睡了手工课老师",
        "text": "这是真事。我爸，我爸曾经睡了我八年级的艺术和手工老师（arts and crafts teacher）。我非常生气，因为那些成绩不重要（those grades don't matter）。"
    },
    {
        "id": "1.28",
        "title": "要求爸爸睡代数老师",
        "text": "他觉得很愧疚。他说：我怎么才能补偿你？我说：你可以操我78岁的代数老师 Breyer 先生（Mr. Breyer）。"
    },
    {
        "id": "1.29",
        "title": "意大利爸爸的家训",
        "text": "我爸是意大利人。所以他总是告诉我：儿子，记住，la famiglia è tutto（家庭就是一切）。Male tua madre è una puttana（你妈妈是婊子）。\\n\\n我现在还是不知道第二部分是什么意思，但听起来真好听（nice ring to it）。"
    },
    {
        "id": "1.30",
        "title": "爸爸心脏病-遗嘱事件",
        "text": "去年我爸心脏病发作。他想让我下去，好让我看看他的遗嘱（will）。他说：我想让你知道，如果在我到之前出了什么事，我会在你所有演出中以 spirit 的形式出现。我说：哦，就像你生前一样（just like when you were alive）。"
    },
    {
        "id": "1.31",
        "title": "Venmo请求",
        "text": "所以我买了下一班飞机。我给我爸发了一个 Venmo 请求（Venmo request）。"
    },
    {
        "id": "1.32",
        "title": "爸爸的新女友年龄差",
        "text": "我爸对我说：儿子，你不明白，当我约会同龄的女人时，这让我想起我的死亡（mortality）。我说：好吧，当我看到你约会的女人时，这让我想起 Jeffrey Epstein。"
    },
    {
        "id": "1.33",
        "title": "爸爸把遗产给新女友",
        "text": "他想向全家宣布，他要把三分之一的遗产（a third of his estate）给这个新女友。我能看出我妹妹很生气。所以我低声对她说：现在你知道你出生的时候我是什么感受了（now you know how I felt when you were born）。"
    },
    {
        "id": "1.34",
        "title": "爸爸的劳动价值论",
        "text": "我不得不向她解释：亲爱的，我爸71岁了。如果你给一个71岁的人吹箫（suck a 71 year old's dick），你就能进遗嘱。这叫资本主义（capitalism），亲爱的。我们在干嘛呢？"
    }
]

# 创建图形
fig, ax = plt.subplots(1, 1, figsize=(16, 150))
ax.set_xlim(0, 50)
ax.set_ylim(0, 300)
ax.axis('off')

# 标题
title_y = 297
ax.text(25, title_y, "【原生家庭】主题笑点详解", fontsize=32, fontweight='bold', ha='center', va='top', color='#1A5276')
ax.text(25, title_y - 4, "Tom Segura - Thief of Joy | 共34个笑点", fontsize=18, ha='center', va='top', color='#2874A6')
ax.text(25, title_y - 8, "括号内为英文原文，帮助理解文字游戏 | 蓝色箭头=承接 | 红色虚线=Callback", fontsize=12, ha='center', va='top', color='#5D6D7E', style='italic')

# 布局参数
box_width = 44
x_center = 25
y_start = title_y - 15
spacing_y = 8

# 存储每个模块的底部和顶部位置
module_positions = []

# 绘制每个笑点
for i, joke in enumerate(family_jokes):
    # 计算文本高度
    text_lines = len(joke['text']) // 26 + joke['text'].count('\\n') + 2
    adjusted_height = max(5, text_lines * 0.75 + 1.5)
    
    y_top = y_start - i * spacing_y
    y_bottom = y_top - adjusted_height
    
    # 记录位置 (底部y, 顶部y, 中心x, 高度)
    module_positions.append((y_bottom, y_top, x_center, adjusted_height))
    
    # 绘制圆角矩形
    rect = FancyBboxPatch((x_center - box_width/2, y_bottom), box_width, adjusted_height,
                           boxstyle="round,pad=0.15",
                           facecolor='#A2D9CE', edgecolor='#1A5276', 
                           linewidth=2.5, alpha=0.95)
    ax.add_patch(rect)
    
    # 编号和标题
    ax.text(x_center - box_width/2 + 0.8, y_top - 0.6, f"{joke['id']} {joke['title']}", 
            fontsize=14, fontweight='bold', ha='left', va='top', color='#154360')
    
    # 文本内容
    ax.text(x_center - box_width/2 + 0.8, y_top - 1.9, joke['text'], fontsize=11,
            ha='left', va='top', color='#1A5276', wrap=True,
            linespacing=1.45)

# 画承接箭头 - 从上一个模块底部连接到下一个模块顶部
for i in range(len(module_positions) - 1):
    y_bottom_current, _, x_center_current, _ = module_positions[i]
    _, y_top_next, x_center_next, _ = module_positions[i + 1]
    
    # 箭头从当前模块底部向下延伸0.2，连接到下一个模块顶部向上0.2
    ax.annotate('', xy=(x_center_next, y_top_next + 0.2), 
               xytext=(x_center_current, y_bottom_current - 0.2),
               arrowprops=dict(arrowstyle='->', color='#2980B9', lw=3,
                             connectionstyle="arc3,rad=0"))

# 标注callback关系 (1.17 到 1.18)
callback_start_idx = 16  # 1.17
callback_end_idx = 17    # 1.18
y_bottom_17, _, x_17, _ = module_positions[callback_start_idx]
_, y_top_18, x_18, _ = module_positions[callback_end_idx]

ax.annotate('', xy=(x_18 + box_width/2 - 2, y_top_18 + 0.5), 
           xytext=(x_17 + box_width/2 - 2, y_bottom_17 - 0.5),
           arrowprops=dict(arrowstyle='->', color='#C0392B', lw=3.5, ls='--',
                         connectionstyle="arc3,rad=0.15"))
ax.text(x_17 + box_width/2 + 1.5, (y_bottom_17 + y_top_18)/2, 'callback', 
        fontsize=10, color='#C0392B', fontweight='bold', rotation=90, va='center')

# 添加说明
ax.text(25, 2, "—— 蓝色实线：承接关系  |  红色虚线：Callback 呼应  |  （）内为英文原文", 
        fontsize=13, ha='center', style='italic', color='#555')

plt.tight_layout()
plt.savefig('/root/.openclaw/workspace/transcripts/Thief_of_Joy_原生家庭_修正版.png', 
            dpi=200, bbox_inches='tight', facecolor='white', edgecolor='none')
print("✅ 修正版原生家庭主题图已生成（含英文原文+对齐箭头）")

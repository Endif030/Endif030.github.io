from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

# 创建演示文稿
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# 原生家庭主题数据 - 包含关系说明
family_jokes = [
    {
        "id": "1.1",
        "title": "开场钩子",
        "text": "我来自一个 messed up 的家庭。我知道这并不会让我在这个房间里显得特别。我猜你们大多数人也都来自 messed up 的家庭，因为想想看，来自健康家庭的人，他们在外面。和朋友们一起欢笑。但不，不是你们。你们需要专业人士（needed a professional）。",
        "relation": "开场引入"
    },
    {
        "id": "1.2", 
        "title": "Kevin家的健康争吵",
        "text": "当你还是个孩子的时候，你不会意识到你的家庭 messed up，因为那就是你所知道的一切。对我来说，那是七年级。我在朋友 Kevin 家过夜，Kevin 的爸爸走进客厅说：嘿，今晚谁想看《加勒比海盗》？然后 Kevin 的妈妈跑进来，说：绝对不行，那对他们来说太成熟了。Kevin 爸爸说：但我真的很想看。Kevin 妈妈说：我想你会没事的 Kirk。然后 Kevin 说：我很抱歉让你看到这一幕。那是我听过的最健康的争吵（healthiest disagreement）。",
        "relation": "承接1.1：展开童年认知"
    },
    {
        "id": "1.3",
        "title": "父母7天大离婚",
        "text": "我父母在我出生七天的时候就离婚了。所以像大多数孩子一样，我的第一个词是妈妈（mama），但我的接下来五个字（next five words），是她让我告诉你的（told me to tell you）。\n【梗：mama + next five words 连读像是 mama told me to tell you】",
        "relation": "承接1.2：引入父母离婚"
    },
    {
        "id": "1.4",
        "title": "家庭结构混乱",
        "text": "我妈离过两次婚，我爸离过三次婚，我有四个同父异母的弟弟妹妹（four younger half siblings）。所以总共两个（So two total）。\n【梗：四个同父异母，但从完整家庭角度算两个】",
        "relation": "承接1.3：展开家庭结构"
    },
    {
        "id": "1.5",
        "title": "36楼烂地基",
        "text": "我现在36岁了。很多人都觉得，到了36岁，你应该停止把你所有的问题都归咎于父母了。好吧，让我问你这个问题：如果你在一栋地基烂掉的楼（fucked up foundation）里，你觉得在36层（36th floor）会更安全吗？是的，我也不这么认为。",
        "relation": "承接1.4：升华原生家庭影响"
    },
    {
        "id": "1.6",
        "title": "ex-stepdad的尴尬命名",
        "text": "上个月我和前继父一起吃饭。这种关系没有一个方便的称呼，因为它本不应该存在。我不知道哪个更好：前继父（former stepdad），还是那个下台的父亲（the dad who stepped down）。我敢肯定德语里一定有个词来形容一个曾经操我妈的男人。",
        "relation": "转入继父话题"
    },
    {
        "id": "1.7",
        "title": "ex-stepdad是sugar daddy",
        "text": "我们仍然花时间在一起的唯一原因是他为每顿饭买单，从技术上讲，这让他成为我的糖爹（sugar daddy），如果非要这么说的话。",
        "relation": "承接1.6：展开继父关系"
    },
    {
        "id": "1.8",
        "title": "给继父的婚姻建议",
        "text": "我记得有一次在高中，我继父开车送我。他们肯定刚吵过架，因为他问我：我怎么才能让你妈妈开心？但在那个年龄，我对女人的唯一了解来自互联网。所以我说：我不知道。你试过用舌头拼字母表吗（spelling the alphabet with your tongue）？我延长了那段婚姻六年。",
        "relation": "承接1.7：继父故事展开"
    },
    {
        "id": "1.9",
        "title": "妈妈在eHarmony",
        "text": "但他们现在离婚了。现在我妈在 eHarmony 上。万一你也想操我妈呢（Just in case you want to fuck my mom）。",
        "relation": "转入妈妈约会话题"
    },
    {
        "id": "1.10",
        "title": "妈妈的约会反馈",
        "text": "她最近和一个男人约会。我问她，约会怎么样？她说：这么说吧，我们在身体上很兼容（physically compatible）。我说：这么说吧，下次别说了。怎么样？",
        "relation": "承接1.9：妈妈约会故事"
    },
    {
        "id": "1.11",
        "title": "和妈妈的互相伤害",
        "text": "然后她问我，你女朋友怎么样？我说：嗯，她是个喷子（she's a squirter），但我们还能维持（keeping afloat）。互相伤害啊，妈咪（Two can play this game, mommy）。",
        "relation": "承接1.10：母子互动升级"
    },
    {
        "id": "1.12",
        "title": "妈妈只约会年长男性",
        "text": "我妈只约会比她年长的男人。所以她很快就快没选择了（running out of options）。",
        "relation": "承接1.11：妈妈约会话题继续"
    },
    {
        "id": "1.13",
        "title": "前男友不举",
        "text": "她向我抱怨她上一个男朋友硬不起来（couldn't get it up）。当我见到他时，我意识到她指的是他的整个身体。\n【梗：get it up 通常指勃起，但这里指全身瘫痪】",
        "relation": "承接1.12：妈妈约会对象故事"
    },
    {
        "id": "1.14",
        "title": "有钱老男友的电车难题",
        "text": "她和一个男人约会。我真的很喜欢这个男人，因为他很有钱。我猜他就是电车难题（trolley problem）的原版司机。\n【梗：为了钱可以牺牲母亲，就像电车难题中选择撞谁】",
        "relation": "承接1.13：妈妈约会对象故事2"
    },
    {
        "id": "1.15",
        "title": "狗的共同抚养",
        "text": "分手非常复杂，因为他们一起领养了一只狗。这只可爱的小狗叫 Reggie。我妈告诉我，他们决定尝试共同抚养（shared custody）这只狗。我告诉她，我说：我敢肯定 Reggie 宁愿被安乐死（prefer to be put down）。",
        "relation": "承接1.14：妈妈分手后故事"
    },
    {
        "id": "1.16",
        "title": "Reggie的焦虑和妈妈约会",
        "text": "但她说，他们这样做是为了 Reggie。我妈说，她注意到每当她约会后带新男人回公寓时，Reggie 都会变得非常焦虑和不舒服（anxious and uncomfortable）。所以现在她只在 Reggie 去他爸爸家时才去约会。我说：哦，我要是只博美犬（Pomeranian）就好了。",
        "relation": "承接1.15：Reggie故事展开"
    },
    {
        "id": "1.17",
        "title": "爸爸的糖果trick",
        "text": "我爸经常约会。经常到他都有技巧了。每当他把新女人带进我的生活时，首先他会去 CVS，买一大堆糖果（shitload of candy）。他会把糖果给那个女人，然后她再给我。所以我就会自动信任她，你知道，就像恋童癖一样（like a pedophile）。",
        "relation": "转入爸爸话题"
    },
    {
        "id": "1.18",
        "title": "万圣节后遗症",
        "text": "而且这招很管用。我到现在每到万圣节（Halloween）还会对女人过度依恋（overly attached）。\n【callback：承接上一条糖果梗，万圣节会收到糖果】",
        "relation": "【callback 1.17糖果trick】承接爸爸的糖果技巧"
    },
    {
        "id": "1.19",
        "title": "爸爸出轨的术语",
        "text": "但每段关系都会结束，因为我爸会出轨。他相信的现在应该叫做非伦理非一夫一妻制（non-ethical non-monogamy）。我们当时不用这些术语。相反，他说：她疯了，儿子（she just went crazy, son）。",
        "relation": "承接1.18：爸爸约会话题继续"
    },
    {
        "id": "1.20",
        "title": "遇到ex-stepmom",
        "text": "我小时候我爸再婚了，我和继母很亲近。当然，我们年龄相仿。我们离婚后没有保持联系，但几年前，我在一家杂货店。我转进麦片 aisle，看到我前继母（ex-step-mom）和一个小男孩一起挑麦片。感觉就像遇到了前女友（running into an ex-girlfriend）。",
        "relation": "转入继母话题"
    },
    {
        "id": "1.21",
        "title": "对继母新儿子的嫉妒",
        "text": "说实话，我当时就想：Belinda，这他妈是谁（who the fuck is this）？她说：这是我儿子 Tommy。我说：嘿，伙计。她还戴着我母亲节给她做的通心粉项链（macaroni necklace）吗？还是你只是在假装它很漂亮好操我爸？我希望你喜欢二手货，你这个小婊子（you little bitch）。",
        "relation": "承接1.20：继母故事展开"
    },
    {
        "id": "1.22",
        "title": "女友替代妈妈",
        "text": "我有两个继母，我和她们都很亲近，但方式不同。我从来没有把她们看作是我亲生母亲的替代品（replacement）。那是我女朋友的作用（That's what my girlfriend is for）。",
        "relation": "承接1.21：继母话题总结"
    },
    {
        "id": "1.23",
        "title": "妈妈当瑜伽老师反击",
        "text": "当我对事业感到沮丧时，我妈会对我说：你是个演员（you're an actor）。你为什么不演得不那么沮丧呢（act like you're not depressed）？\n所以我说：妈，你是个瑜伽老师（you're a yoga teacher）。你为什么不自己去操自己呢（go fuck yourself）？",
        "relation": "转入妈妈反击话题"
    },
    {
        "id": "1.24",
        "title": "妈妈握有黑料",
        "text": "我讲太多关于我妈的笑话时要小心，因为她还留着我高中《一千零一夜》（Arabian Nights）演出的所有照片。她可以用一条 Instagram 帖子 cancel 我。如果我太过分，她只会打：你永远是我的小阿里巴巴（you'll always be my little Alibaba）。",
        "relation": "承接1.23：妈妈黑料话题"
    },
    {
        "id": "1.25",
        "title": "爸爸长得帅",
        "text": "我觉得如果你知道我爸也很帅（hot），他的很多行为就更有意义了。我知道我说这个听起来很奇怪，但操你。我必须面对这个。人们见到我爸，他们会说：你爸真帅（your dad's really good looking）。好像我欠他们一个解释似的（Like I owe them an explanation）。",
        "relation": "转入爸爸外貌话题"
    },
    {
        "id": "1.26",
        "title": "爸爸传谣言",
        "text": "我记得我爸有一次来初中接我——我的意思是就一次（I mean once）——然后我年级里就开始传谣言说我一定是领养的（adopted）。这真的很伤人，因为那是我爸传的谣言。",
        "relation": "承接1.25：爸爸故事展开"
    },
    {
        "id": "1.27",
        "title": "爸爸睡了手工课老师",
        "text": "这是真事。我爸，我爸曾经睡了我八年级的艺术和手工老师（arts and crafts teacher）。我非常生气，因为那些成绩不重要（those grades don't matter）。",
        "relation": "承接1.26：爸爸故事继续"
    },
    {
        "id": "1.28",
        "title": "要求爸爸睡代数老师",
        "text": "他觉得很愧疚。他说：我怎么才能补偿你？我说：你可以操我78岁的代数老师 Breyer 先生（Mr. Breyer）。",
        "relation": "承接1.27：爸爸睡老师故事"
    },
    {
        "id": "1.29",
        "title": "意大利爸爸的家训",
        "text": "我爸是意大利人。所以他总是告诉我：儿子，记住，la famiglia è tutto（家庭就是一切）。Male tua madre è una puttana（你妈妈是婊子）。\n我现在还是不知道第二部分是什么意思，但听起来真好听（nice ring to it）。",
        "relation": "承接1.28：爸爸身份背景"
    },
    {
        "id": "1.30",
        "title": "爸爸心脏病-遗嘱事件",
        "text": "去年我爸心脏病发作。他想让我下去，好让我看看他的遗嘱（will）。他说：我想让你知道，如果在我到之前出了什么事，我会在你所有演出中以 spirit 的形式出现。我说：哦，就像你生前一样（just like when you were alive）。",
        "relation": "转入爸爸心脏病话题"
    },
    {
        "id": "1.31",
        "title": "Venmo请求",
        "text": "所以我买了下一班飞机。我给我爸发了一个 Venmo 请求（Venmo request）。",
        "relation": "承接1.30：爸爸心脏病后续"
    },
    {
        "id": "1.32",
        "title": "爸爸的新女友年龄差",
        "text": "我爸对我说：儿子，你不明白，当我约会同龄的女人时，这让我想起我的死亡（mortality）。我说：好吧，当我看到你约会的女人时，这让我想起 Jeffrey Epstein。",
        "relation": "承接1.31：爸爸康复后话题"
    },
    {
        "id": "1.33",
        "title": "爸爸把遗产给新女友",
        "text": "他想向全家宣布，他要把三分之一的遗产（a third of his estate）给这个新女友。我能看出我妹妹很生气。所以我低声对她说：现在你知道你出生的时候我是什么感受了（now you know how I felt when you were born）。",
        "relation": "承接1.32：爸爸新女友话题"
    },
    {
        "id": "1.34",
        "title": "爸爸的劳动价值论",
        "text": "我不得不向她解释：亲爱的，我爸71岁了。如果你给一个71岁的人吹箫（suck a 71 year old's dick），你就能进遗嘱。这叫资本主义（capitalism），亲爱的。我们在干嘛呢？",
        "relation": "承接1.33：爸爸遗产话题收尾"
    }
]

# 颜色定义
BG_COLOR = RGBColor(162, 217, 206)  # #A2D9CE
BORDER_COLOR = RGBColor(26, 82, 118)  # #1A5276
TITLE_COLOR = RGBColor(21, 67, 96)  # #154360
TEXT_COLOR = RGBColor(26, 82, 118)  # #1A5276
RELATION_COLOR = RGBColor(41, 128, 185)  # 关系说明颜色

# 每页放2个笑点
jokes_per_slide = 2

for slide_idx in range(0, len(family_jokes), jokes_per_slide):
    # 添加新幻灯片
    blank_layout = prs.slide_layouts[6]  # 空白布局
    slide = prs.slides.add_slide(blank_layout)
    
    # 如果是第一页，添加标题
    if slide_idx == 0:
        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(12.333), Inches(0.6))
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = "【原生家庭】主题笑点详解 - Tom Segura Thief of Joy"
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = TITLE_COLOR
        p.alignment = PP_ALIGN.CENTER
        
        start_y = 1.0
    else:
        start_y = 0.4
    
    # 添加该页的笑点
    for i, joke in enumerate(family_jokes[slide_idx:slide_idx + jokes_per_slide]):
        y_pos = start_y + i * 3.4
        
        # 添加形状（模块）
        shape = slide.shapes.add_shape(
            1,  # MSO_SHAPE.RECTANGLE
            Inches(0.5), Inches(y_pos),
            Inches(12.333), Inches(3.1)
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = BG_COLOR
        shape.line.color.rgb = BORDER_COLOR
        shape.line.width = Pt(3)
        
        # 添加标题文本
        title_box = slide.shapes.add_textbox(Inches(0.7), Inches(y_pos + 0.15), Inches(11.9), Inches(0.4))
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = f"{joke['id']} {joke['title']}"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = TITLE_COLOR
        
        # 添加内容文本
        content_box = slide.shapes.add_textbox(Inches(0.7), Inches(y_pos + 0.6), Inches(11.9), Inches(2.0))
        tf = content_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = joke['text']
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_COLOR
        p.line_spacing = 1.3
        
        # 添加关系说明
        relation_box = slide.shapes.add_textbox(Inches(0.7), Inches(y_pos + 2.7), Inches(11.9), Inches(0.35))
        tf = relation_box.text_frame
        p = tf.paragraphs[0]
        p.text = f"→ {joke['relation']}"
        p.font.size = Pt(10)
        p.font.color.rgb = RELATION_COLOR
        p.font.italic = True
    
    # 如果不是最后一页，添加页码提示
    if slide_idx + jokes_per_slide < len(family_jokes):
        page_box = slide.shapes.add_textbox(Inches(6), Inches(7.1), Inches(1.333), Inches(0.3))
        tf = page_box.text_frame
        p = tf.paragraphs[0]
        p.text = f"第 {slide_idx//jokes_per_slide + 1} 页 / 共 17 页"
        p.font.size = Pt(9)
        p.font.color.rgb = RGBColor(127, 140, 141)
        p.alignment = PP_ALIGN.CENTER

# 保存PPT
ppt_path = '/root/.openclaw/workspace/transcripts/Thief_of_Joy_原生家庭_PPT_带关系版.pptx'
prs.save(ppt_path)
print(f"✅ PPT已生成: {ppt_path}")
print(f"共 {len(prs.slides)} 页，每页2个笑点")
print("每个笑点底部添加了关系说明（→ 承接X.X / → 【callback X.X】）")

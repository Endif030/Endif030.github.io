from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

# 创建演示文稿 - 表演生涯主题
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

career_jokes = [
    {"id": "3.1", "title": "剧场孩子", "text": "我曾经是个 theater kid（戏剧孩子），但你们都能看出来对吧？我手势太多了。连聋人都会说：shut the fuck up（闭嘴）。", "relation": "开场自嘲"},
    {"id": "3.2", "title": "主持变装比赛", "text": "我曾经主持过一场 drag competition（变装比赛）。一个变装皇后让我低调一点。另一个说我在讲笑话前看起来像在对自己说 five, six, seven, eight。获胜的变装皇后叫我 John Mulaney，如果他唯一上瘾的药物是舞台的话。", "relation": "承接3.1：戏剧身份"},
    {"id": "3.3", "title": "音乐剧学位", "text": "我大学学的是音乐剧（musical theater），这就像拥有 imagination（想象力）的博士学位。", "relation": "承接3.2：学历自嘲"},
    {"id": "3.4", "title": "课程名字", "text": "我的课叫 movement（动作）和 voice（声音），还有其他我小时候就已经学过的东西。", "relation": "承接3.3：课程自嘲"},
    {"id": "3.5", "title": "演员的会计课", "text": "我唯一的学术课叫 accounting for actors（演员会计），就像普通会计，但专注于负数。第一课是如何申请失业救济（how to file for unemployment）。", "relation": "承接3.4：职业自嘲"},
    {"id": "3.6", "title": "观众行为好", "text": "每个喜剧俱乐部都对我说：你的观众表现很好。我说：这不是他们第一次在合唱团（not their first time in the ensemble）。", "relation": "承接3.5：演员经历"},
    {"id": "3.7", "title": "triple threat", "text": "对于非戏剧孩子的人来说，我被称为 triple threat（三重威胁）。威胁一：你会看到的，我能表演。威胁二：我能唱歌。威胁三：我很烦（I'm annoying）。", "relation": "承接3.6：自嘲"},
    {"id": "3.8", "title": "20万学费梗", "text": "谢谢。那个笑话花了我 $200,000（20万美元）。", "relation": "承接3.7：学费自嘲"},
    {"id": "3.9", "title": "华尔街之狼服务员", "text": "我演过《华尔街之狼》，我演 Leonardo DiCaprio 的 waiter（服务员）。所以为了准备这个角色，我当了12年服务员。", "relation": "承接3.8：演员经历"},
    {"id": "3.10", "title": "extra work", "text": "这叫 extra work（群演），你在屏幕上但没有台词。你就像 furniture, but with dreams（家具，但有梦想）。", "relation": "承接3.9：群演经历"}
]

BG_COLOR = RGBColor(144, 200, 172)  # 薄荷绿
BORDER_COLOR = RGBColor(26, 82, 118)
TITLE_COLOR = RGBColor(21, 67, 96)
TEXT_COLOR = RGBColor(26, 82, 118)
RELATION_COLOR = RGBColor(41, 128, 185)

for slide_idx in range(0, len(career_jokes), 2):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    
    if slide_idx == 0:
        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(12.333), Inches(0.6))
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = "【表演生涯】主题笑点详解 - Tom Segura Thief of Joy"
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = TITLE_COLOR
        p.alignment = PP_ALIGN.CENTER
        start_y = 1.0
    else:
        start_y = 0.4
    
    for i, joke in enumerate(career_jokes[slide_idx:slide_idx + 2]):
        y_pos = start_y + i * 3.4
        shape = slide.shapes.add_shape(1, Inches(0.5), Inches(y_pos), Inches(12.333), Inches(3.1))
        shape.fill.solid()
        shape.fill.fore_color.rgb = BG_COLOR
        shape.line.color.rgb = BORDER_COLOR
        shape.line.width = Pt(3)
        
        title_box = slide.shapes.add_textbox(Inches(0.7), Inches(y_pos + 0.15), Inches(11.9), Inches(0.4))
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = f"{joke['id']} {joke['title']}"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = TITLE_COLOR
        
        content_box = slide.shapes.add_textbox(Inches(0.7), Inches(y_pos + 0.6), Inches(11.9), Inches(2.0))
        tf = content_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = joke['text']
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_COLOR
        p.line_spacing = 1.3
        
        relation_box = slide.shapes.add_textbox(Inches(0.7), Inches(y_pos + 2.7), Inches(11.9), Inches(0.35))
        tf = relation_box.text_frame
        p = tf.paragraphs[0]
        p.text = f"→ {joke['relation']}"
        p.font.size = Pt(10)
        p.font.color.rgb = RELATION_COLOR
        p.font.italic = True

ppt_path = '/root/.openclaw/workspace/transcripts/Thief_of_Joy_表演生涯.pptx'
prs.save(ppt_path)
print(f"✅ 表演生涯主题PPT已生成: 5页")

# 性身体主题
prs2 = Presentation()
prs2.slide_width = Inches(13.333)
prs2.slide_height = Inches(7.5)

sex_jokes = [
    {"id": "4.1", "title": "爸爸是legs guy", "text": "我爸是个 legs guy（腿控）。你知道，男人要么是腿控，要么是屁股控，要么是胸控。我知道把男人这样分类很冒犯。但如果我爸看到高个子女人，他会说：儿子，she's got legs for days（她的腿有好几天那么长）。因为这是在这愚蠢的国家测量腿的唯一方式。", "relation": "转入身体话题"},
    {"id": "4.2", "title": "英尺的荒谬", "text": "作为美国人，你应该每天花一点时间反思我们用 feet（英尺）作为测量单位有多愚蠢。那只是某个人的脚一次。但我们仍用它测量很重要的东西，除了马。马用手（hands）测量。 Feet, hands。他们一定试过...他们一定试过用鸡巴测量。", "relation": "承接4.1：测量单位"},
    {"id": "4.3", "title": "用阴茎测量的历史", "text": "我敢打赌他们试过用鸡巴测量。我可以告诉你发生了什么：没人能同意一个鸡巴应该有多长。一开始肯定是平均值，但下半部分男人冲进了国会：什么？我的鸡巴只有半个鸡巴？这不行！于是他们不得不让鸡巴越来越小，直到没人感到不安全。这就是 centimeter（厘米）的由来。", "relation": "承接4.2：公制起源"},
    {"id": "4.4", "title": "6英寸愿望", "text": "我只想要六英寸（six inches）。天啊，我高中时每晚都用 dollar bill（美元钞票）测量我的鸡巴。你知道为什么用美元钞票吗？因为它们差不多六英寸，而且尺子不会弯曲。我花了几个小时用鸡巴拍 George Washington 的脸。", "relation": "承接4.3：身体焦虑"},
    {"id": "4.5", "title": "华盛顿的回应", "text": "他回头看着我说：I cannot tell a lie（我不能撒谎）。你差一美元（You're a buck short）。", "relation": "承接4.4：华盛顿梗"},
    {"id": "4.6", "title": "特朗普上钞票", "text": "我不喜欢特朗普，但我希望把他放在 $1 bill（一美元钞票）上。因为无论你多大，他都会说 huge（巨大）。", "relation": "承接4.5：政治梗"},
    {"id": "4.7", "title": "高中剧场经历", "text": "高中戏剧派对上，所有女人和所有男同性恋开始互相亲热。我会在后面说：whose dick do I have to suck to get some pussy?（我要吸多少鸡巴才能吸到逼？）这太疯狂了。", "relation": "承接4.6：高中经历"},
    {"id": "4.8", "title": "NYU三人行", "text": "我在 NYU 宿舍，和 straight guy Steve（直男史蒂夫）以及 gay Garrison（同性恋加里森）在我的床上讨论电影版 Rent 出了什么问题。突然，直男史蒂夫开始解开我的 cargo shorts（工装短裤）。我说：直男史蒂夫，你在下面干什么？他说：Jamarcus，I'm straight, but I can make you feel amazing（我是直男，但我能让你感觉很棒）。", "relation": "承接4.7：NYU经历"},
    {"id": "4.9", "title": "口交技巧列举", "text": "这不是他的第一次口交。他在用不同的技巧：用手，普通方式，扭转式，rolling the snake（滚蛇），mine climbing a rope（爬绳），Spider-Man（蜘蛛侠），step team（仪仗队）。", "relation": "承接4.8：三人行细节"},
    {"id": "4.10", "title": "最孤独的时刻", "text": "我太沮丧了，史蒂夫直接滑过去开始吸加里森的鸡巴，那已经准备好了。我记得侧身躺着，看着直男史蒂夫猛吸同性恋加里森的大肥鸡巴。天啊，I am so lonely（我太孤独了）。Blackout（昏倒）。", "relation": "承接4.9：情感反转"},
    {"id": "4.11", "title": "谣言受益者", "text": "谣言传回了营地。但下一次戏剧派对，我发现每个人都在说是我吸了史蒂夫的鸡巴。我这辈子从没得到过这么多逼。", "relation": "承接4.10：谣言结果"},
    {"id": "4.12", "title": "离梦想最近的距离", "text": "我试图享受群演工作，但这很难，因为我从未如此接近我想要的一切，却又如此遥远。这就像你一生的挚爱在你身上，getting fucked by Leonardo DiCaprio（被小李子操）。", "relation": "callback 3.9：华尔街之狼服务员"},
    {"id": "4.13", "title": "事业失意", "text": "喜剧进展很好。但我以为我现在会更出名。我不知道我在想什么。高中时没人喜欢我，但也许全球会。", "relation": "承接4.12：事业反思"}
]

for slide_idx in range(0, len(sex_jokes), 2):
    blank_layout = prs2.slide_layouts[6]
    slide = prs2.slides.add_slide(blank_layout)
    
    if slide_idx == 0:
        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(12.333), Inches(0.6))
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = "【性身体】主题笑点详解 - Tom Segura Thief of Joy"
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = TITLE_COLOR
        p.alignment = PP_ALIGN.CENTER
        start_y = 1.0
    else:
        start_y = 0.4
    
    for i, joke in enumerate(sex_jokes[slide_idx:slide_idx + 2]):
        y_pos = start_y + i * 3.4
        shape = slide.shapes.add_shape(1, Inches(0.5), Inches(y_pos), Inches(12.333), Inches(3.1))
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(244, 208, 63)  # 金黄
        shape.line.color.rgb = BORDER_COLOR
        shape.line.width = Pt(3)
        
        title_box = slide.shapes.add_textbox(Inches(0.7), Inches(y_pos + 0.15), Inches(11.9), Inches(0.4))
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = f"{joke['id']} {joke['title']}"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = TITLE_COLOR
        
        content_box = slide.shapes.add_textbox(Inches(0.7), Inches(y_pos + 0.6), Inches(11.9), Inches(2.0))
        tf = content_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = joke['text']
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_COLOR
        p.line_spacing = 1.3
        
        relation_box = slide.shapes.add_textbox(Inches(0.7), Inches(y_pos + 2.7), Inches(11.9), Inches(0.35))
        tf = relation_box.text_frame
        p = tf.paragraphs[0]
        p.text = f"→ {joke['relation']}"
        p.font.size = Pt(10)
        p.font.color.rgb = RELATION_COLOR
        p.font.italic = True

ppt_path2 = '/root/.openclaw/workspace/transcripts/Thief_of_Joy_性身体.pptx'
prs2.save(ppt_path2)
print(f"✅ 性身体主题PPT已生成: 7页")

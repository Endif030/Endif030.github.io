from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

# 生死心理主题
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

death_jokes = [
    {"id": "5.1", "title": "自杀开头", "text": "你有没有试过说服朋友不要自杀，然后意识到你没有任何好理由？你们有些人今晚带他们来了。挺住。", "relation": "开场-黑色幽默"},
    {"id": "5.2", "title": "地狱", "text": "你会下地狱（You'll go to hell）。我年纪大了越来越理解宗教。有时你需要相信有比活着更糟的东西。", "relation": "承接5.1"},
    {"id": "5.3", "title": "免责声明", "text": "这些笑话可能对真正自杀的人不敬，但他们今晚不在这里。所以我想让你们享受它，好吗？", "relation": "承接5.2"},
    {"id": "5.4", "title": "朋友的自杀短信", "text": "我的朋友过得很好，但去年很艰难。有一天我醒来，朋友给我发了三条短信：I love you, I'm sorry, goodbye（我爱你，对不起，再见）。我立即打电话，直接转到语音信箱。每次都是：嗨，我是 Alice，请留言，我会回电话。这就是为什么如果你正在考虑自杀，update your voicemail（更新你的语音信箱）。", "relation": "承接5.3：朋友故事"},
    {"id": "5.5", "title": "通灵师", "text": "我曾经打错自杀热线，不小心打给了通灵师。说实话，这就是让我停止自杀的原因。Why would I kill myself right before I'm a movie star?（我为什么要在我成为电影明星前自杀？）", "relation": "承接5.4：自杀热线"},
    {"id": "5.6", "title": "867-5309", "text": "自杀热线现在是988，但我会改成 867-5309。因为万一你想自杀，你会说：天啊，867-5309。我很好，你呢（I'm great, how are you）？", "relation": "承接5.5：热线号码"},
    {"id": "5.7", "title": "加拿大安乐死", "text": "加拿大医保覆盖 taking your own life（结束自己生命）。在美国我们也有，我们叫它 not giving people healthcare（不给人医保）。这是一种延迟释放安乐死。如果你想要更快见效的，你得 become a healthcare CEO（成为医疗公司CEO）。", "relation": "承接5.6：安乐死话题"},
    {"id": "5.8", "title": "38岁半", "text": "我认为我们应该在美国正式合法化安乐死。18岁可以投票，21岁可以喝酒，38岁半。让我们给千禧一代一些期待。38岁半，双倍就是美国平均预期寿命。公平地说：you've seen half, do you want to continue?（你看了一半，想继续吗？）", "relation": "承接5.7：年龄话题"},
    {"id": "5.9", "title": "12个自杀梗", "text": "你们表现得很好。这已经是连续12个自杀笑话了。如果对你来说太多了，试着把它想成一个集体自杀笑话（one mass suicide joke）。", "relation": "承接5.8：元幽默"},
    {"id": "5.10", "title": "朋友需要我创作", "text": "我不想任何人自杀，尤其是我的朋友。I need them creatively（我需要他们来创作）。", "relation": "承接5.9"},
    {"id": "5.11", "title": "朋友让我当喜剧演员", "text": "这是那个让我成为单口喜剧演员的朋友。我们都是挣扎的演员，他们说：你应该试试单口，你很搞笑。所以现在我每周给他们打一次电话，讲一小时新笑话。所以他们现在想自杀了。", "relation": "承接5.10"},
    {"id": "5.12", "title": "首演夜的父母", "text": "我记得我首演夜走出来，差点破功，因为第三排坐着我离婚的父母。我爸眼睛哭得通红，我妈拿着一大束水仙花（daffodils），因为她记得我爸过敏。", "relation": "【callback 3.10/4.12】演员经历"},
    {"id": "5.13", "title": "纹身冲突", "text": "这是那个让我当单口演员的朋友。我们四周年纪念日时，我女朋友说：如果你不打算去掉或遮盖那个纹身，我觉得我们不能在一起了。我说：宝贝，那我的 Larry 笑话怎么办？", "relation": "【callback 2.12/2.13】纹身话题"},
    {"id": "5.14", "title": "喜剧是礼物", "text": "这是礼物，我不认为理所当然。我有时笑着对女朋友说：我能给你讲些新笑话吗？她说：Alexa，set a timer for two minutes（设个两分钟的计时器）。", "relation": "承接5.13：女友话题"},
    {"id": "5.15", "title": "女友和心理咨询", "text": "我女朋友和我都在做心理咨询。这意味着当我们有分歧时，我们各自看自己的治疗师，然后碰头引用他们的话。她说：我的治疗师说你优先考虑工作而不是共度优质时光。我说：我的治疗师说她可以 beat the shit out of your therapist（把你的治疗师打得屁滚尿流）。", "relation": "承接5.14：女友话题"}
]

BG_COLOR = RGBColor(241, 148, 138)  # 珊瑚
BORDER_COLOR = RGBColor(26, 82, 118)
TITLE_COLOR = RGBColor(21, 67, 96)
TEXT_COLOR = RGBColor(26, 82, 118)
RELATION_COLOR = RGBColor(41, 128, 185)

for slide_idx in range(0, len(death_jokes), 2):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    
    if slide_idx == 0:
        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(12.333), Inches(0.6))
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = "【生死心理】主题笑点详解 - Tom Segura Thief of Joy"
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = TITLE_COLOR
        p.alignment = PP_ALIGN.CENTER
        start_y = 1.0
    else:
        start_y = 0.4
    
    for i, joke in enumerate(death_jokes[slide_idx:slide_idx + 2]):
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

ppt_path = '/root/.openclaw/workspace/transcripts/Thief_of_Joy_生死心理.pptx'
prs.save(ppt_path)
print(f"✅ 生死心理主题PPT已生成: 8页")

# 社会观察主题
prs2 = Presentation()
prs2.slide_width = Inches(13.333)
prs2.slide_height = Inches(7.5)

social_jokes = [
    {"id": "6.1", "title": "进步语言", "text": "作为喜剧演员，我想首先是搞笑。但我也想让大家知道我是进步的。这两件事不总是一致，因为进步很大一部分是关于语言的。你想使用更新的语言和术语，因为你想对他人的感受敏感。that's not funny（那不好笑）。", "relation": "开场-喜剧与进步"},
    {"id": "6.2", "title": "非法移民术语", "text": "我有个笑话用 illegal immigrant（非法移民）这个词。进步朋友建议用 undocumented immigrant（无证移民）。我听了，我不是混蛋。我改了。我在全国和加拿大、澳大利亚都用这个词。你知道发生了什么吗？Stopped getting laughs（不好笑了）。", "relation": "承接6.1：术语例子"},
    {"id": "6.3", "title": "普选", "text": "所以我回去找进步朋友说：I'm sorry. Unlike you guys, I have to win the popular vote（抱歉，和你们不同，我必须赢得普选）。", "relation": "承接6.2"},
    {"id": "6.4", "title": "左派伪装", "text": "我的笑话是左派的，但它们 disguised in centrist language（用中间派语言伪装），因为它们需要在加州以外的地方奏效。", "relation": "承接6.3"},
    {"id": "6.5", "title": "让爸爸投票给Bernie", "text": "我努力让我爸给 Bernie Sanders 投票。每次他都说：还有谁支持全民医保？还有谁支持老年医保？Adolf Hitler。我说：not for everybody（不是对所有人）。", "relation": "承接6.4：爸爸政治"},
    {"id": "6.6", "title": "免费大学", "text": "我试图把我71岁的父亲变成社会主义者。我说：给我一个反对免费大学教育的好理由。所以他给我发了一个链接，link to my website（链接到我的网站）。", "relation": "承接6.5"},
    {"id": "6.7", "title": "喜剧延迟", "text": "写笑话需要很多时间。就像看星星，你不是看到星星现在的样子，而是看到它光年前的过去。这就是单口喜剧。我讲的事情好像刚发生，但在现实生活中，我已经完全崩溃了。", "relation": "承接6.6：创作感悟"},
    {"id": "6.8", "title": "SVU", "text": "我想在 Law & Order SVU 上扮演律师。但 NBC 上没人真正说脏话。他们想让所有的强奸和娈童 fun for the whole family（全家都能看）。", "relation": "承接6.7：媒体观察"},
    {"id": "6.9", "title": "发现尸体", "text": "如果你倒垃圾时垃圾桶里有一具尸体，电视上的人会说：I don't remember throwing that away（我不记得扔了那个）。我会说：哦操。天啊。在滴吗？操。我的鞋上有了吗？", "relation": "承接6.8：电视与现实对比"},
    {"id": "6.10", "title": "CSAM术语", "text": "你不能用 child porn（儿童色情）这个词，因为它暗示是双方同意的色情。适当的术语是 child sexual abuse materials（儿童性虐待材料），这很有道理，但 that's a lot to type with one hand（单手打字太长了）。", "relation": "承接6.9：术语话题"},
    {"id": "6.11", "title": "邮件回复", "text": "上次我讲这个笑话，15分钟后我收到一封邮件。这个女人简单地写道：儿童色情没什么好笑的。我说：what the fuck did I just tell you about that phrase?（我刚才跟你说了不要用那个词，你他妈没听见吗？）", "relation": "承接6.10"}
]

for slide_idx in range(0, len(social_jokes), 2):
    blank_layout = prs2.slide_layouts[6]
    slide = prs2.slides.add_slide(blank_layout)
    
    if slide_idx == 0:
        title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.2), Inches(12.333), Inches(0.6))
        tf = title_box.text_frame
        p = tf.paragraphs[0]
        p.text = "【社会观察】主题笑点详解 - Tom Segura Thief of Joy"
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = TITLE_COLOR
        p.alignment = PP_ALIGN.CENTER
        start_y = 1.0
    else:
        start_y = 0.4
    
    for i, joke in enumerate(social_jokes[slide_idx:slide_idx + 2]):
        y_pos = start_y + i * 3.4
        shape = slide.shapes.add_shape(1, Inches(0.5), Inches(y_pos), Inches(12.333), Inches(3.1))
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(174, 214, 241)  # 浅蓝
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

ppt_path2 = '/root/.openclaw/workspace/transcripts/Thief_of_Joy_社会观察.pptx'
prs2.save(ppt_path2)
print(f"✅ 社会观察主题PPT已生成: 6页")
print("\\n🎉 全部6个主题PPT已完成！")

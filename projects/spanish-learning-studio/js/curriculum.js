window.curriculum = [
  {
    id: "day-001",
    dayNumber: 1,
    title: "问候与自我介绍",
    goals: [
      "会读并会说 10 个基础表达",
      "能完成 20-30 秒自我介绍",
      "掌握 mucho gusto 等高频短句的重音"
    ],
    vocab: [
      { es: "hola", zh: "你好", ipa: "ˈo.la", hint: "哦-拉" },
      { es: "buenos días", zh: "早上好", ipa: "ˈbwe.nos ˈdi.as", hint: "布埃诺斯-迪亚斯" },
      { es: "me llamo", zh: "我叫", ipa: "me ˈʝa.mo", hint: "梅-亚莫" },
      { es: "soy", zh: "我是", ipa: "soj", hint: "索伊" },
      { es: "de China", zh: "来自中国", ipa: "de ˈtʃi.na", hint: "德-奇纳" },
      { es: "mucho gusto", zh: "很高兴认识你", ipa: "ˈmu.tʃo ˈɡus.to", hint: "穆乔-古斯托" }
    ],
    sentences: [
      { es: "Hola, me llamo Roy.", zh: "你好，我叫 Roy。", ipa: "ˈo.la | me ˈʝa.mo roj" },
      { es: "Soy consultor.", zh: "我是咨询顾问。", ipa: "soj kon.sulˈtoɾ" },
      { es: "Soy de China.", zh: "我来自中国。", ipa: "soj de ˈtʃi.na" },
      { es: "Mucho gusto.", zh: "很高兴认识你。", ipa: "ˈmu.tʃo ˈɡus.to" },
      { es: "Gracias.", zh: "谢谢。", ipa: "ˈɡɾa.sjas" },
      { es: "Por favor.", zh: "请。", ipa: "poɾ faˈβoɾ" },
      { es: "Buenos días.", zh: "早上好。", ipa: "ˈbwe.nos ˈdi.as" },
      { es: "Buenas tardes.", zh: "下午好。", ipa: "ˈbwe.nas ˈtaɾ.ðes" },
      { es: "Sí.", zh: "是。", ipa: "si" },
      { es: "No.", zh: "不。", ipa: "no" }
    ],
    practice: {
      shadowing: "每句先慢速1遍，再正常2遍",
      outputTask: "完成两句自我介绍：Hola, me llamo ___. / Soy de ___."
    },
    practiceItems: [
      { type: "spelling", prompt: "你好", answer: "hola", hint: "开场问候" },
      { type: "spelling", prompt: "我叫", answer: "me llamo", hint: "自我介绍核心短语" },
      { type: "spelling", prompt: "很高兴认识你", answer: "mucho gusto", hint: "固定表达" },
      { type: "cloze", prompt: "Hola, me ____ Roy.", answer: "llamo", hint: "表示“我叫...”" },
      { type: "cloze", prompt: "Soy ____ China.", answer: "de", hint: "来自某地用 de" },
      { type: "cloze", prompt: "Mucho ____.", answer: "gusto", hint: "固定搭配" },
      { type: "reorder", prompt: "请按正确语序排列：Soy / de / China", answer: "Soy de China", hint: "主语+介词+地名" },
      { type: "translate", prompt: "请翻译：你好，我叫 Roy。", answer: "Hola, me llamo Roy", hint: "关键词：hola + me llamo + Roy" }
    ]
  },
  {
    id: "day-002",
    dayNumber: 2,
    title: "职业、国家与基础问答",
    goals: [
      "掌握 10 个职业/国家相关高频表达",
      "能回答 ¿Cómo te llamas? / ¿De dónde eres? / ¿A qué te dedicas?",
      "理解 ser + de + 地点 与 ser + 职业 的基础句型"
    ],
    vocab: [
      { es: "¿Cómo te llamas?", zh: "你叫什么名字？", ipa: "ˈko.mo te ˈʝa.mas", hint: "科莫-特-亚马斯" },
      { es: "Me llamo...", zh: "我叫……", ipa: "me ˈʝa.mo", hint: "梅-亚莫" },
      { es: "¿De dónde eres?", zh: "你来自哪里？", ipa: "de ˈdon.de ˈe.ɾes", hint: "德-东德-埃雷斯" },
      { es: "Soy de...", zh: "我来自……", ipa: "soj de", hint: "索伊-德" },
      { es: "¿A qué te dedicas?", zh: "你从事什么工作？", ipa: "a ke te ðeˈði.kas", hint: "阿-克-特-德迪卡斯" },
      { es: "Soy consultor.", zh: "我是咨询顾问。", ipa: "soj kon.sulˈtoɾ", hint: "索伊-孔苏尔托尔" },
      { es: "Soy estudiante.", zh: "我是学生。", ipa: "soj es.tuˈðjan.te", hint: "索伊-埃斯图迪安特" },
      { es: "Soy profesor.", zh: "我是老师。", ipa: "soj pɾo.feˈsoɾ", hint: "索伊-普罗费索尔" },
      { es: "China", zh: "中国", ipa: "ˈtʃi.na", hint: "奇纳" },
      { es: "España", zh: "西班牙", ipa: "esˈpa.ɲa", hint: "埃斯帕尼亚" }
    ],
    sentences: [
      { es: "¿Cómo te llamas?", zh: "你叫什么名字？", ipa: "ˈko.mo te ˈʝa.mas" },
      { es: "Me llamo Roy.", zh: "我叫 Roy。", ipa: "me ˈʝa.mo roj" },
      { es: "¿De dónde eres?", zh: "你来自哪里？", ipa: "de ˈdon.de ˈe.ɾes" },
      { es: "Soy de China.", zh: "我来自中国。", ipa: "soj de ˈtʃi.na" },
      { es: "¿A qué te dedicas?", zh: "你做什么工作？", ipa: "a ke te ðeˈði.kas" },
      { es: "Soy consultor.", zh: "我是咨询顾问。", ipa: "soj kon.sulˈtoɾ" },
      { es: "Soy estudiante.", zh: "我是学生。", ipa: "soj es.tuˈðjan.te" },
      { es: "Soy profesor.", zh: "我是老师。", ipa: "soj pɾo.feˈsoɾ" },
      { es: "Mucho gusto.", zh: "很高兴认识你。", ipa: "ˈmu.tʃo ˈɡus.to" },
      { es: "Gracias.", zh: "谢谢。", ipa: "ˈɡɾa.sjas" }
    ],
    grammar: [
      { point: "疑问句基本结构", note: "西语疑问句常用倒问号 ¿...?，语序可与陈述句接近，如 ¿Cómo te llamas?" },
      { point: "ser + de + 地点", note: "表达来自某地：Soy de China. / Soy de España." },
      { point: "ser + 职业（通常不加冠词）", note: "表达职业时一般不用 un/una：Soy consultor.（不是 Soy un consultor.）" }
    ],
    practice: {
      shadowing: "每句先慢速1遍，再正常2遍，重点模仿疑问句语调",
      outputTask: "完成三句问答：Me llamo ___. / Soy de ___. / Soy ___."
    },
    practiceItems: [
      { type: "spelling", prompt: "你来自哪里？", answer: "¿De dónde eres?", hint: "完整疑问句，注意重音和问号", unitIds: ["de_donde_eres"], sourceDay: "day-002" },
      { type: "spelling", prompt: "我来自（某地）", answer: "Soy de", hint: "国家前常用 de", unitIds: ["ser_de"], sourceDay: "day-002" },
      { type: "cloze", prompt: "Me ____ Roy.", answer: "llamo", hint: "自我介绍动词 llamar", unitIds: ["me_llamo"], sourceDay: "day-002" },
      { type: "cloze", prompt: "¿De dónde ____?", answer: "eres", hint: "主语 tú 对应 eres", unitIds: ["ser_eres"], sourceDay: "day-002" },
      { type: "cloze", prompt: "Soy ____ China.", answer: "de", hint: "来自某地用 de", unitIds: ["ser_de"], sourceDay: "day-002" },
      { type: "reorder", prompt: "请按正确语序排列：Soy / consultor", answer: "Soy consultor", hint: "职业表达不加冠词", unitIds: ["ser_profesion"], sourceDay: "day-002" },
      { type: "translate", prompt: "请翻译：我来自西班牙。", answer: "Soy de España", hint: "Soy de + 国家", unitIds: ["ser_de"], sourceDay: "day-002" },
      { type: "translate", prompt: "请翻译：你从事什么工作？", answer: "¿A qué te dedicas?", hint: "高频问职业句型", unitIds: ["a_que_te_dedicas"], sourceDay: "day-002" }
    ]
  }
];

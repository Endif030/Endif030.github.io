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
  }
];

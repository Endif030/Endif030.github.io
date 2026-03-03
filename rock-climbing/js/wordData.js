const WordRoots = [
  {
    id: 1,
    root: "抓握点 (Hold)",
    origin: "基础术语",
    meaning: "岩壁上供手抓握的凸起或凹陷部位",
    description: "抓握点是攀岩者与岩壁接触的主要部位，根据形状和大小可分为大把手(Jug)、捏握点(Pinch)、指洞点(Crimp)等。正确识别和利用抓握点是攀岩技术的核心。抓握点的选择直接影响攀爬效率和疲劳程度，初学者应优先选择大把手点建立信心。",
    examples: [
      {
        word: "大把手点",
        meaning: "足够容纳整个手掌的大凸起",
        breakdown: { root: "抓握点" },
        explanation: "最容易抓握的点，适合休息和恢复体力"
      },
      {
        word: "指洞点",
        meaning: "只能容纳1-2根手指的小凹陷",
        breakdown: { root: "抓握点" },
        explanation: "需要较强的指力，常见于高难度线路"
      },
      {
        word: "捏握点",
        meaning: "需要用手指和拇指对捏的凸起",
        breakdown: { root: "抓握点" },
        explanation: "考验手指力量，需要正确的捏握技巧"
      }
    ],
    quiz: {
      question: "以下哪种抓握点最适合初学者？",
      options: ["指洞点", "大把手点", "捏握点", "摩擦点"],
      correctAnswer: 1
    }
  },
  {
    id: 2,
    root: "踩点 (Footwork)",
    origin: "基础技术",
    meaning: "利用脚部力量支撑身体重量的技术",
    description: "攀岩中70%的力量应来自腿部而非手臂。良好的踩点技术包括脚尖踩点、脚跟钩挂、脚尖钩挂等。正确的踩点可以减少手臂疲劳，提高攀爬效率。初学者常见错误是过度依赖手臂力量，应注重练习腿部发力和身体重心的转移。",
    examples: [
      {
        word: "脚尖踩点",
        meaning: "用攀岩鞋的前端精确踩在小点上",
        breakdown: { root: "踩点" },
        explanation: "最基础的踩点方式，需要精确的脚部定位"
      },
      {
        word: "脚跟钩挂",
        meaning: "用脚后跟钩住岩壁上的凸起",
        breakdown: { root: "踩点" },
        explanation: "用于固定身体位置或辅助转身动作"
      },
      {
        word: "脚尖钩挂",
        meaning: "用脚尖钩住岩壁下方的凸起",
        breakdown: { root: "踩点" },
        explanation: "常用于屋顶线路或需要对抗重力的动作"
      }
    ],
    quiz: {
      question: "攀岩时应该用哪个部位发力为主？",
      options: ["手臂", "腿部", "背部", "核心"],
      correctAnswer: 1
    }
  },
  {
    id: 3,
    root: "保护系统 (Protection)",
    origin: "安全装备",
    meaning: "防止坠落受伤的整套安全装置和流程",
    description: "保护系统是攀岩安全的基石，包括安全带、绳索、快挂、保护器等装备。正确的保护流程是：检查装备→穿戴安全带→系绳结→做双重检查→开始攀爬。任何疏忽都可能导致严重后果。记住：生命只有一次，检查永不嫌多。",
    examples: [
      {
        word: "动力绳",
        meaning: "具有一定弹性的攀岩专用绳索",
        breakdown: { root: "保护系统" },
        explanation: "可以吸收坠落冲击力，保护攀岩者不受伤害"
      },
      {
        word: "快挂",
        meaning: "连接绳索和岩壁挂片的装置",
        breakdown: { root: "保护系统" },
        explanation: "由两个铁锁和一根扁带组成，是运动攀岩的基本保护装备"
      },
      {
        word: "保护器",
        meaning: "控制绳索收放的装置",
        breakdown: { root: "保护系统" },
        explanation: "保护员使用，可以在坠落时快速制动"
      }
    ],
    quiz: {
      question: "攀岩前最重要的步骤是什么？",
      options: ["选择路线", "检查装备", "热身运动", "拍照留念"],
      correctAnswer: 1
    }
  },
  {
    id: 4,
    root: "八字结 (Figure-8)",
    origin: "绳结技术",
    meaning: "攀岩中最常用的安全带连接绳结",
    description: "八字结因其形状像数字8而得名，是攀岩中最安全、最常用的绳结。它的特点是受力后不易松开，且容易检查是否正确。打结时必须确保至少预留10厘米尾绳，并做双重检查。记住口诀：穿、绕、回、紧、查。",
    examples: [
      {
        word: "双八字结",
        meaning: "反穿八字结的加强版",
        breakdown: { root: "八字结" },
        explanation: "用于连接安全带，是攀岩者必须掌握的基础技能"
      },
      {
        word: "单八字结",
        meaning: "在绳端形成的八字结",
        breakdown: { root: "八字结" },
        explanation: "常用于制作绳圈或连接快挂"
      },
      {
        word: "兔耳八字结",
        meaning: "带有两个绳圈的八字结",
        breakdown: { root: "八字结" },
        explanation: "用于顶绳攀登时的固定点连接"
      }
    ],
    quiz: {
      question: "八字结的特点是什么？",
      options: ["容易松开", "不易检查", "受力后不易松开", "打法简单"],
      correctAnswer: 2
    }
  },
  {
    id: 5,
    root: "先锋攀登 (Lead Climbing)",
    origin: "攀登方式",
    meaning: "一边攀登一边放置保护点的攀登方式",
    description: "先锋攀登是运动攀岩和传统攀岩的主要方式。攀登者带着绳索向上攀爬，每到一个保护点就将绳索挂入快挂。如果坠落，会从最后一个保护点下方开始坠落。先锋攀登需要更高的技术水平和心理素质，是攀岩进阶的必经之路。",
    examples: [
      {
        word: "挂绳",
        meaning: "将绳索扣入快挂的动作",
        breakdown: { root: "先锋攀登" },
        explanation: "需要单手操作，是先锋攀登的基本技能"
      },
      {
        word: "冲坠",
        meaning: "先锋攀登时的坠落",
        breakdown: { root: "先锋攀登" },
        explanation: "需要从心理上适应，是学习先锋攀登的重要部分"
      },
      {
        word: "保护点",
        meaning: "固定在岩壁上的锚点",
        breakdown: { root: "先锋攀登" },
        explanation: "用于连接快挂，防止坠落距离过长"
      }
    ],
    quiz: {
      question: "先锋攀登时坠落会从哪开始？",
      options: ["地面", "最后一个保护点下方", "顶峰", "中途随机"],
      correctAnswer: 1
    }
  },
  {
    id: 6,
    root: "顶绳攀登 (Top-Rope)",
    origin: "攀登方式",
    meaning: "绳索从上方保护点的攀登方式",
    description: "顶绳攀登是最适合初学者的攀登方式。绳索预先固定在上方，保护员在下方控制绳索。坠落时几乎没有自由落体，非常安全。这是学习基本动作和建立信心的最佳方式。大多数攀岩馆都采用这种方式进行教学和娱乐攀登。",
    examples: [
      {
        word: "保护员",
        meaning: "在下方控制绳索的伙伴",
        breakdown: { root: "顶绳攀登" },
        explanation: "需要密切观察攀登者，随时准备收绳"
      },
      {
        word: "缓冲坠落",
        meaning: "保护员给予一定缓冲的坠落",
        breakdown: { root: "顶绳攀登" },
        explanation: "软着陆可以减少对攀登者的冲击"
      },
      {
        word: "预挂绳",
        meaning: "事先设置好的顶绳",
        breakdown: { root: "顶绳攀登" },
        explanation: "常见于攀岩馆，方便快速攀爬"
      }
    ],
    quiz: {
      question: "哪种攀登方式最适合初学者？",
      options: ["先锋攀登", "顶绳攀登", "抱石", "自由攀登"],
      correctAnswer: 1
    }
  },
  {
    id: 7,
    root: "抱石 (Bouldering)",
    origin: "攀登方式",
    meaning: "不使用绳索，在较低岩壁上的攀登",
    description: "抱石是在4-5米高的岩壁上进行的无绳攀登，下方铺设厚垫子作为保护。抱石强调力量和技术，动作通常比攀岩更动态和爆发。它是提升技术、增强力量的绝佳训练方式，也是现代攀岩比赛中备受瞩目的项目。",
    examples: [
      {
        word: "厚垫子",
        meaning: "铺在下方缓冲坠落的垫子",
        breakdown: { root: "抱石" },
        explanation: "通常需要多块拼接，完全覆盖可能的坠落区域"
      },
      {
        word: "动态动作",
        meaning: "通过爆发力完成的动作",
        breakdown: { root: "抱石" },
        explanation: "如跳抓、摆荡等，是抱石的特色动作"
      },
      {
        word: "起步",
        meaning: "抱石线路的开始动作",
        breakdown: { root: "抱石" },
        explanation: "通常有规定的起始手点和脚点"
      }
    ],
    quiz: {
      question: "抱石时用什么代替绳索保护？",
      options: ["安全带", "厚垫子", "头盔", "手套"],
      correctAnswer: 1
    }
  },
  {
    id: 8,
    root: "难度等级 (Grade)",
    origin: "评级系统",
    meaning: "表示攀岩线路难度的分级标准",
    description: "攀岩难度有不同的评级系统：法国系统(5a-9c)、美国优胜美地系统(5.0-5.15d)等。数字越大表示难度越高。初学者通常从5.7/5a开始，5.10/6a属于中级水平，5.12/7a+已经是高级水平。等级只是参考，不同岩场的同等级可能有差异。",
    examples: [
      {
        word: "5.10a",
        meaning: "美国系统的入门级中级难度",
        breakdown: { root: "难度等级" },
        explanation: "适合有一定基础的攀岩者"
      },
      {
        word: "6a",
        meaning: "法国系统的入门中级难度",
        breakdown: { root: "难度等级" },
        explanation: "与美国的5.10a相当"
      },
      {
        word: "V4",
        meaning: "抱石系统的初级难度",
        breakdown: { root: "难度等级" },
        explanation: "适合练习各种基础技巧"
      }
    ],
    quiz: {
      question: "法国系统的5a相当于美国系统的多少？",
      options: ["5.7", "5.8", "5.9", "5.10"],
      correctAnswer: 1
    }
  },
  {
    id: 9,
    root: "三点接触 (Three-Point Contact)",
    origin: "技术原则",
    meaning: "始终保持三个肢体接触岩壁的稳定原则",
    description: "三点接触是攀岩中的黄金法则：移动一个肢体时，其他三个肢体保持与岩壁的接触。这确保了在动作过程中始终有稳定的支撑点。遵循这个原则可以大大提高攀爬的安全性和效率，是初学者最需要养成的习惯。",
    examples: [
      {
        word: "静态攀爬",
        meaning: "缓慢、控制好的攀爬方式",
        breakdown: { root: "三点接触" },
        explanation: "严格遵循三点接触原则，适合初学者"
      },
      {
        word: "重心转移",
        meaning: "将身体重量转移到支撑点的动作",
        breakdown: { root: "三点接触" },
        explanation: "在三点接触的基础上移动身体重心"
      },
      {
        word: "平衡姿势",
        meaning: "身体重量均匀分布的稳定姿态",
        breakdown: { root: "三点接触" },
        explanation: "三点接触帮助维持的最佳攀爬姿态"
      }
    ],
    quiz: {
      question: "攀岩时应该保持几点接触岩壁？",
      options: ["两点", "三点", "四点", "没有固定要求"],
      correctAnswer: 1
    }
  },
  {
    id: 10,
    root: "手臂伸直 (Straight Arms)",
    origin: "技术原则",
    meaning: "攀爬时保持手臂伸直以节省体力的技巧",
    description: "手臂伸直是节能攀爬的关键技巧。弯曲的手臂需要肌肉持续用力，很快就会疲劳；而伸直的手臂可以让骨骼承担大部分重量，肌肉得到休息。这个原则贯穿整个攀岩过程，是区分新手和老手的重要标志。",
    examples: [
      {
        word: "锁定",
        meaning: "手臂弯曲用力拉的动作",
        breakdown: { root: "手臂伸直" },
        explanation: "应该尽量避免，只在必要时使用"
      },
      {
        word: "休息姿势",
        meaning: "在岩壁上恢复体力的姿态",
        breakdown: { root: "手臂伸直" },
        explanation: "手臂伸直，重心靠近岩壁"
      },
      {
        word: "垂臂",
        meaning: "让手臂自然下垂放松",
        breakdown: { root: "手臂伸直" },
        explanation: "在好点上可以短暂休息恢复"
      }
    ],
    quiz: {
      question: "为什么要保持手臂伸直？",
      options: ["看起来好看", "节省体力", "更容易发力", "传统要求"],
      correctAnswer: 1
    }
  },
  {
    id: 11,
    root: "重心 (Center of Gravity)",
    origin: "身体控制",
    meaning: "身体重量的集中点，攀岩中需要精确控制",
    description: "控制重心是攀岩技术的核心。通过移动髋部、扭转身体、调整脚点位置来改变重心位置，可以让动作变得更轻松。好的重心控制可以让困难的动作变得简单，是提升攀爬效率的关键。",
    examples: [
      {
        word: "贴墙",
        meaning: "让重心靠近岩壁",
        breakdown: { root: "重心" },
        explanation: "减少手臂负担，增加稳定性"
      },
      {
        word: "侧拉",
        meaning: "侧身拉动身体移动",
        breakdown: { root: "重心" },
        explanation: "利用身体扭转转移重心"
      },
      {
        word: "旗式",
        meaning: "用腿在身体侧面保持平衡",
        breakdown: { root: "重心" },
        explanation: "类似旗帜飘动，帮助维持重心"
      }
    ],
    quiz: {
      question: "攀岩时重心应该在哪？",
      options: ["远离岩壁", "靠近岩壁", "正中间", "随意"],
      correctAnswer: 1
    }
  },
  {
    id: 12,
    root: "呼吸 (Breathing)",
    origin: "身体控制",
    meaning: "攀爬时保持正常呼吸节奏的技巧",
    description: "很多初学者在困难动作时会屏住呼吸，这会导致肌肉更快疲劳。保持稳定的呼吸节奏可以给肌肉持续供氧，延缓疲劳。困难动作前深呼吸，动作中保持呼吸，不要憋气。",
    examples: [
      {
        word: "深呼吸",
        meaning: "动作前深吸一口气",
        breakdown: { root: "呼吸" },
        explanation: "为即将发力的动作储备氧气"
      },
      {
        word: "节奏呼吸",
        meaning: "与动作配合的呼吸模式",
        breakdown: { root: "呼吸" },
        explanation: "如：抓点时呼气，移动时吸气"
      },
      {
        word: "屏息",
        meaning: "不自觉地停止呼吸",
        breakdown: { root: "呼吸" },
        explanation: "需要克服的坏习惯，会导致快速疲劳"
      }
    ],
    quiz: {
      question: "攀岩困难时应该怎么做？",
      options: ["屏住呼吸", "保持呼吸", "快速喘气", "大声喊叫"],
      correctAnswer: 1
    }
  },
  {
    id: 13,
    root: "镁粉 (Chalk)",
    origin: "辅助装备",
    meaning: "用于保持手部干燥的碳酸镁粉末",
    description: "镁粉可以吸收手汗，增加摩擦力，防止手滑。通常装在镁粉袋中挂在腰后。使用时拍一拍双手即可，不要过度使用以免粉尘飞扬。现代攀岩馆通常要求使用液体镁粉以减少粉尘。",
    examples: [
      {
        word: "镁粉袋",
        meaning: "装镁粉的小袋子",
        breakdown: { root: "镁粉" },
        explanation: "挂在腰后，方便随时取粉"
      },
      {
        word: "液体镁粉",
        meaning: "含镁粉的酒精溶液",
        breakdown: { root: "镁粉" },
        explanation: "涂抹后酒精挥发，留下镁粉层，粉尘更少"
      },
      {
        word: "拍粉",
        meaning: "双手拍打镁粉袋取粉",
        breakdown: { root: "镁粉" },
        explanation: "攀岩前和出汗后都要做"
      }
    ],
    quiz: {
      question: "镁粉的主要作用是什么？",
      options: ["增加美观", "保持手部干燥", "防止受伤", "标记路线"],
      correctAnswer: 1
    }
  },
  {
    id: 14,
    root: "攀岩鞋 (Climbing Shoes)",
    origin: "核心装备",
    meaning: "专为攀岩设计的紧身鞋，鞋底采用高摩擦橡胶",
    description: "攀岩鞋是攀岩最重要的装备。它们比普通鞋紧很多，鞋尖收窄便于踩小点，鞋底采用特殊橡胶提供高摩擦力。新鞋通常需要磨合期。选择合适尺码的攀岩鞋很重要：太松影响精准度，太紧会导致疼痛。",
    examples: [
      {
        word: "鞋尖",
        meaning: "鞋的前端收窄部分",
        breakdown: { root: "攀岩鞋" },
        explanation: "用于踩小点和精确施力"
      },
      {
        word: "摩擦橡胶",
        meaning: "高摩擦系数的鞋底材料",
        breakdown: { root: "攀岩鞋" },
        explanation: "提供与岩壁的摩擦力，不同品牌配方不同"
      },
      {
        word: "系带式",
        meaning: "用鞋带固定的攀岩鞋",
        breakdown: { root: "攀岩鞋" },
        explanation: "可以精确调节松紧，适合多用途"
      }
    ],
    quiz: {
      question: "攀岩鞋为什么要紧？",
      options: ["为了好看", "增加精准度", "传统要求", "防止脱落"],
      correctAnswer: 1
    }
  },
  {
    id: 15,
    root: "安全带 (Harness)",
    origin: "安全装备",
    meaning: "穿在身上的保护装置，用于连接绳索",
    description: "安全带是攀岩安全的生命线。现代安全带由腰带和腿环组成，通过扣具固定。使用时必须双重检查所有扣具是否正确扣好。安全带要合身但不过紧，确保在坠落时不会脱落或造成不适。",
    examples: [
      {
        word: "腰带",
        meaning: "安全带环绕腰部的部分",
        breakdown: { root: "安全带" },
        explanation: "主要受力点，坠落时承受大部分力量"
      },
      {
        word: "腿环",
        meaning: "环绕大腿的部分",
        breakdown: { root: "安全带" },
        explanation: "分散坠落力量，保持倒立时的安全"
      },
      {
        word: "保护环",
        meaning: "安全带前方用于连接绳索的环",
        breakdown: { root: "安全带" },
        explanation: "必须始终位于身体正中"
      }
    ],
    quiz: {
      question: "使用安全带前最重要的是什么？",
      options: ["调整松紧", "双重检查", "选择颜色", "询问他人"],
      correctAnswer: 1
    }
  },
  {
    id: 16,
    root: "读线 (Route Reading)",
    origin: "技术策略",
    meaning: "攀爬前观察和分析线路的动作序列",
    description: "读线是在攀爬前观察岩壁、规划动作、预判难点的重要步骤。好的读线可以节省大量体力，避免在岩壁上浪费能量思考。读线时要注意：关键手点脚点的位置、可能的休息点、难点动作、可能的Beta（攀爬方案）。",
    examples: [
      {
        word: "Beta",
        meaning: "攀爬某条线路的方法",
        breakdown: { root: "读线" },
        explanation: "可以询问他人或自己探索"
      },
      {
        word: "休息点",
        meaning: "可以放松恢复的位置",
        breakdown: { root: "读线" },
        explanation: "通常是好的大把手点，读线时要识别"
      },
      {
        word: "关键点",
        meaning: "线路中最难的动作",
        breakdown: { root: "读线" },
        explanation: "需要特别注意和准备的难点"
      }
    ],
    quiz: {
      question: "攀爬前应该做什么？",
      options: ["直接上", "读线分析", "拉伸热身", "发朋友圈"],
      correctAnswer: 1
    }
  },
  {
    id: 17,
    root: "序列 (Sequence)",
    origin: "技术策略",
    meaning: "完成一段线路的手脚动作顺序",
    description: "序列是指完成一组动作的特定顺序。好的序列可以让困难的动作变得简单。序列通常由手点顺序和脚点顺序组成，需要协调配合。找到最适合自己的序列是攀岩的艺术之一，不同身高和体型的人可能有不同的最优序列。",
    examples: [
      {
        word: "交叉手",
        meaning: "两手交叉抓点的动作",
        breakdown: { root: "序列" },
        explanation: "常用于保持身体平衡或完成远距离移动"
      },
      {
        word: "换脚",
        meaning: "在同一踩点上更换脚",
        breakdown: { root: "序列" },
        explanation: "优化身体位置，为下一步做准备"
      },
      {
        word: "drop knee",
        meaning: "膝盖下沉的姿势",
        breakdown: { root: "序列" },
        explanation: "可以增加手臂reach距离"
      }
    ],
    quiz: {
      question: "什么是序列？",
      options: ["攀岩装备", "动作顺序", "难度等级", "安全规则"],
      correctAnswer: 1
    }
  },
  {
    id: 18,
    root: "Crimp (指力点)",
    origin: "抓握技术",
    meaning: "只能用指尖抓握的小点，考验指力",
    description: "Crimp 是最考验手指力量的抓握点，只有指尖能接触岩壁。抓 Crimp 时要特别注意：保持手臂伸直减少负荷、不要过度依赖 Crimp、注意手指保护避免受伤。长期过度训练 Crimp 可能导致手指肌腱损伤。",
    examples: [
      {
        word: "全Crimp",
        meaning: "拇指压在手指上的抓法",
        breakdown: { root: "Crimp" },
        explanation: "力量最强但对关节压力最大"
      },
      {
        word: "半Crimp",
        meaning: "拇指不参与的正手抓法",
        breakdown: { root: "Crimp" },
        explanation: "平衡力量和关节保护"
      },
      {
        word: "开放抓",
        meaning: "手指不完全闭合的抓法",
        breakdown: { root: "Crimp" },
        explanation: "对关节压力最小，适合保护手指"
      }
    ],
    quiz: {
      question: "抓Crimp时应该注意什么？",
      options: ["用力拉", "保护手指", "弯曲手臂", "快速通过"],
      correctAnswer: 1
    }
  },
  {
    id: 19,
    root: "Sloper (摩擦点)",
    origin: "抓握技术",
    meaning: "没有明显边缘的圆滑凸起，依靠摩擦力抓握",
    description: "Sloper 是没有明显边缘的圆滑抓握点，完全依靠手掌和手指与岩壁的摩擦力。抓 Sloper 的技巧包括：最大化接触面积、保持重心正确、不要用力过猛（反而容易滑脱）。Sloper 考验身体位置和心理控制，很多人害怕滑脱而不敢用力。",
    examples: [
      {
        word: "手掌贴合",
        meaning: "用整个手掌贴合Sloper",
        breakdown: { root: "Sloper" },
        explanation: "最大化接触面积增加摩擦力"
      },
      {
        word: "重心控制",
        meaning: "保持正确的身体位置",
        breakdown: { root: "Sloper" },
        explanation: "重心正确时Sloper才容易抓稳"
      },
      {
        word: "心理克服",
        meaning: "克服对滑脱的恐惧",
        breakdown: { root: "Sloper" },
        explanation: "相信摩擦力，放松但稳固地抓握"
      }
    ],
    quiz: {
      question: "抓Sloper时最重要的是什么？",
      options: ["用力抓", "摩擦力", "快速移动", "避免接触"],
      correctAnswer: 1
    }
  },
  {
    id: 20,
    root: "Pocket (指洞)",
    origin: "抓握技术",
    meaning: "岩壁上的凹陷，可以插入手指",
    description: "Pocket 是岩壁上的凹陷孔洞，可以插入1-4根手指。根据可插入手指数量分为一指洞、二指洞、三指洞等。手指插入越深越安全，但也要注意角度避免扭伤。Pocket 是某些岩场（如石灰岩）的特色抓点。",
    examples: [
      {
        word: "单指洞",
        meaning: "只能插入一根手指的洞",
        breakdown: { root: "Pocket" },
        explanation: "对单指力量要求极高"
      },
      {
        word: "双指洞",
        meaning: "可以插入两根手指的洞",
        breakdown: { root: "Pocket" },
        explanation: "最常见，通常是中指和食指"
      },
      {
        word: "全指洞",
        meaning: "可以插入四根手指的洞",
        breakdown: { root: "Pocket" },
        explanation: "相当于小把手点，相对容易"
      }
    ],
    quiz: {
      question: "Pocket是什么？",
      options: ["攀岩装备", "岩壁凹陷", "安全装置", "绳结类型"],
      correctAnswer: 1
    }
  },
  {
    id: 21,
    root: "Undercut (反提)",
    origin: "抓握技术",
    meaning: "从下方向上抓握的反向手点",
    description: "Undercut 是方向朝下的手点，需要从下方向上抓握。抓 Undercut 时身体通常需要贴近岩壁，利用腿部力量向上推。Undercut 常出现在屋顶线路和悬垂线路上，是进阶技术的重要组成部分。",
    examples: [
      {
        word: "反拉",
        meaning: "利用Undercut向下拉的动作",
        breakdown: { root: "Undercut" },
        explanation: "配合腿部发力向上推进"
      },
      {
        word: "身体姿态",
        meaning: "使用Undercut时的身体位置",
        breakdown: { root: "Undercut" },
        explanation: "通常需要身体贴近岩壁"
      },
      {
        word: "配合脚点",
        meaning: "与Undercut配合使用的脚点",
        breakdown: { root: "Undercut" },
        explanation: "好的脚点可以让Undercut更容易"
      }
    ],
    quiz: {
      question: "Undercut的方向是？",
      options: ["朝上", "朝下", "朝左", "朝右"],
      correctAnswer: 1
    }
  },
  {
    id: 22,
    root: "Gaston (反向推)",
    origin: "抓握技术",
    meaning: "拇指朝下、手肘朝外的反向推压动作",
    description: "Gaston 是一种特殊的手点使用方法：手肘朝外，拇指朝下，利用反向推压的力量。这种动作常用于宽缝攀爬或需要身体向外推的情况。Gaston 对肩膀和核心力量要求较高，是一种进阶技术。",
    examples: [
      {
        word: "肘部外展",
        meaning: "手肘向外打开的姿势",
        breakdown: { root: "Gaston" },
        explanation: "Gaston动作的特征姿态"
      },
      {
        word: "反向发力",
        meaning: "向外推而不是向内拉",
        breakdown: { root: "Gaston" },
        explanation: "利用身体的对抗力量"
      },
      {
        word: "宽缝应用",
        meaning: "在宽裂缝中使用Gaston",
        breakdown: { root: "Gaston" },
        explanation: "宽缝攀爬的典型技术"
      }
    ],
    quiz: {
      question: "Gaston时拇指朝向？",
      options: ["上", "下", "左", "右"],
      correctAnswer: 1
    }
  },
  {
    id: 23,
    root: " heel hook (脚跟钩)",
    origin: "脚法技术",
    meaning: "用脚跟钩住岩壁上的凸起",
    description: "Heel hook 是用脚后跟钩住岩壁上的凸起或边缘，用于固定身体位置或产生向身体方向拉的力。这是克服难点的有效技术，常见于需要身体 tension（张力）的动作。Heel hook 可以解放双手或帮助身体旋转。",
    examples: [
      {
        word: "稳定身体",
        meaning: "利用heel hook固定位置",
        breakdown: { root: "heel hook" },
        explanation: "解放双手进行休息或挂绳"
      },
      {
        word: "产生拉力",
        meaning: "用heel hook向身体方向拉",
        breakdown: { root: "heel hook" },
        explanation: "配合手臂动作完成平衡"
      },
      {
        word: "转身辅助",
        meaning: "利用heel hook帮助身体旋转",
        breakdown: { root: "heel hook" },
        explanation: "在改变方向时特别有用"
      }
    ],
    quiz: {
      question: "heel hook主要用哪个部位？",
      options: ["脚尖", "脚跟", "脚内侧", "脚外侧"],
      correctAnswer: 1
    }
  },
  {
    id: 24,
    root: "toe hook (脚尖钩)",
    origin: "脚法技术",
    meaning: "用脚尖钩住岩壁下方的边缘或凸起",
    description: "Toe hook 是用脚尖向上钩住岩壁下方的边缘，常用于屋顶线路或需要对抗重力的动作。Toe hook 配合 heel hook 可以形成'双钩'，产生强大的身体张力。这种技术对核心力量和柔韧性有一定要求。",
    examples: [
      {
        word: "屋顶线路",
        meaning: "水平或向上倾斜的岩壁",
        breakdown: { root: "toe hook" },
        explanation: "toe hook在屋顶线路中特别重要"
      },
      {
        word: "双钩技术",
        meaning: "同时使用heel hook和toe hook",
        breakdown: { root: "toe hook" },
        explanation: "产生最大身体张力，解放双手"
      },
      {
        word: "核心发力",
        meaning: "用核心力量维持toe hook",
        breakdown: { root: "toe hook" },
        explanation: "需要强大的核心力量支撑"
      }
    ],
    quiz: {
      question: "toe hook主要用于哪种线路？",
      options: ["垂直线", "屋顶线", "slab线", "裂缝线"],
      correctAnswer: 1
    }
  },
  {
    id: 25,
    root: "smear (摩擦踩)",
    origin: "脚法技术",
    meaning: "在没有明显踩点的地方用鞋底摩擦岩壁",
    description: "Smear 是在没有明显凸起踩点时，直接用攀岩鞋的橡胶鞋底摩擦光滑岩壁的技术。成功的 smear 需要：干净的鞋底、正确的身体位置、信任的重心转移。Slab（缓坡）线路上 smear 是最常用的技术。",
    examples: [
      {
        word: "slab攀爬",
        meaning: "在缓坡岩壁上攀爬",
        breakdown: { root: "smear" },
        explanation: "slab线路主要依赖smear技术"
      },
      {
        word: "重心转移",
        meaning: "把重量转移到smear脚上",
        breakdown: { root: "smear" },
        explanation: "信任摩擦力，完全转移重心"
      },
      {
        word: "鞋底清洁",
        meaning: "保持攀岩鞋底部干净",
        breakdown: { root: "smear" },
        explanation: "灰尘会大大降低摩擦力"
      }
    ],
    quiz: {
      question: "smear靠什么提供支撑？",
      options: ["岩壁凸起", "鞋底摩擦", "脚部力量", "手臂拉力"],
      correctAnswer: 1
    }
  },
  {
    id: 26,
    root: "edging (边踩)",
    origin: "脚法技术",
    meaning: "用攀岩鞋的边缘踩在小的凸起上",
    description: "Edging 是用攀岩鞋的前端或外侧边缘踩在小的凸起上的技术。这是最常见的踩点方式，需要精确的脚部定位。好的 edging 技术可以让很小的点变得可用。保持脚踝稳定和身体平衡是成功 edging 的关键。",
    examples: [
      {
        word: "内边缘",
        meaning: "用大脚趾侧的鞋边",
        breakdown: { root: "edging" },
        explanation: "最常用的edging方式"
      },
      {
        word: "外边缘",
        meaning: "用小脚趾侧的鞋边",
        breakdown: { root: "edging" },
        explanation: "用于特殊的身体位置"
      },
      {
        word: "高踩",
        meaning: "脚踩在较高的位置",
        breakdown: { root: "edging" },
        explanation: "可以增加reach距离"
      }
    ],
    quiz: {
      question: "edging主要用鞋的哪个部位？",
      options: ["鞋跟", "鞋边", "鞋底", "鞋背"],
      correctAnswer: 1
    }
  },
  {
    id: 27,
    root: "mantle (撑台)",
    origin: "进阶技术",
    meaning: "用手撑在平台上将身体推上去的动作",
    description: "Mantle 是攀岩中模拟从游泳池边撑身上岸的动作：双手撑在平台上，用手臂和核心力量将身体推上去。这种技术常见于大平台的顶部或某些特定的抱石动作。Mantle 对肩膀和核心力量要求很高，是一种典型的进阶技术。",
    examples: [
      {
        word: "撑推",
        meaning: "用手撑台面向上推",
        breakdown: { root: "mantle" },
        explanation: "主要发力动作"
      },
      {
        word: "收腿",
        meaning: "将脚收到台面上",
        breakdown: { root: "mantle" },
        explanation: "mantle的最后一步"
      },
      {
        word: "平台顶",
        meaning: "岩壁顶端的水平面",
        breakdown: { root: "mantle" },
        explanation: "mantle最常见的应用场景"
      }
    ],
    quiz: {
      question: "mantle模仿的是哪个动作？",
      options: ["爬山", "上楼梯", "出泳池", "举重"],
      correctAnswer: 2
    }
  },
  {
    id: 28,
    root: "layback (反身拉)",
    origin: "进阶技术",
    meaning: "身体后仰、双手拉 crack 的攀爬方式",
    description: "Layback 是一种用于攀爬裂缝或边缘的技术：身体后仰，双手拉住裂缝的一边，双脚蹬住另一边，利用身体的 tension（张力）保持平衡。Layback 看起来优美但消耗体力很大，需要在适当时候转换为其他技术休息。",
    examples: [
      {
        word: "身体张力",
        meaning: "身体像弓一样紧绷的状态",
        breakdown: { root: "layback" },
        explanation: "layback的核心力学原理"
      },
      {
        word: "对角线",
        meaning: "手脚对角的layback姿势",
        breakdown: { root: "layback" },
        explanation: "左手左脚 vs 右手右脚"
      },
      {
        word: "裂缝攀爬",
        meaning: "在岩壁裂缝中攀爬",
        breakdown: { root: "layback" },
        explanation: "layback最常见的应用场景"
      }
    ],
    quiz: {
      question: "layback时身体姿态是？",
      options: ["贴墙", "后仰", "前倾", "侧向"],
      correctAnswer: 1
    }
  },
  {
    id: 29,
    root: " stemming (撑开)",
    origin: "进阶技术",
    meaning: "在两面岩壁之间用手脚撑开的动作",
    description: "Stemming 是在两面岩壁形成的角落或 chimney（烟囱）中，用手和脚分别撑住两边岩壁的技术。通过交替更换支撑点向上移动。Stemming 考验身体柔韧性和对重心的精细控制，是一种典型的多向受力技术。",
    examples: [
      {
        word: "chimney",
        meaning: "像烟囱一样的垂直裂缝",
        breakdown: { root: "stemming" },
        explanation: "stemming的主要应用场景"
      },
      {
        word: "对角支撑",
        meaning: "左手右脚或右手左脚撑开",
        breakdown: { root: "stemming" },
        explanation: "stemming的基本姿态"
      },
      {
        word: "休息姿态",
        meaning: "在stemming中休息的姿势",
        breakdown: { root: "stemming" },
        explanation: "四肢全部撑开，放松身体"
      }
    ],
    quiz: {
      question: "stemming主要用于哪种地形？",
      options: ["平滑面", "裂缝/角落", "悬垂", "大平台"],
      correctAnswer: 1
    }
  },
  {
    id: 30,
    root: "dyno (动态)",
    origin: "进阶技术",
    meaning: "利用摆荡和爆发力抓住远点",
    description: "Dyno 是 dynamic movement（动态动作）的简称，指利用身体的摆荡和爆发力抓住远距离的手点。Dyno 是攀岩中最具观赏性的动作之一，需要精确的时机把握和充分的力量。初学者应在安全环境下练习，掌握正确的发力技巧。",
    examples: [
      {
        word: "摆荡",
        meaning: "身体像钟摆一样摆动",
        breakdown: { root: "dyno" },
        explanation: "为dyno积累动能"
      },
      {
        word: "抓空",
        meaning: "dyno时没有抓住目标点",
        breakdown: { root: "dyno" },
        explanation: "常见结果，需要安全保护"
      },
      {
        word: "死点",
        meaning: "刚好能抓住的最远点",
        breakdown: { root: "dyno" },
        explanation: "dyno的目标，通常非常远"
      }
    ],
    quiz: {
      question: "dyno主要依靠什么？",
      options: ["静态力量", "爆发力", "柔韧性", "耐力"],
      correctAnswer: 1
    }
  }
];

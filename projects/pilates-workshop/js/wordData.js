const WordRoots = [
  {
    id: 1,
    root: "核心控制 (Core Control)",
    origin: "基础原则",
    meaning: "通过深层核心肌群维持脊柱稳定和身体对位",
    description: "核心控制是普拉提的基础，强调从深层腹肌（腹横肌）开始，逐步激活腹直肌、腹斜肌和背部肌群。良好的核心控制可以保护腰椎，提高动作效率，预防运动损伤。练习时需保持骨盆中立位，避免过度前倾或后倾，让核心肌群成为所有动作的支点。",
    examples: [
      {
        word: "骨盆中立位",
        meaning: "骨盆自然平衡的位置",
        breakdown: { root: "核心控制" },
        explanation: "髂前上棘与耻骨在同一垂直平面，是核心训练的基础姿态"
      },
      {
        word: "腹横肌",
        meaning: "最深层的腹部肌肉",
        breakdown: { root: "核心控制" },
        explanation: "像束腰一样包裹腹部，是核心稳定的第一道防线"
      },
      {
        word: "腰椎保护",
        meaning: "通过核心力量减轻腰椎压力",
        breakdown: { root: "核心控制" },
        explanation: "强大的核心可以分担腰椎承受的负荷，预防腰痛"
      }
    ],
    quiz: {
      question: "核心控制最先激活哪块肌肉？",
      options: ["腹直肌", "腹横肌", "腹斜肌", "竖脊肌"],
      correctAnswer: 1
    }
  },
  {
    id: 2,
    root: "呼吸 (Breathing)",
    origin: "基础原则",
    meaning: "普拉提特有的横向呼吸法，配合动作节奏",
    description: "普拉提采用横向胸式呼吸，吸气时肋骨向两侧扩张，呼气时肋骨收缩并配合核心收紧。呼吸与动作协调：通常用力时呼气，放松时吸气。正确的呼吸模式可以提高氧气摄入，激活深层核心，帮助动作流畅完成。避免屏气和过度换气。",
    examples: [
      {
        word: "横向呼吸",
        meaning: "肋骨向两侧扩张的呼吸方式",
        breakdown: { root: "呼吸" },
        explanation: "区别于腹式呼吸，强调胸廓的侧向运动"
      },
      {
        word: "呼吸节奏",
        meaning: "呼吸与动作的协调配合",
        breakdown: { root: "呼吸" },
        explanation: "通常用力动作配合呼气，伸展动作配合吸气"
      },
      {
        word: "核心激活",
        meaning: "通过呼气激活深层核心",
        breakdown: { root: "呼吸" },
        explanation: "呼气时想象腹部向脊柱方向收紧"
      }
    ],
    quiz: {
      question: "普拉提采用哪种呼吸方式？",
      options: ["腹式呼吸", "横向胸式呼吸", "完全呼吸", "屏气"],
      correctAnswer: 1
    }
  },
  {
    id: 3,
    root: "专注 (Concentration)",
    origin: "基础原则",
    meaning: "全神贯注于每一个动作和身体感受",
    description: "专注是普拉提的六大原则之一。练习时需要将注意力集中在正在工作的肌肉、身体对位和动作质量上，而不是机械地完成动作。专注可以提高神经肌肉连接，让训练效果事半功倍。每一次练习都是与身体对话的过程，倾听身体的反馈。",
    examples: [
      {
        word: "身心连接",
        meaning: "意识与身体动作的统一",
        breakdown: { root: "专注" },
        explanation: "通过专注建立大脑与肌肉的神经通路"
      },
      {
        word: "动作质量",
        meaning: "重视动作的精准而非数量",
        breakdown: { root: "专注" },
        explanation: "3个精准的动作胜过10个随意的动作"
      },
      {
        word: "身体觉察",
        meaning: "感知身体各部位的位置和状态",
        breakdown: { root: "专注" },
        explanation: "了解自己的身体是改善的第一步"
      }
    ],
    quiz: {
      question: "普拉提更重视什么？",
      options: ["动作数量", "动作质量", "速度", "重量"],
      correctAnswer: 1
    }
  },
  {
    id: 4,
    root: "中心 (Center)",
    origin: "基础原则",
    meaning: "从身体核心发起所有动作",
    description: "中心原则强调所有动作都应从身体的动力核心（Powerhouse）发起。动力核心包括腹部、下背部、臀部和髋部。想象核心是一个能量中心，力量从这里产生并传递到四肢。强壮的中心可以稳定脊柱，提高动作效率，改善姿态。",
    examples: [
      {
        word: "动力核心",
        meaning: "身体的能量中心区域",
        breakdown: { root: "中心" },
        explanation: "包括腹部、腰部、臀部，是所有动作的起点"
      },
      {
        word: "能量传递",
        meaning: "力量从核心传到四肢",
        breakdown: { root: "中心" },
        explanation: "核心稳定后，手脚的动作才能精准高效"
      },
      {
        word: "核心稳定",
        meaning: "保持核心区域的对位和力量",
        breakdown: { root: "中心" },
        explanation: "稳定的核心是四肢自由活动的基础"
      }
    ],
    quiz: {
      question: "普拉提的动力核心不包括？",
      options: ["腹部", "下背部", "臀部", "小腿"],
      correctAnswer: 3
    }
  },
  {
    id: 5,
    root: "控制 (Control)",
    origin: "基础原则",
    meaning: "有意识地控制每一个动作，而非惯性完成",
    description: "控制原则要求在动作过程中保持肌肉的主动参与，避免借助惯性或重力自由落体。每一个动作都应是有意识的、受控的，包括向心收缩（用力）和离心收缩（放松）阶段。控制可以防止受伤，确保目标肌肉得到训练，提高身体觉察能力。",
    examples: [
      {
        word: "向心收缩",
        meaning: "肌肉缩短发力的阶段",
        breakdown: { root: "控制" },
        explanation: "如卷腹时腹部肌肉的收缩"
      },
      {
        word: "离心收缩",
        meaning: "肌肉延长但仍受控的阶段",
        breakdown: { root: "控制" },
        explanation: "如缓慢放下身体时腹部的控制"
      },
      {
        word: "避免惯性",
        meaning: "不借助重力或弹力完成动作",
        breakdown: { root: "控制" },
        explanation: "用肌肉力量控制每一个动作阶段"
      }
    ],
    quiz: {
      question: "控制原则强调避免使用什么？",
      options: ["肌肉力量", "惯性", "呼吸", "核心"],
      correctAnswer: 1
    }
  },
  {
    id: 6,
    root: "精准 (Precision)",
    origin: "基础原则",
    meaning: "动作的标准化和准确性",
    description: "精准原则强调每个动作都有标准的形式和路径，关注细节才能让训练有效。一个精准的动作可以激活目标肌肉，而错误的动作模式可能导致代偿或受伤。初学者应在专业指导下学习正确形式，建立良好的动作模式后再增加难度。",
    examples: [
      {
        word: "动作标准",
        meaning: "符合生物力学的动作形式",
        breakdown: { root: "精准" },
        explanation: "正确的轨迹和对位才能有效训练目标肌群"
      },
      {
        word: "细节关注",
        meaning: "注意动作中的微小调整",
        breakdown: { root: "精准" },
        explanation: "如肩胛骨的位置、脚尖的方向等细节"
      },
      {
        word: "避免代偿",
        meaning: "防止非目标肌肉过度参与",
        breakdown: { root: "精准" },
        explanation: "精准的动作才能避免其他肌肉代偿"
      }
    ],
    quiz: {
      question: "精准原则主要关注什么？",
      options: ["动作速度", "动作准确性", "动作数量", "动作重量"],
      correctAnswer: 1
    }
  },
  {
    id: 7,
    root: "流畅 (Flow)",
    origin: "基础原则",
    meaning: "动作之间的连贯性和优雅",
    description: "流畅原则强调动作之间应无缝衔接，像行云流水一样自然优雅。普拉提不是零散的动作组合，而是一系列连贯的运动流程。流畅的动作需要核心稳定、呼吸协调和良好的身体控制。流畅性体现了身体的整合能力和运动质量。",
    examples: [
      {
        word: "动作衔接",
        meaning: "动作之间的自然过渡",
        breakdown: { root: "流畅" },
        explanation: "上一个动作的结束是下一个动作的开始"
      },
      {
        word: "运动节奏",
        meaning: "动作的速度和韵律",
        breakdown: { root: "流畅" },
        explanation: "匀速、流畅的动作比忽快忽慢更有控制力"
      },
      {
        word: "能量流动",
        meaning: "力量在身体内的传递",
        breakdown: { root: "流畅" },
        explanation: "感受力量从核心流向四肢的过程"
      }
    ],
    quiz: {
      question: "流畅原则强调动作的什么特性？",
      options: ["断续性", "连贯性", "快速性", "力量性"],
      correctAnswer: 1
    }
  },
  {
    id: 8,
    root: "骨盆卷动 (Pelvic Curl)",
    origin: "基础动作",
    meaning: "仰卧位脊柱逐节卷起的经典动作",
    description: "骨盆卷动是普拉提最基础的动作之一。仰卧屈膝，双脚平放，从尾骨开始逐节卷起脊柱，直到肩胛骨支撑，然后逐节落下。这个动作可以激活核心、灵活脊柱、强化臀部。关键是逐节运动，想象脊柱像珍珠项链一样一颗一颗抬起和放下。",
    examples: [
      {
        word: "逐节运动",
        meaning: "脊柱一节一节地活动",
        breakdown: { root: "骨盆卷动" },
        explanation: "从尾骨开始，依次抬起腰椎、胸椎"
      },
      {
        word: "臀部激活",
        meaning: "抬起时收紧臀部肌肉",
        breakdown: { root: "骨盆卷动" },
        explanation: "臀部发力帮助骨盆抬起，同时避免过度夹紧"
      },
      {
        word: "肩胛支撑",
        meaning: "抬起后重量在肩胛骨上",
        breakdown: { root: "骨盆卷动" },
        explanation: "避免重量压在脖子上，保持颈椎自然"
      }
    ],
    quiz: {
      question: "骨盆卷动从哪开始卷起？",
      options: ["颈椎", "胸椎", "腰椎", "尾骨"],
      correctAnswer: 3
    }
  },
  {
    id: 9,
    root: "卷腹 (Chest Lift)",
    origin: "基础动作",
    meaning: "仰卧位上半身抬起的核心训练动作",
    description: "卷腹是普拉提核心训练的基础动作。仰卧屈膝，双手托头，呼气时抬起头部、颈部和肩胛骨，保持腰部贴地，吸气时缓慢落下。与普通仰卧起坐不同，普拉提卷腹幅度较小，强调核心控制和脊柱中立。避免用手拉头，保持颈部自然延伸。",
    examples: [
      {
        word: "腰椎贴地",
        meaning: "保持下背部与地面接触",
        breakdown: { root: "卷腹" },
        explanation: "保护腰椎，确保核心正确参与"
      },
      {
        word: "下巴微收",
        meaning: "保持颈椎自然对位",
        breakdown: { root: "卷腹" },
        explanation: "在头后方放拳头，保持拳头的空间"
      },
      {
        word: "肋骨下滑",
        meaning: "呼气时肋骨向骨盆方向收",
        breakdown: { root: "卷腹" },
        explanation: "帮助激活深层核心，避免肋骨外翻"
      }
    ],
    quiz: {
      question: "普拉提卷腹与普通仰卧起坐的区别是？",
      options: ["幅度更大", "幅度更小", "速度更快", "重量更重"],
      correctAnswer: 1
    }
  },
  {
    id: 10,
    root: "百次呼吸 (The Hundred)",
    origin: "经典动作",
    meaning: "普拉提最著名的热身和核心强化动作",
    description: "百次呼吸是普拉提的标志性动作。仰卧抬起头和肩胛骨，双腿抬起（可伸直或桌台式），手臂在身体两侧上下摆动，配合5次吸气5次呼气的呼吸节奏，共做100次。这个动作可以快速提高体温、激活核心、提升心肺功能。保持颈部放松，核心稳定。",
    examples: [
      {
        word: "桌式腿位",
        meaning: "大腿垂直，小腿平行地面",
        breakdown: { root: "百次呼吸" },
        explanation: "初学者友好的腿部位置，减轻腰部压力"
      },
      {
        word: "手臂摆动",
        meaning: "手臂上下小幅振动",
        breakdown: { root: "百次呼吸" },
        explanation: "保持肩关节稳定，动作小而有力"
      },
      {
        word: "5/5呼吸",
        meaning: "5次短吸5次短呼",
        breakdown: { root: "百次呼吸" },
        explanation: "10次呼吸为一组，共做10组达到100次"
      }
    ],
    quiz: {
      question: "百次呼吸需要做多少次手臂摆动？",
      options: ["50次", "100次", "200次", "10次"],
      correctAnswer: 1
    }
  },
  {
    id: 11,
    root: "单腿画圈 (Single Leg Circle)",
    origin: "基础动作",
    meaning: "仰卧单腿在空中画圈，稳定骨盆",
    description: "单腿画圈训练髋部灵活性和骨盆稳定性。仰卧，一腿抬起垂直地面，在髋关节处画圈，另一腿伸直或屈膝踩地。关键是保持骨盆稳定，不要随腿部画圈而晃动。这个动作可以改善髋关节活动度，增强核心控制能力，美化腿部线条。",
    examples: [
      {
        word: "骨盆稳定",
        meaning: "保持骨盆中立不动",
        breakdown: { root: "单腿画圈" },
        explanation: "如果骨盆晃动，说明画圈范围过大"
      },
      {
        word: "髋部发力",
        meaning: "从髋关节开始画圈",
        breakdown: { root: "单腿画圈" },
        explanation: "大腿在髋臼中旋转，膝盖保持伸直"
      },
      {
        word: "反向画圈",
        meaning: "顺时针和逆时针各做一组",
        breakdown: { root: "单腿画圈" },
        explanation: "均衡发展髋部各方向的灵活性"
      }
    ],
    quiz: {
      question: "单腿画圈时最重要的是什么？",
      options: ["画圈范围大", "骨盆稳定", "速度快", "腿伸直"],
      correctAnswer: 1
    }
  },
  {
    id: 12,
    root: "滚动如球 (Rolling Like a Ball)",
    origin: "经典动作",
    meaning: "坐姿抱腿，利用核心力量前后滚动",
    description: "滚动如球是一个有趣又有效的动作。坐姿屈膝抱腿，脚离地，用核心力量向后滚动到肩胛骨触地，再滚回坐姿。这个动作按摩脊柱，激活核心，提高身体控制力。滚动时保持身体紧缩成球形，用核心而非惯性控制滚动。",
    examples: [
      {
        word: "抱腿坐姿",
        meaning: "双手抱住小腿后侧",
        breakdown: { root: "滚动如球" },
        explanation: "脚离地，核心收紧保持平衡"
      },
      {
        word: "控制滚动",
        meaning: "用核心力量而非惯性滚动",
        breakdown: { root: "滚动如球" },
        explanation: "想象核心是一个弹簧，控制滚动速度"
      },
      {
        word: "脊柱按摩",
        meaning: "滚动时脊柱依次触地",
        breakdown: { root: "滚动如球" },
        explanation: "温和地按摩脊柱，促进血液循环"
      }
    ],
    quiz: {
      question: "滚动如球主要靠什么控制？",
      options: ["惯性", "核心力量", "手臂拉力", "腿部力量"],
      correctAnswer: 1
    }
  },
  {
    id: 13,
    root: "单腿伸展 (Single Leg Stretch)",
    origin: "经典动作",
    meaning: "仰卧抬起上半身，双腿交替伸展",
    description: "单腿伸展是腹部训练系列的一部分。仰卧抬起头和肩胛骨，一腿伸直靠近身体，双手抱另一屈膝腿靠近胸部，双腿交替交换。这个动作强化腹部，提高协调性，伸展腿部。保持上身稳定，用腹部力量而非颈部力量维持上身抬起。",
    examples: [
      {
        word: "交替伸展",
        meaning: "双腿像剪刀一样交替",
        breakdown: { root: "单腿伸展" },
        explanation: "一条腿屈膝靠近，另一条腿伸直远离"
      },
      {
        word: "上身稳定",
        meaning: "肩胛骨保持抬起不动",
        breakdown: { root: "单腿伸展" },
        explanation: "避免上身随腿部动作晃动"
      },
      {
        word: "腿部伸展",
        meaning: "伸直的腿远离身体",
        breakdown: { root: "单腿伸展" },
        explanation: "同时伸展髋屈肌，增加动作幅度"
      }
    ],
    quiz: {
      question: "单腿伸展主要训练哪个部位？",
      options: ["手臂", "腹部", "腿部", "背部"],
      correctAnswer: 1
    }
  },
  {
    id: 14,
    root: "双腿伸展 (Double Leg Stretch)",
    origin: "经典动作",
    meaning: "双臂双腿同时伸展，挑战核心稳定",
    description: "双腿伸展是单腿伸展的进阶版。仰卧抬起上身，双腿屈膝靠近胸部，双手抱膝，然后同时伸展双臂向后、双腿向前，再收回到起始位置。这个动作大大增加了对核心稳定性的挑战，同时训练协调性和身体感知能力。",
    examples: [
      {
        word: "同时伸展",
        meaning: "手臂和腿同时向相反方向伸展",
        breakdown: { root: "双腿伸展" },
        explanation: "增加动作幅度，加大核心挑战"
      },
      {
        word: "画圈收回",
        meaning: "手臂从侧面画圈回到腿部",
        breakdown: { root: "双腿伸展" },
        explanation: "增加肩部活动度和动作流畅性"
      },
      {
        word: "腰部保护",
        meaning: "始终保持腰部贴地",
        breakdown: { root: "双腿伸展" },
        explanation: "如果腰拱起，说明核心力量不足，应减小幅度"
      }
    ],
    quiz: {
      question: "双腿伸展与单腿伸展的主要区别是？",
      options: ["速度不同", "幅度更大", "同时伸展四肢", "重量不同"],
      correctAnswer: 2
    }
  },
  {
    id: 15,
    root: "脊柱前伸 (Spine Stretch Forward)",
    origin: "基础动作",
    meaning: "坐姿脊柱逐节前屈的伸展动作",
    description: "脊柱前伸是经典的普拉提伸展动作。坐姿双腿伸直分开与髋同宽，双臂前平举，呼气时从头顶开始逐节前屈脊柱，直到腹部靠近大腿，吸气时逐节回正。这个动作伸展脊柱、腘绳肌，改善姿态。关键是逐节运动，而不是整体前倾。",
    examples: [
      {
        word: "逐节前屈",
        meaning: "脊柱一节一节向前弯曲",
        breakdown: { root: "脊柱前伸" },
        explanation: "从颈椎开始，依次弯曲胸椎、腰椎"
      },
      {
        word: "腘绳肌伸展",
        meaning: "大腿后侧肌群的伸展",
        breakdown: { root: "脊柱前伸" },
        explanation: "如果腿后侧紧，可以微屈膝"
      },
      {
        word: "逐节回正",
        meaning: "从尾骨开始依次回正脊柱",
        breakdown: { root: "脊柱前伸" },
        explanation: "最后头才回到直立位置"
      }
    ],
    quiz: {
      question: "脊柱前伸从哪开始弯曲？",
      options: ["腰椎", "胸椎", "颈椎/头顶", "尾骨"],
      correctAnswer: 2
    }
  },
  {
    id: 16,
    root: "天鹅式 (Swan)",
    origin: "经典动作",
    meaning: "俯卧位脊柱后伸，强化背部",
    description: "天鹅式是普拉提中重要的背部训练动作。俯卧，双手在肩膀下方，呼气时抬起胸部和头部，伸展脊柱，吸气时落下。这个动作强化背部伸肌，改善圆肩驼背，打开胸腔。动作应来自背部力量，而非用手推地，保持耻骨贴地保护腰椎。",
    examples: [
      {
        word: "背部发力",
        meaning: "用背部肌肉抬起上身",
        breakdown: { root: "天鹅式" },
        explanation: "想象背部肌肉缩短将上身拉起"
      },
      {
        word: "脊柱伸展",
        meaning: "胸椎段的后伸",
        breakdown: { root: "天鹅式" },
        explanation: "打开胸腔，改善驼背姿态"
      },
      {
        word: "耻骨贴地",
        meaning: "保持骨盆前侧与地面接触",
        breakdown: { root: "天鹅式" },
        explanation: "限制腰椎过度伸展，保护腰部"
      }
    ],
    quiz: {
      question: "天鹅式主要强化哪个部位？",
      options: ["腹部", "背部", "腿部", "手臂"],
      correctAnswer: 1
    }
  },
  {
    id: 17,
    root: "锯式 (Saw)",
    origin: "经典动作",
    meaning: "坐姿脊柱旋转加前屈的组合动作",
    description: "锯式结合了脊柱旋转和前屈。坐姿双腿伸直分开，双臂侧平举，呼气时旋转躯干并前屈，一手触对侧脚外侧，另一手向后伸展，吸气时回正再转向另一侧。这个动作提高脊柱旋转灵活性，伸展腿部，强化核心控制。保持骨盆稳定，旋转来自胸椎。",
    examples: [
      {
        word: "脊柱旋转",
        meaning: "胸椎段的转动",
        breakdown: { root: "锯式" },
        explanation: "从腰部以上旋转，骨盆保持稳定"
      },
      {
        word: "对角伸展",
        meaning: "一手向前一手向后形成对角线",
        breakdown: { root: "锯式" },
        explanation: "增加躯干旋转幅度和肩部伸展"
      },
      {
        word: "骨盆稳定",
        meaning: "旋转时骨盆正对前方",
        breakdown: { root: "锯式" },
        explanation: "确保旋转来自胸椎而非骨盆"
      }
    ],
    quiz: {
      question: "锯式的旋转应该来自哪里？",
      options: ["腰椎", "胸椎", "颈椎", "骨盆"],
      correctAnswer: 1
    }
  },
  {
    id: 18,
    root: "平板支撑 (Plank)",
    origin: "强化动作",
    meaning: "俯卧位全身保持一条直线的等长收缩动作",
    description: "平板支撑是核心训练的王者动作。俯卧，用前臂和脚尖支撑，身体成一条直线，保持自然呼吸。这个动作强化整个核心、肩部、臀部和腿部。关键是保持身体成直线，不塌腰不撅臀，肩胛骨保持稳定。时间不是唯一标准，质量更重要。",
    examples: [
      {
        word: "身体成线",
        meaning: "耳肩髋踝在一条直线上",
        breakdown: { root: "平板支撑" },
        explanation: "避免塌腰或撅臀，保持脊柱中立"
      },
      {
        word: "核心收紧",
        meaning: "腹部向脊柱方向收紧",
        breakdown: { root: "平板支撑" },
        explanation: "想象有人要打你的肚子，你收紧防御"
      },
      {
        word: "肩胛稳定",
        meaning: "肩胛骨不突起或下沉",
        breakdown: { root: "平板支撑" },
        explanation: "保持肩胛骨平贴在胸廓上"
      }
    ],
    quiz: {
      question: "平板支撑时身体应该是什么形状？",
      options: ["弧形", "一条直线", "V形", "S形"],
      correctAnswer: 1
    }
  },
  {
    id: 19,
    root: "侧平板 (Side Plank)",
    origin: "强化动作",
    meaning: "侧卧位侧身支撑，强化侧腹和臀部",
    description: "侧平板是平板支撑的变体，侧卧，用一侧前臂和脚外侧支撑，髋部抬起，身体成直线。这个动作强化腹斜肌、臀部外展肌和肩部。可以强化侧腹线条，改善脊柱侧弯，提高侧向稳定性。保持髋部不上沉，身体成一条斜线。",
    examples: [
      {
        word: "髋部抬起",
        meaning: "将髋部从地面抬起",
        breakdown: { root: "侧平板" },
        explanation: "用侧腹和臀部力量支撑身体重量"
      },
      {
        word: "身体成线",
        meaning: "从头到脚成一条斜线",
        breakdown: { root: "侧平板" },
        explanation: "避免髋部下沉或前倾"
      },
      {
        word: "腹斜肌",
        meaning: "侧腹部的肌肉",
        breakdown: { root: "侧平板" },
        explanation: "侧平板是训练腹斜肌的最佳动作之一"
      }
    ],
    quiz: {
      question: "侧平板主要训练哪块肌肉？",
      options: ["腹直肌", "腹斜肌", "竖脊肌", "髋屈肌"],
      correctAnswer: 1
    }
  },
  {
    id: 20,
    root: "桥式 (Bridge)",
    origin: "基础动作",
    meaning: "仰卧位抬起臀部的经典动作",
    description: "桥式是强化臀部和下背部的有效动作。仰卧屈膝，双脚平放，呼气时抬起臀部直到身体成斜线，吸气时缓慢落下。这个动作可以激活臀大肌，改善臀部无力，保护腰椎。抬起时收紧臀部和核心，避免过度顶腰，重点在臀部发力。",
    examples: [
      {
        word: "臀部激活",
        meaning: "抬起时主动收紧臀部",
        breakdown: { root: "桥式" },
        explanation: "感受臀部肌肉缩短发力"
      },
      {
        word: "避免顶腰",
        meaning: "不要过度伸展腰椎",
        breakdown: { root: "桥式" },
        explanation: "肋骨不要突出，保持核心稳定"
      },
      {
        word: "肩胛支撑",
        meaning: "重量分散在肩胛和双脚",
        breakdown: { root: "桥式" },
        explanation: "颈部放松，不要压脖子"
      }
    ],
    quiz: {
      question: "桥式主要训练哪个部位？",
      options: ["腹部", "臀部", "背部", "腿部"],
      correctAnswer: 1
    }
  },
  {
    id: 21,
    root: "单腿踢 (Single Leg Kick)",
    origin: "经典动作",
    meaning: "俯卧位双腿交替向后踢",
    description: "单腿踢是背部伸展系列的动作。俯卧，双肘撑地，抬起胸部，双腿交替屈膝向后踢。这个动作强化背部和臀部，灵活膝关节。保持上身稳定，踢腿时核心收紧保护腰部。动作节奏轻快但受控，像游泳踢水一样。",
    examples: [
      {
        word: "交替踢腿",
        meaning: "双腿像剪刀一样交替",
        breakdown: { root: "单腿踢" },
        explanation: "一条腿屈膝踢，另一条腿伸直"
      },
      {
        word: "上身抬起",
        meaning: "胸部离开地面",
        breakdown: { root: "单腿踢" },
        explanation: "保持背部发力，肩胛骨稳定"
      },
      {
        word: "脚跟找臀",
        meaning: "屈膝时脚跟靠近臀部",
        breakdown: { root: "单腿踢" },
        explanation: "增加膝关节屈曲幅度"
      }
    ],
    quiz: {
      question: "单腿踢时上身应该？",
      options: ["贴地", "抬起", "侧转", "前屈"],
      correctAnswer: 1
    }
  },
  {
    id: 22,
    root: "双腿踢 (Double Leg Kick)",
    origin: "经典动作",
    meaning: "俯卧位双腿同时向后踢",
    description: "双腿踢是单腿踢的进阶版。俯卧，双手在背后十指交扣，双腿同时屈膝向后踢三下，然后伸直双腿并抬起上身，双手向后伸展。这个动作强化整个背部，打开肩部和胸腔。动作要有节奏感，踢三下后伸展，配合呼吸。",
    examples: [
      {
        word: "三下踢腿",
        meaning: "双腿同时屈膝踢三下",
        breakdown: { root: "双腿踢" },
        explanation: "快速但受控的三次踢腿"
      },
      {
        word: "双手后伸",
        meaning: "上身抬起时双手向后",
        breakdown: { root: "双腿踢" },
        explanation: "打开肩部和胸腔，伸展胸肌"
      },
      {
        word: "脊柱伸展",
        meaning: "上身抬起的后伸动作",
        breakdown: { root: "双腿踢" },
        explanation: "强化背部伸肌，改善姿态"
      }
    ],
    quiz: {
      question: "双腿踢时双腿需要踢几下？",
      options: ["1下", "2下", "3下", "5下"],
      correctAnswer: 2
    }
  },
  {
    id: 23,
    root: " teaser",
    origin: "高级动作",
    meaning: "仰卧位全身V字平衡的高级核心动作",
    description: "Teaser是普拉提的高级动作，被称为'终极核心挑战'。仰卧，同时抬起上身和双腿，身体形成V字形，只用臀部支撑平衡。这个动作需要极强的核心力量、协调性和平衡能力。初学者可以先练习半 teaser（一腿伸直一腿屈膝）。",
    examples: [
      {
        word: "V字平衡",
        meaning: "身体形成V字形",
        breakdown: { root: "Teaser" },
        explanation: "上身和双腿抬起，重心在臀部"
      },
      {
        word: "全身整合",
        meaning: "核心、髋屈肌、背部的协同工作",
        breakdown: { root: "Teaser" },
        explanation: "需要多个肌群同时参与的高级动作"
      },
      {
        word: "半 teaser",
        meaning: "一腿伸直一腿屈膝的简化版",
        breakdown: { root: "Teaser" },
        explanation: "初学者友好的退阶动作"
      }
    ],
    quiz: {
      question: "Teaser 动作身体形成什么形状？",
      options: ["直线", "V字", "圆形", "S形"],
      correctAnswer: 1
    }
  },
  {
    id: 24,
    root: "游泳式 (Swimming)",
    origin: "经典动作",
    meaning: "俯卧位四肢交替上下摆动",
    description: "游泳式模仿自由泳的动作模式。俯卧，抬起胸部和双腿，双臂双腿交替上下摆动。这个动作强化背部深层肌群，改善脊柱稳定性，提高协调性。保持核心收紧保护腰部，动作流畅有节奏，不要憋气。",
    examples: [
      {
        word: "对侧伸展",
        meaning: "左手和右腿同时抬起",
        breakdown: { root: "游泳式" },
        explanation: "模拟爬行模式，训练协调性"
      },
      {
        word: "核心稳定",
        meaning: "保持腰部不塌陷",
        breakdown: { root: "游泳式" },
        explanation: "核心力量支撑四肢动作"
      },
      {
        word: "背部深层",
        meaning: "多裂肌等深层稳定肌",
        breakdown: { root: "游泳式" },
        explanation: "游泳式是训练背部深层肌的好方法"
      }
    ],
    quiz: {
      question: "游泳式主要训练什么能力？",
      options: ["爆发力", "协调性", "柔韧性", "耐力"],
      correctAnswer: 1
    }
  },
  {
    id: 25,
    root: "肩桥 (Shoulder Bridge)",
    origin: "进阶动作",
    meaning: "桥式基础上抬起一腿的进阶动作",
    description: "肩桥是桥式的进阶版。从桥式开始，抬起一腿伸直指向天花板，保持臀部高度稳定，然后换腿。这个动作增加对臀部和核心的挑战，提高骨盆稳定性，伸展腿部。保持支撑腿的臀部不下降，骨盆保持水平。",
    examples: [
      {
        word: "单腿抬起",
        meaning: "一腿伸直指向天花板",
        breakdown: { root: "肩桥" },
        explanation: "增加不稳定因素，加大核心挑战"
      },
      {
        word: "骨盆水平",
        meaning: "保持骨盆两侧同高",
        breakdown: { root: "肩桥" },
        explanation: "避免一侧髋部下沉或上提"
      },
      {
        word: "臀部稳定",
        meaning: "支撑腿臀部保持高度",
        breakdown: { root: "肩桥" },
        explanation: "用臀部力量维持桥式高度"
      }
    ],
    quiz: {
      question: "肩桥与桥式的主要区别是？",
      options: ["速度不同", "单腿抬起", "手臂位置", "呼吸方式"],
      correctAnswer: 1
    }
  },
  {
    id: 26,
    root: "开瓶器 (Corkscrew)",
    origin: "高级动作",
    meaning: "仰卧位双腿画圈同时骨盆侧转",
    description: "开瓶器是高级的脊柱旋转动作。仰卧，双腿抬起垂直地面，双臂放在身体两侧，双腿一起向一侧画圈，同时骨盆稍微抬起并侧转，然后向另一侧画圈。这个动作灵活脊柱，强化核心控制，改善脊柱旋转能力。保持肩膀贴地，动作流畅缓慢。",
    examples: [
      {
        word: "双腿画圈",
        meaning: "双腿并拢做圆周运动",
        breakdown: { root: "开瓶器" },
        explanation: "像开瓶器一样旋转"
      },
      {
        word: "骨盆抬起",
        meaning: "画圈时骨盆稍微离地",
        breakdown: { root: "开瓶器" },
        explanation: "增加核心挑战和脊柱活动度"
      },
      {
        word: "肩膀贴地",
        meaning: "旋转时保持肩胛骨贴地",
        breakdown: { root: "开瓶器" },
        explanation: "确保旋转来自腰椎而非胸椎"
      }
    ],
    quiz: {
      question: "开瓶器动作像什么工具的运动？",
      options: ["螺丝刀", "开瓶器", "扳手", "钳子"],
      correctAnswer: 1
    }
  },
  {
    id: 27,
    root: "剪刀式 (Scissors)",
    origin: "经典动作",
    meaning: "仰卧位双腿交替上下摆动",
    description: "剪刀式是普拉提腿部系列的动作。仰卧，抬起双腿垂直地面，双手支撑臀部，双腿像剪刀一样交替上下摆动。这个动作灵活髋关节，强化核心控制，伸展腿部后侧。保持双腿伸直，动作流畅有控制，骨盆保持稳定。",
    examples: [
      {
        word: "双手支撑",
        meaning: "双手托住臀部帮助稳定",
        breakdown: { root: "剪刀式" },
        explanation: "给核心一些辅助，让动作更容易控制"
      },
      {
        word: "交替摆动",
        meaning: "双腿像剪刀一样上下",
        breakdown: { root: "剪刀式" },
        explanation: "一腿向上，一腿向下，幅度适中"
      },
      {
        word: "骨盆稳定",
        meaning: "保持骨盆不晃动",
        breakdown: { root: "剪刀式" },
        explanation: "核心力量控制骨盆位置"
      }
    ],
    quiz: {
      question: "剪刀式中双手的作用是什么？",
      options: ["拉起身体", "支撑臀部", "伸展手臂", "保持平衡"],
      correctAnswer: 1
    }
  },
  {
    id: 28,
    root: "自行车式 (Bicycle)",
    origin: "经典动作",
    meaning: "仰卧位双腿交替做骑车动作",
    description: "自行车式模仿骑自行车的动作。仰卧，抬起上身和双腿，双腿交替屈膝伸直，像踩自行车一样。这个动作强化腹部，灵活髋关节，提高协调性。保持上身稳定，核心收紧，动作有节奏感。这是一个很有效的腹部训练动作。",
    examples: [
      {
        word: "骑车动作",
        meaning: "双腿交替屈膝伸直",
        breakdown: { root: "自行车式" },
        explanation: "模拟骑车踏板运动"
      },
      {
        word: "上身抬起",
        meaning: "肩胛骨离开地面",
        breakdown: { root: "自行车式" },
        explanation: "增加腹部训练的强度"
      },
      {
        word: "节奏感",
        meaning: "动作流畅有节奏",
        breakdown: { root: "自行车式" },
        explanation: "不要太快或太慢，保持均匀节奏"
      }
    ],
    quiz: {
      question: "自行车式模仿什么运动？",
      options: ["跑步", "游泳", "骑车", "跳舞"],
      correctAnswer: 2
    }
  },
  {
    id: 29,
    root: "骨盆时钟 (Pelvic Clock)",
    origin: "基础动作",
    meaning: "仰卧位骨盆做圆周运动",
    description: "骨盆时钟是一个觉察骨盆位置的基础动作。仰卧屈膝，想象骨盆是一个时钟，12点在肚脐，6点在耻骨，缓慢移动骨盆画圆。这个动作提高骨盆觉察能力，灵活髋关节，改善骨盆控制。动作应缓慢细腻，感受骨盆的微小运动。",
    examples: [
      {
        word: "12点6点",
        meaning: "骨盆前倾和后倾",
        breakdown: { root: "骨盆时钟" },
        explanation: "腰椎拱起和压平的动作"
      },
      {
        word: "3点9点",
        meaning: "骨盆左右侧倾",
        breakdown: { root: "骨盆时钟" },
        explanation: "骨盆左右高低变化"
      },
      {
        word: "画圆运动",
        meaning: "骨盆做圆周轨迹",
        breakdown: { root: "骨盆时钟" },
        explanation: "将前倾后倾侧倾连贯成圆"
      }
    ],
    quiz: {
      question: "骨盆时钟想象骨盆是什么？",
      options: ["球", "时钟", "方块", "直线"],
      correctAnswer: 1
    }
  },
  {
    id: 30,
    root: "呼吸式 (Breathing)",
    origin: "基础动作",
    meaning: "坐姿专注呼吸的放松动作",
    description: "呼吸式是普拉提课程中常用的放松和专注动作。舒适坐姿，双手放在肋骨两侧，闭眼，专注感受呼吸时肋骨的扩张和收缩。这个动作帮助建立正确的呼吸模式，放松身心，提高身体觉察。可以在课程开始或结束时做，也可以作为日常放松练习。",
    examples: [
      {
        word: "手放肋骨",
        meaning: "双手感受肋骨运动",
        breakdown: { root: "呼吸式" },
        explanation: "触觉反馈帮助建立正确的呼吸意识"
      },
      {
        word: "肋骨扩张",
        meaning: "吸气时肋骨向两侧打开",
        breakdown: { root: "呼吸式" },
        explanation: "横向呼吸的关键特征"
      },
      {
        word: "身心放松",
        meaning: "通过呼吸放松身心",
        breakdown: { root: "呼吸式" },
        explanation: "专注呼吸可以帮助平静心情"
      }
    ],
    quiz: {
      question: "呼吸式时手应该放在哪里？",
      options: ["腹部", "肋骨", "胸口", "头顶"],
      correctAnswer: 1
    }
  }
];

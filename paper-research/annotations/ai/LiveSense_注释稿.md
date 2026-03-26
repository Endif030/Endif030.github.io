# LiveSense: 用笔记本WiFi做厘米级传感器

## 论文信息

**标题**: LiveSense: A Real-Time Wi-Fi Sensing Platform for Range-Doppler on COTS Laptop  
**arXiv ID**: 2603.06545  
**作者**: Jessica Sanson, Rahul C. Shah, Maximilian Pinaroc  
**领域**: 普适计算 / 无线感知 / 物联网

---

## 【原文】Abstract

We present LiveSense - a cross-platform that transforms a commercial off-the-shelf (COTS) Wi-Fi Network Interface Card (NIC) on a laptop into a centimeter-level Range-Doppler sensor while preserving simultaneous communication capability.

## 【中文翻译】摘要

我们提出LiveSense——一个跨平台系统，将笔记本电脑上的商用现成（COTS）WiFi网络接口卡（NIC）转变为厘米级距离-多普勒传感器，同时保持正常的通信能力。

## 【注释解释】

- **COTS (Commercial Off-The-Shelf)**: 商用现成产品，无需定制硬件
- **Range-Doppler**: 距离-多普勒联合感知
  - Range: 目标距离（通过信号传播时间计算）
  - Doppler: 目标速度（通过多普勒频移计算）
- **CSI (Channel State Information)**: 信道状态信息，WiFi信号在物理层的详细参数
- **NIC (Network Interface Card)**: 网络接口卡，即WiFi模块

---

## 核心创新

**用通信设备做感知**:
- 普通WiFi网卡 → 厘米级传感器
- 同时保持正常WiFi通信
- 无需额外硬件

**技术原理**:
1. **CSI利用**: 从WiFi信号物理层提取环境信息
2. **MIMO技术**: 多天线接收，形成"虚拟雷达"
3. **信号处理**: 从噪声中提取微小变化（如人体呼吸引起的信号变化）

---

## 应用场景

| 场景 | 原理 | 精度 |
|------|------|------|
| 人体存在检测 | 人体移动引起信号变化 | 存在/不存在 |
| 手势识别 | 手部动作的多普勒特征 | 厘米级 |
| 跌倒检测 | 突然的姿态变化 | 秒级响应 |
| 呼吸监测 | 胸部起伏的微小位移 | 亚厘米级 |
| 睡眠质量监测 | 睡眠中的微动 | 整夜连续 |

---

## 为什么这很酷？

**技术民主化**:
- 不需要专用雷达（贵、大、功耗高）
- 笔记本电脑、手机都可用
- 低成本、大规模部署

**无形界面**:
- 不需要穿戴设备
- 不需要摄像头（隐私友好）
- 人在家中坐，系统已感知

**隐私友好**:
- 只感知存在/动作，不识别身份
- 无视频记录
- 符合隐私法规

---

## 跨学科关联

- **人类学**: 技术如何悄然融入日常生活（普适计算愿景）
- **设计学**: Calm Technology（平静技术）——技术应该退到背景中
- **社会学**: 隐私与便利的边界，监控与关怀的区分

---

## 与Fly360的对比

| 维度 | Fly360 | LiveSense |
|------|--------|-----------|
| 感知方式 | 光学摄像头（全景） | WiFi信号（无线电） |
| 主动性 | 主动发射光 | 被动利用现有信号 |
| 隐私 | 需要图像处理 | 信号处理，隐私友好 |
| 应用场景 | 户外导航 | 室内监测 |

---

## 思考问题

1. WiFi感知能否识别具体是谁在房间里？（身份识别 vs 存在检测）
2. 多个WiFi设备之间会互相干扰吗？
3. 这项技术可能被滥用吗？（如暗中监控）

# Spanish Learning Studio

面向 Roy 的西语学习网站（长期日更版）。

## 当前状态
- ✅ Day1 已上线（`day-001`）
- ✅ 支持句子发音播放（浏览器 Web Speech）
- ✅ 支持跟读打卡与本地进度存储
- ✅ 框架已预留 Day2+ 扩展

## 如何新增 Day2/Day3
1. 打开 `js/curriculum.js`
2. 按 `day-001` 的结构新增一个对象，id 改成 `day-002` 等
3. 在 `index.html` 导航区增加对应链接

## 本地运行
直接浏览器打开 `index.html` 即可；若语音不可用，建议 Chrome 打开。

## 后续可增强
- 接入 Google/Azure TTS（替代浏览器默认声音）
- 跟读录音上传 + 自动评分
- 周测页面与复盘页

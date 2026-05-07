# XHS Cover Collage Studio

一个纯前端静态工具网站，用于制作小红书笔记封面配图。

## 已实现能力
- 电脑 / 手机 H5 响应式布局
- 上传 2-12 张图片
- 竖屏比例预设：9:16、3:4
- 基础拼图模板：横向等分、竖向等分、网格、主次分屏
- 创意斜切模板：3-6 张中心放射 / 交叉切分模板
- 单图区图片拖拽、缩放、旋转
- 当前区域图片替换、重置、铺满、完整显示
- 导出 PNG / JPG，支持 1x / 2x / 3x
- 分割线样式控制：显示开关、颜色、粗细
- 模板缩略图与当前真实模板比例同步

## 模板规则文件
斜切模板规则已抽离到：
- [diagonal-template-rules.js](file:///Users/royluo/.craft-agent/workspaces/my-workspace/xhs-cover-collage/diagonal-template-rules.js)

当前 `app.js` 会读取 `window.DIAGONAL_TEMPLATE_RULES` 来生成 3 / 4 / 5 / 6 图斜切模板。

## 本地运行
可直接用任意静态文件服务器打开，例如：

```bash
cd /Users/royluo/.craft-agent/workspaces/my-workspace/xhs-cover-collage
python3 -m http.server 4173
```

然后访问：
[http://127.0.0.1:4173](http://127.0.0.1:4173)

## 说明
- 当前实现为无后端版本，所有图片处理都在浏览器本地完成。
- 斜切模板支持独立规则配置，便于后续继续微调角度与边界点。
- 若后续继续产品化，建议下一步补：本地草稿、模板收藏、边距圆角、模板预览优化。
